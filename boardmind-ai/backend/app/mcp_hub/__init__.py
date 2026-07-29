"""MCP Knowledge Hub.

Centralized knowledge layer for executive agents backed by PostgreSQL.
Three independent services:
- EvidenceService: domain-specific evidence retrieval
- StorageService: persists agent analyses and consensus results
- HistoryService: retrieves historical board decisions for context

This module is purely additive — the existing orchestration works
without it, and falls back gracefully if PostgreSQL is unavailable.
"""

from .config import get_database_url, is_hub_configured
from .evidence_service import EvidenceService
from .storage_service import StorageService
from .history_service import HistoryService

__all__ = [
    "EvidenceService",
    "StorageService",
    "HistoryService",
    "get_database_url",
    "is_hub_configured",
]
