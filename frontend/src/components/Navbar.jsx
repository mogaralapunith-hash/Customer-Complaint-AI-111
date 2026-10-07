import { useEffect, useState } from "react";

const LINKS = [
  { href: "#analyzer", label: "Analyze" },
  { href: "#how-it-works", label: "How it works" },
  { href: "#contact", label: "Contact" }
];

function BrandMark() {
  return (
    <svg className="brand-mark" viewBox="0 0 40 40" width="40" height="40" aria-hidden="true">
      <circle cx="20" cy="20" r="19" fill="#2f6fae" />
      <path
        d="M10.5 21.5c0-2.4 1.9-4.3 4.3-4.3a5.2 5.2 0 0 1 9.7-.9c.3-.1.6-.1.9-.1 2.4 0 4.3 1.8 4.3 4.2"
        stroke="#fffdf8"
        strokeWidth="1.7"
        strokeLinecap="round"
        fill="none"
      />
      <path d="M15 21.5h11" stroke="#fffdf8" strokeWidth="1.7" strokeLinecap="round" />
      <circle cx="24" cy="25.5" r="2.1" fill="#ffd97a" />
    </svg>
  );
}

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 30);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className={`navbar ${scrolled ? "navbar--scrolled" : ""}`}>
      <a className="logo" href="#top" onClick={() => setOpen(false)}>
        <BrandMark />
        <span className="logo__text">
          Customer Complaint <strong>AI</strong>
        </span>
      </a>

      <button
        className={`navbar__toggle ${open ? "is-open" : ""}`}
        aria-label="Toggle navigation"
        aria-expanded={open}
        onClick={() => setOpen((value) => !value)}
      >
        <span />
        <span />
        <span />
      </button>

      <nav className={`nav-links ${open ? "is-open" : ""}`}>
        {LINKS.map((link) => (
          <a key={link.href} href={link.href} onClick={() => setOpen(false)}>
            {link.label}
          </a>
        ))}
        <a
          className="btn btn--primary btn--small"
          href="#analyzer"
          onClick={() => setOpen(false)}
        >
          Analyze complaint
        </a>
      </nav>
    </header>
  );
}