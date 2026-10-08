import { MailIcon, PhoneIcon, ClockIcon } from "./Icons";

const CATEGORIES = [
  { tone: "#cc6b43", title: "Damaged Product", text: "Broken, cracked or damaged items verified with a photo." },
  { tone: "#2f6fae", title: "Late Delivery", text: "Shipment tracked with your order ID and expected date." },
  { tone: "#b25c71", title: "Wrong Item", text: "Incorrect products replaced after a quick verification." },
  { tone: "#c08e2e", title: "Refund", text: "Refund status explained with the exact settlement timeline." },
  { tone: "#5f8f76", title: "Payment Issue", text: "Failed or duplicate charges verified with a transaction ID." }
];

const STEPS = [
  { title: "Describe", text: "Write your complaint in plain language — no forms to fill out." },
  { title: "Classify", text: "The model reads the text and picks the closest support category." },
  { title: "Resolve", text: "You get the right next step and the exact form you need." }
];

export function About() {
  return (
    <section className="section" id="how-it-works">
      <div className="section__head">
        <span className="eyebrow">Under the hood</span>
        <h2>How the complaint desk works</h2>
        <p>
          A small machine-learning pipeline that reads a complaint, picks a
          support category and suggests the fastest way to fix it.
        </p>
      </div>

      <div className="grid grid--steps">
        {STEPS.map((step, index) => (
          <article className="info-card" key={step.title}>
            <span className="info-card__num" aria-hidden="true">
              0{index + 1}
            </span>
            <h3>{step.title}</h3>
            <p>{step.text}</p>
          </article>
        ))}
      </div>

      <div className="grid grid--categories">
        {CATEGORIES.map((category) => (
          <article className="category-card" key={category.title}>
            <span
              className="result__dot"
              aria-hidden="true"
              style={{ background: category.tone }}
            />
            <div>
              <h3>{category.title}</h3>
              <p>{category.text}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export function Contact() {
  const items = [
    {
      icon: <MailIcon />,
      title: "Email us",
      value: "mogaralapunith@gmail.com",
      href: "mailto:mogaralapunith@gmail.com"
    },
    {
      icon: <PhoneIcon />,
      title: "Call us",
      value: "7075272498",
      href: "tel:+917075272498"
    },
    { icon: <ClockIcon />, title: "Support hours", value: "24/7" }
  ];

  return (
    <section className="section" id="contact">
      <div className="section__head">
        <span className="eyebrow">Talk to a human</span>
        <h2>Prefer a real person?</h2>
        <p>
          Our support team is one message away and will pick up any open
          complaint from here.
        </p>
      </div>

      <div className="grid grid--contact">
        {items.map((item) => (
          <article className="info-card" key={item.title}>
            <span className="card__icon" aria-hidden="true">
              {item.icon}
            </span>
            <h3>{item.title}</h3>
            {item.href ? (
              <p>
                <a className="contact__link" href={item.href}>
                  {item.value}
                </a>
              </p>
            ) : (
              <p>{item.value}</p>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}

export function Footer() {
  return (
    <footer className="footer">
      <p className="footer__credit">
        <span className="footer__by">Developed by</span>
        <strong className="footer__name">Mogarala Punith Sai</strong>
      </p>
      <p className="footer__meta">
        Customer Complaint AI · powered by scikit-learn + Flask + React
      </p>
    </footer>
  );
}