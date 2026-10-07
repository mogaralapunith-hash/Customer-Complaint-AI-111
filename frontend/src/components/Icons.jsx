const stroke = {
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.7,
  strokeLinecap: "round",
  strokeLinejoin: "round"
};

export function EditIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <path {...stroke} d="M4 20h4l11-11a2.1 2.1 0 0 0-3-3L6 17z" />
      <path {...stroke} d="M13.5 6.5l3 3" />
    </svg>
  );
}

export function PlusIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <path {...stroke} d="M12 5v14M5 12h14" />
    </svg>
  );
}

export function ImageIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <rect {...stroke} x="3" y="4" width="18" height="16" rx="2" />
      <circle {...stroke} cx="8.5" cy="9.5" r="1.5" />
      <path {...stroke} d="M21 15l-5-5-9 9" />
    </svg>
  );
}

export function TruckIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <path {...stroke} d="M2 6h11v10H2z" />
      <path {...stroke} d="M13 9h4l3 3v4h-7" />
      <circle {...stroke} cx="6.5" cy="17.5" r="1.8" />
      <circle {...stroke} cx="16.5" cy="17.5" r="1.8" />
    </svg>
  );
}

export function CheckIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <path {...stroke} d="M4 12.5l5 5L20 6.5" />
    </svg>
  );
}

export function MailIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <rect {...stroke} x="3" y="5" width="18" height="14" rx="2" />
      <path {...stroke} d="M3 7l9 6 9-6" />
    </svg>
  );
}

export function PhoneIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <path {...stroke} d="M5 4h4l1.5 4.5L8 10a12 12 0 0 0 6 6l1.5-2.5L20 15v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z" />
    </svg>
  );
}

export function ClockIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <circle {...stroke} cx="12" cy="12" r="9" />
      <path {...stroke} d="M12 7v5l3.5 2" />
    </svg>
  );
}

export function SearchIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" {...props}>
      <circle {...stroke} cx="11" cy="11" r="7" />
      <path {...stroke} d="M20 20l-3.2-3.2" />
    </svg>
  );
}

export function CloudIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" {...props}>
      <path {...stroke} d="M6 19a4 4 0 0 1-.7-7.9A6 6 0 0 1 17 10a3.5 3.5 0 0 1 1 9H6z" />
    </svg>
  );
}