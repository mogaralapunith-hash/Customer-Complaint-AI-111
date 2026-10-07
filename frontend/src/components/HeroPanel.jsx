import { useEffect, useRef, useState } from "react";
import { analyzeComplaint, CATEGORIES } from "../lib/classifier.js";

const SAMPLES = [
  "My order is5 days late and still not delivered",
  "The phone I received has a cracked screen",
  "You sent me the wrong product, I ordered headphones",
  "Money was deducted but my payment failed",
  "I want a refund for my order"
];

const TYPE_MS = 34;
const HOLD_MS = 3400;

export default function HeroPanel() {
  const [sampleIndex, setSampleIndex] = useState(0);
  const [typed, setTyped] = useState("");
  const [phase, setPhase] = useState("typing");
  const timerRef = useRef(null);

  const full = SAMPLES[sampleIndex];
  const result = analyzeComplaint(full);

  useEffect(() => {
    clearTimeout(timerRef.current);

    if (phase === "typing") {
      if (typed.length < full.length) {
        timerRef.current = setTimeout(
          () => setTyped(full.slice(0, typed.length + 1)),
          TYPE_MS
        );
        return () => clearTimeout(timerRef.current);
      }
      timerRef.current = setTimeout(() => setPhase("result"), 320);
      return () => clearTimeout(timerRef.current);
    }

    timerRef.current = setTimeout(() => {
      setSampleIndex((index) => (index + 1) % SAMPLES.length);
      setTyped("");
      setPhase("typing");
    }, HOLD_MS);
    return () => clearTimeout(timerRef.current);
  }, [typed, phase, sampleIndex, full.length]);

  const confidence = Math.round(result.confidence * 100);
  const activeIndex = CATEGORIES.indexOf(result.category);

  return (
    <div className="hero__panel">
      <div className="panel__bar">
        <span className="panel__dots" aria-hidden="true">
          <i /><i /><i />
        </span>
        <span className="panel__title">complaint-analyzer.ai</span>
        <span className="panel__live">
          <i /> live
        </span>
      </div>

      <p className="panel__label">Customer message</p>
      <p className={`panel__text ${phase === "typing" ? "is-typing" : ""}`}>
        {typed || "\u00a0"}
      </p>

      <div className="panel__chips">
        {CATEGORIES.map((category, index) => (
          <span
            key={category}
            className={`panel__chip ${
              phase === "result" && index === activeIndex ? "is-active" : ""
            }`}
          >
            {category}
          </span>
        ))}
      </div>

      <div className="panel__result">
        <div className="panel__result-top">
          <strong>
            {phase === "result" ? result.category : "Analyzing…"}
          </strong>
          <span className="panel__conf">
            {phase === "result" ? `${confidence}% confidence` : ""}
          </span>
        </div>
        <div className="panel__meter">
          <span style={{ width: phase === "result" ? `${confidence}%` : "0%" }} />
        </div>
        <p className="panel__next">
          <b>Next step: </b>
          {phase === "result"
            ? result.issue.split(". ").slice(0, 2).join(". ") + "."
            : "Reading the message and matching it to a support category…"}
        </p>
      </div>

      <div className="panel__foot">
        <span>TF-IDF</span>
        <span>Linear SVM</span>
        <span>5 classes</span>
      </div>
    </div>
  );
}
