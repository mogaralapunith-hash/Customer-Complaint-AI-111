import { useEffect, useState } from "react";
import Navbar from "./components/Navbar.jsx";
import ComplaintForm from "./components/ComplaintForm.jsx";
import ResultPanel from "./components/ResultPanel.jsx";
import { About, Contact, Footer } from "./components/Sections.jsx";
import { fetchPrediction } from "./lib/api.js";
import HeroPanel from "./components/HeroPanel.jsx";
import { CloudIcon } from "./components/Icons.jsx";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    if (!toast) return undefined;
    const timer = window.setTimeout(() => setToast(null), 4800);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const handleAnalyze = async (complaint) => {
    setLoading(true);
    setResult(null);
    try {
      const data = await fetchPrediction(complaint);
      setResult(data);
      window.setTimeout(() => {
        document
          .getElementById("results")
          ?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 80);
    } catch (error) {
      setToast({ message: error.message, type: "error", id: Date.now() });
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = (message, type = "success", detail = "") => {
    setToast({ message, type, detail, id: Date.now() });
  };

  return (
    <div className="app" id="top">
      <Navbar />

      <section className="hero">
        <div className="hero__bg" aria-hidden="true">
          <span className="hero__grid" />
          <span className="hero__orb hero__orb--1" />
          <span className="hero__orb hero__orb--2" />
          <span className="hero__orb hero__orb--3" />
        </div>

        <div className="hero__inner">
          <div className="hero__copy">
            <span className="eyebrow">AI-powered support desk</span>
            <h1>
              Complaints handled <em>clearly</em>, quickly
            </h1>
            <p>
              Describe what went wrong and let the model pick the category and
              the right next step — no menus, no phone trees.
            </p>

            <div className="hero__actions">
              <a className="btn btn--light" href="#analyzer">
                Analyze a complaint
              </a>
              <a className="btn btn--outline-light" href="#how-it-works">
                How it works
              </a>
            </div>

            <div className="hero__stats">
              <div>
                <strong>5</strong>
                <span>complaint categories</span>
              </div>
              <div>
                <strong>40+</strong>
                <span>training samples</span>
              </div>
              <div>
                <strong>&lt;1s</strong>
                <span>to classify</span>
              </div>
            </div>
          </div>

          <HeroPanel />
        </div>
      </section>

      <main className="shell">
        <ComplaintForm onSubmit={handleAnalyze} loading={loading} />

        <div id="results" className="results-anchor">
          {loading && (
            <div className="results">
              {[0, 1].map((item) => (
                <div className="card skeleton" key={item}>
                  <span className="skeleton__line skeleton__line--short" />
                  <span className="skeleton__line" />
                  <span className="skeleton__line skeleton__line--mid" />
                </div>
              ))}
            </div>
          )}

          {!loading && result && (
            <ResultPanel result={result} onComplete={handleComplete} />
          )}

          {!loading && !result && (
            <div className="empty card">
              <span className="empty__mark" aria-hidden="true">
                <CloudIcon />
              </span>
              <p>
                Your prediction and suggested next step will appear here after
                you analyze a complaint.
              </p>
            </div>
          )}
        </div>

        <About />
        <Contact />
      </main>

      <Footer />

      {toast && (
        <div className={`toast toast--${toast.type}`} role="status">
          <div>
            <p>{toast.message}</p>
            {toast.detail && <small>{toast.detail}</small>}
          </div>
          <button aria-label="Dismiss" onClick={() => setToast(null)}>
            ✕
          </button>
        </div>
      )}
    </div>
  );
}