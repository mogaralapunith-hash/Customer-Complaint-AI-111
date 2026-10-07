import { useRef, useState } from "react";
import { uploadImage, submitDelivery } from "../lib/api.js";
import { ImageIcon, TruckIcon } from "./Icons";

const TONES = {
  "Damaged Product": { dot: "#f97316", tone: "tone-0" },
  "Late Delivery": { dot: "#3b82f6", tone: "tone-1" },
  "Wrong Item": { dot: "#ec4899", tone: "tone-2" },
  Refund: { dot: "#f59e0b", tone: "tone-3" },
  "Payment Issue": { dot: "#10b981", tone: "tone-4" },
  "General Enquiry": { dot: "#94a3b8", tone: "tone-5" },
  Other: { dot: "#94a3b8", tone: "tone-5" }
};

function UploadCard({ onComplete }) {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [dragging, setDragging] = useState(false);
  const [status, setStatus] = useState("idle");

  const pick = (selected) => {
    if (!selected || !selected.type.startsWith("image/")) {
      onComplete("Please select an image file before uploading.", "error");
      return;
    }
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };

  const onDrop = (event) => {
    event.preventDefault();
    setDragging(false);
    pick(event.dataTransfer.files?.[0]);
  };

  const submit = async (event) => {
    event.preventDefault();
    if (!file) {
      onComplete("Please select an image file before uploading.", "error");
      return;
    }
    setStatus("uploading");
    try {
      const data = await uploadImage(file);
      setStatus("done");
      onComplete(
        "Thank you! Your image has been uploaded successfully. Our support team will verify the product and get back to you within 24 hours.",
        "success",
        file.name
      );
      void data;
    } catch (error) {
      setStatus("idle");
      onComplete(error.message, "error");
    }
  };

  return (
    <section className="card card--action fade-up">
      <div className="card__head">
        <span className="card__icon" aria-hidden="true">
          <ImageIcon />
        </span>
        <div>
          <h2>Upload a photo</h2>
          <p>A clear image helps us verify the product and act faster.</p>
        </div>
      </div>

      <form onSubmit={submit}>
        <div
          className={`dropzone ${dragging ? "is-dragging" : ""} ${preview ? "has-preview" : ""}`}
          onClick={() => inputRef.current?.click()}
          onDragOver={(event) => {
            event.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
          role="button"
          tabIndex={0}
          onKeyDown={(event) => {
            if (event.key === "Enter") inputRef.current?.click();
          }}
        >
          {preview ? (
            <img className="dropzone__preview" src={preview} alt="Uploaded product" />
          ) : (
            <>
              <span className="dropzone__icon" aria-hidden="true">
                <ImageIcon />
              </span>
              <p>
                <strong>Click to choose a photo</strong> or drag it here
              </p>
              <span className="dropzone__hint">PNG, JPG, WEBP or GIF · up to 5 MB</span>
            </>
          )}
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            hidden
            onChange={(event) => pick(event.target.files?.[0])}
          />
        </div>

        {file && <p className="file-name">{file.name} · {(file.size / 1024).toFixed(0)} KB</p>}

        <button className="btn btn--primary btn--block" type="submit" disabled={status !== "idle"}>
          {status === "uploading" ? (
            <>
              <span className="spinner" aria-hidden="true" /> Uploading…
            </>
          ) : status === "done" ? (
            <>Uploaded</>
          ) : (
            <>Send photo</>
          )}
        </button>
      </form>
    </section>
  );
}

function DeliveryCard({ onComplete }) {
  const [orderId, setOrderId] = useState("");
  const [date, setDate] = useState("");
  const [status, setStatus] = useState("idle");

  const submit = async (event) => {
    event.preventDefault();
    setStatus("sending");
    try {
      const data = await submitDelivery(orderId, date);
      setStatus("done");
      onComplete(
        "Thank you. Your delivery details have been received. Our support team will check your shipment and provide an update within 24 hours.",
        "success",
        `Order ID ${data.orderId} · Expected ${data.deliveryDate}`
      );
    } catch (error) {
      setStatus("idle");
      onComplete(error.message, "error");
    }
  };

  return (
    <section className="card card--action fade-up">
      <div className="card__head">
        <span className="card__icon" aria-hidden="true">
          <TruckIcon />
        </span>
        <div>
          <h2>Delivery details</h2>
          <p>Share your order number so we can check its status.</p>
        </div>
      </div>

      <form onSubmit={submit} className="stack">
        <label className="field-label" htmlFor="order-id">
          Order ID
        </label>
        <input
          id="order-id"
          className="input"
          type="text"
          placeholder="e.g. ORD-2026-77821"
          value={orderId}
          onChange={(event) => setOrderId(event.target.value)}
          required
        />

        <label className="field-label" htmlFor="delivery-date">
          Expected delivery date
        </label>
        <input
          id="delivery-date"
          className="input"
          type="date"
          value={date}
          onChange={(event) => setDate(event.target.value)}
          required
        />

        <button
          className="btn btn--primary btn--block"
          type="submit"
          disabled={status !== "idle"}
        >
          {status === "sending" ? (
            <>
              <span className="spinner" aria-hidden="true" /> Checking…
            </>
          ) : status === "done" ? (
            <>Sent</>
          ) : (
            <>
              <TruckIcon /> Check delivery
            </>
          )}
        </button>
      </form>
    </section>
  );
}

export default function ResultPanel({ result, onComplete }) {
  const tone = TONES[result.category] || TONES["General Enquiry"];
  const confidence = Math.round(result.confidence * 100);

  const facts = result.facts || {};
  const factChips = [
    ...(facts.orderIds || []).map((value) => ({ label: "Order", value })),
    facts.amount ? { label: "Amount", value: facts.amount } : null,
    facts.product ? { label: "Product", value: facts.product } : null,
    facts.paymentMethod ? { label: "Paid via", value: facts.paymentMethod } : null
  ].filter(Boolean);

  const steps = result.steps || [];
  const recovery = result.recovery || [];
  const alternatives = result.alternatives || [];
  const need = result.needFromYou || [];

  return (
    <div className="results">
      <div className="grid grid--results">
        <section className={`card card--result ${tone.tone} fade-up`}>
          <div className="result__top">
            <span className="result__badge">
              <span className="result__dot" style={{ background: tone.dot }} />
              {result.category}
            </span>
            <span className="result__confidence">{confidence}% confidence</span>
          </div>

          <div className="meter" aria-hidden="true">
            <span style={{ width: `${confidence}%` }} />
          </div>

          {result.summary && <p className="result__summary">{result.summary}</p>}

          {factChips.length > 0 && (
            <div className="fact-chips">
              {factChips.map((chip) => (
                <span key={chip.label + chip.value}>
                  <small>{chip.label}</small>
                  {chip.value}
                </span>
              ))}
            </div>
          )}

          <div className="result__note">
            <h3>What we found</h3>
            <p>{result.analysis}</p>
          </div>
        </section>

        <section className="card card--resolution fade-up">
          <div className="card__head">
            <span className="card__icon" aria-hidden="true">
              <span className="result__dot" style={{ background: tone.dot }} />
            </span>
            <div>
              <h2>Our answer</h2>
              <p>Read from your exact complaint — not a template.</p>
            </div>
          </div>
          <p className="resolution">{result.issue}</p>
        </section>
      </div>

      {(steps.length > 0 || recovery.length > 0 || alternatives.length > 0) && (
        <section className="card card--plan fade-up">
          <div className="plan">
            {steps.length > 0 && (
              <div className="plan__group">
                <h4>What happens next</h4>
                <ol className="plan__steps">
                  {steps.map((step) => (
                    <li key={step}>{step}</li>
                  ))}
                </ol>
              </div>
            )}

            {recovery.length > 0 && (
              <div className="plan__group">
                <h4>Recovery options</h4>
                <ul className="plan__list">
                  {recovery.map((option) => (
                    <li key={option.title}>
                      <strong>{option.title}</strong>
                      <span>{option.detail}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {alternatives.length > 0 && (
              <div className="plan__group">
                <h4>Alternatives</h4>
                <ul className="plan__list plan__list--plain">
                  {alternatives.map((alt) => (
                    <li key={alt}>{alt}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {result.timeline && (
            <p className="plan__timeline">
              <strong>Timeline:</strong> {result.timeline}
            </p>
          )}

          {need.length > 0 && (
            <div className="plan__need">
              <strong>What we need from you</strong>
              <div className="fact-chips">
                {need.map((item) => (
                  <span key={item}>{item}</span>
                ))}
              </div>
            </div>
          )}
        </section>
      )}

      {result.showUpload && <UploadCard onComplete={onComplete} />}
      {result.showDeliveryForm && <DeliveryCard onComplete={onComplete} />}
    </div>
  );
}