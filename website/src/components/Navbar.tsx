import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import mascotLogo from "../assets/durable-request-mascot-logo.png";

const REPO_URL = "http://git.enflame.cn/skills/durablerequest";

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const isHome = location.pathname === "/";

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-[var(--background)]/80 backdrop-blur-xl border-b"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-lg">
          <img src={mascotLogo} alt="DurableRequest" className="w-7 h-7" />
          <span>durable-request</span>
        </Link>
        <div className="hidden sm:flex items-center gap-8 text-sm text-[var(--muted-foreground)]">
          {isHome ? (
            <a href="#features" className="hover:text-[var(--foreground)] transition-colors">
              Product
            </a>
          ) : (
            <Link to="/" className="hover:text-[var(--foreground)] transition-colors">
              Product
            </Link>
          )}
          <Link
            to="/changelog"
            className={`hover:text-[var(--foreground)] transition-colors ${
              location.pathname === "/changelog" ? "text-[var(--foreground)] font-semibold" : ""
            }`}
          >
            Changelog
          </Link>
          <Link
            to="/roadmap"
            className={`hover:text-[var(--foreground)] transition-colors ${
              location.pathname === "/roadmap" ? "text-[var(--foreground)] font-semibold" : ""
            }`}
          >
            Roadmap
          </Link>
          <Link
            to="/steering"
            className={`hover:text-[var(--foreground)] transition-colors ${
              location.pathname === "/steering" ? "text-[var(--foreground)] font-semibold" : ""
            }`}
          >
            <span className="text-amber-400">⚡</span> Steering
          </Link>
          <Link
            to="/health"
            className={`hover:text-[var(--foreground)] transition-colors ${
              location.pathname === "/health" ? "text-[var(--foreground)] font-semibold" : ""
            }`}
          >
            <span className="text-emerald-400 mr-0.5">●</span> Health
          </Link>
          <Link
            to="/cli-session"
            className={`hover:text-[var(--foreground)] transition-colors ${
              location.pathname === "/cli-session" ? "text-[var(--foreground)] font-semibold" : ""
            }`}
          >
            CLI Plugin
          </Link>
          <a
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border hover:bg-[var(--muted)] transition-colors"
          >
            <svg width="28" height="28" viewBox="0 0 380 380" fill="currentColor">
              <path d="M282.83 170.73l-.27-.69-26.14-68.22a6.81 6.81 0 0 0-2.69-3.24 7 7 0 0 0-8 .43 7 7 0 0 0-2.32 3.52l-17.65 54h-71.47l-17.65-54a6.86 6.86 0 0 0-2.32-3.53 7 7 0 0 0-8-.43 6.87 6.87 0 0 0-2.69 3.24L97.44 170l-.26.69a48.54 48.54 0 0 0 16.1 56.1l.09.07.24.17 39.82 29.82 19.7 14.91 12 9.06a8.07 8.07 0 0 0 9.76 0l12-9.06 19.7-14.91 40.06-30 .1-.08a48.56 48.56 0 0 0 16.08-56.04z" />
            </svg>
            GitLab
          </a>
        </div>
      </div>
    </nav>
  );
}
