import { useState } from "react";
import { EditIcon, SearchIcon } from "./Icons";

const MAX_LENGTH = 600;

const SAMPLES = [
  "My product arrived damaged and the box was crushed",
  "My order is late and has not arrived yet",
  "I received the wrong item instead of the phone I ordered",
  "I want a refund for my order",
  "My payment failed but money was deducted"
];

export default function ComplaintForm({ onSubmit, loading }) {
  const [complaint, setComplaint] = useState("");

  const submit = (event) => {
    event.preventDefault();
    if (!complaint.trim() || loading) return;
    onSubmit(complaint.trim());
  };

  return (
    <form className="card analyzer" id="analyzer" onSubmit={submit}>
      <div className="card__head">
        <span className="card__icon" aria-hidden="true">
          <EditIcon />
        </span>
        <div>
          <h2>Tell us what happened</h2>
          <p>
            Describe the problem in your own words — the model classifies it
            and suggests the next step.
          </p>
        </div>
      </div>

      <label className="field-label" htmlFor="complaint">
        Your complaint
      </label>

      <textarea
        id="complaint"
        className="textarea"
        placeholder="Example: My product arrived damaged and the courier refused to help…"
        value={complaint}
        maxLength={MAX_LENGTH}
        onChange={(event) => setComplaint(event.target.value)}
        disabled={loading}
      />

      <div className="textarea__meta">
        <div className="chips">
          {SAMPLES.map((sample) => (
            <button
              key={sample}
              type="button"
              className="chip"
              onClick={() => setComplaint(sample)}
              disabled={loading}
            >
              {sample}
            </button>
          ))}
        </div>
        <span className="counter">
          {complaint.length}/{MAX_LENGTH}
        </span>
      </div>

      <button
        className="btn btn--primary btn--block"
        type="submit"
        disabled={loading || !complaint.trim()}
      >
        {loading ? (
          <>
            <span className="spinner" aria-hidden="true" /> Classifying…
          </>
        ) : (
          <>
            <SearchIcon /> Analyze complaint
          </>
        )}
      </button>
    </form>
  );
}