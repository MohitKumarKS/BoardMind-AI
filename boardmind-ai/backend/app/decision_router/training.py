"""Decision Router model training.

Trains a TF-IDF + LinearSVC pipeline from the built-in dataset.
The model is trained once at module load time and cached in memory.
"""

import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

from .dataset import TRAINING_DATA
from .labels import BUSINESS_CATEGORIES

logger = logging.getLogger(__name__)


def build_pipeline() -> Pipeline:
    """Build the TF-IDF + calibrated LinearSVC pipeline.

    Uses CalibratedClassifierCV to enable probability estimates
    from LinearSVC, which does not natively support predict_proba.
    """
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            stop_words="english",
            sublinear_tf=True,
        )),
        ("classifier", CalibratedClassifierCV(
            estimator=LinearSVC(
                C=1.0,
                max_iter=10000,
                class_weight="balanced",
            ),
            cv=3,
        )),
    ])
    return pipeline


def train_model() -> Pipeline:
    """Train the decision router model from the built-in dataset.

    Returns:
        Trained sklearn Pipeline ready for prediction.
    """
    texts = [text for text, _ in TRAINING_DATA]
    labels = [label for _, label in TRAINING_DATA]

    # Validate that all labels are in known categories
    unknown = set(labels) - set(BUSINESS_CATEGORIES)
    if unknown:
        raise ValueError(f"Unknown categories in training data: {unknown}")

    # Validate all categories have training samples
    label_set = set(labels)
    missing = set(BUSINESS_CATEGORIES) - label_set
    if missing:
        logger.warning(f"Categories without training data: {missing}")

    pipeline = build_pipeline()
    pipeline.fit(texts, labels)

    # Log training accuracy
    scores = cross_val_score(build_pipeline(), texts, labels, cv=3, scoring="accuracy")
    logger.info(
        f"Decision Router trained: {len(texts)} samples, "
        f"{len(set(labels))} categories, "
        f"CV accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})"
    )

    return pipeline


# Module-level singleton: train once at import time
_model: Pipeline | None = None


def get_model() -> Pipeline:
    """Get the trained model, training on first access."""
    global _model
    if _model is None:
        _model = train_model()
    return _model


def predict(text: str) -> tuple[str, float]:
    """Predict the business category for a given text.

    Args:
        text: The business scenario text.

    Returns:
        Tuple of (predicted_category, confidence_score).
    """
    model = get_model()
    probas = model.predict_proba([text])[0]
    classes = model.classes_

    best_idx = np.argmax(probas)
    predicted_category = classes[best_idx]
    confidence = float(probas[best_idx])

    return predicted_category, confidence
