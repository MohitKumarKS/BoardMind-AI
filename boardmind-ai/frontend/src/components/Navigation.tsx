import { NavLink } from "react-router-dom";
import "./Navigation.css";

function Navigation() {
  return (
    <header className="nav">
      <div className="nav__container">
        <NavLink to="/" className="nav__brand">
          <span className="nav__logo" aria-hidden="true">B</span>
          <span className="nav__brand-text">BoardMind AI</span>
        </NavLink>
        <nav className="nav__links" aria-label="Main navigation">
          <NavLink
            to="/workspace"
            className={({ isActive }) =>
              `nav__link ${isActive ? "nav__link--active" : ""}`
            }
          >
            Workspace
          </NavLink>
          <NavLink
            to="/boardroom"
            className={({ isActive }) =>
              `nav__link ${isActive ? "nav__link--active" : ""}`
            }
          >
            Boardroom
          </NavLink>
          <NavLink
            to="/history"
            className={({ isActive }) =>
              `nav__link ${isActive ? "nav__link--active" : ""}`
            }
          >
            History
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

export default Navigation;
