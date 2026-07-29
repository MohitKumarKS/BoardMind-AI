import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import "./HomePage.css";

function HomePage() {
  return (
    <div className="home">
      <motion.div
        className="home__hero"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="home__logo-mark" aria-hidden="true">
          <span>B</span>
        </div>
        <h1 className="home__title">BoardMind AI</h1>
        <p className="home__tagline">Executive Multi-Agent Decision Intelligence Platform</p>
        <p className="home__description">
          Submit any business scenario and receive cross-functional analysis from
          8 AI department heads. Get consensus-driven recommendations backed by
          finance, marketing, sales, HR, operations, legal, IT, and analytics perspectives.
        </p>
      </motion.div>

      <motion.div
        className="home__cards"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.15 }}
      >
        <Link to="/workspace" className="home__card home__card--workspace">
          <div className="home__card-icon" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </div>
          <h2 className="home__card-title">Department Workspace</h2>
          <p className="home__card-desc">
            Consult individual department heads for focused,
            single-perspective analysis of your business scenario.
          </p>
          <span className="home__card-cta">8 departments available</span>
        </Link>

        <Link to="/boardroom" className="home__card home__card--boardroom">
          <div className="home__card-icon" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
              <line x1="8" y1="21" x2="16" y2="21"/>
              <line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
          </div>
          <h2 className="home__card-title">Executive Boardroom</h2>
          <p className="home__card-desc">
            Full board meeting with multi-department analysis,
            consensus engine, and executive decision report.
          </p>
          <span className="home__card-cta">AI-powered consensus</span>
        </Link>
      </motion.div>

      <motion.div
        className="home__features"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.3 }}
      >
        <div className="home__feature">
          <span className="home__feature-number">8</span>
          <span className="home__feature-label">AI Departments</span>
        </div>
        <div className="home__feature">
          <span className="home__feature-number">14</span>
          <span className="home__feature-label">Business Categories</span>
        </div>
        <div className="home__feature">
          <span className="home__feature-number">&lt;2s</span>
          <span className="home__feature-label">Analysis Time</span>
        </div>
        <div className="home__feature">
          <span className="home__feature-number">PDF</span>
          <span className="home__feature-label">Executive Reports</span>
        </div>
      </motion.div>
    </div>
  );
}

export default HomePage;
