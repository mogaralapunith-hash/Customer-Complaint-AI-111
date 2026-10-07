"""Deep complaint analysis engine.

Reads a free-form customer complaint, extracts concrete facts from it
(order IDs, amounts, products, payment methods, dates, urgency) and
composes a complete, actionable answer: what we found, what happens
next, recovery options, alternatives, timeline and what we still need.
"""

import re

# ============================================================
# CATEGORIES
# ============================================================

CATEGORIES = [
    "Damaged Product",
    "Late Delivery",
    "Wrong Item",
    "Refund",
    "Payment Issue",
]

GENERAL = "General Enquiry"

# ============================================================
# INTENT LEXICON  (phrase, weight)
# ============================================================

LEXICON = {
    "Damaged Product": [
        ("damaged", 3), ("damage", 3), ("broken", 3), ("break", 2),
        ("crack", 3), ("cracked", 3), ("shattered", 3), ("smashed", 3),
        ("crushed", 3), ("dented", 3), ("bent", 2), ("scratched", 2),
        ("torn", 2), ("ripped", 2), ("leaking", 2), ("leak", 2),
        ("defective", 3), ("faulty", 3), ("not working", 3),
        ("stopped working", 3), ("doesn't work", 3), ("does not work", 3),
        ("won't turn on", 3), ("wont turn on", 3), ("dead on arrival", 4),
        ("not turning on", 3), ("in pieces", 3), ("pieces", 2),
        ("unusable", 3), ("useless", 2), ("broken screen", 4),
        ("screen broke", 4), ("screen is broken", 4), ("screen shattered", 4),
        ("arrived damaged", 5), ("came damaged", 4), ("received damaged", 4),
        ("product is broken", 5), ("item is broken", 5), ("box was crushed", 4),
        ("packaging damaged", 4), ("poor condition", 3), ("bad condition", 3),
        ("in bad shape", 3), ("damaged in transit", 5), ("broken in transit", 4),
        ("threw", 3), ("thrown", 3), ("flung", 3), ("dropped", 2),
        ("dented in transit", 4), ("crushed in transit", 4),
        ("battery swollen", 3), ("battery drain", 2), ("overheating", 2),
        ("malfunction", 3), ("malfunctioning", 3), ("spoiled", 2),
        ("rotten", 2), ("expired", 2), ("missing parts", 3),
        ("parts missing", 3), ("scratch", 2), ("dent", 3),
        ("falling apart", 3), ("came apart", 3), ("handle broke", 4),
        ("glass broke", 4), ("glass cracked", 4), ("screen broke", 4),
        ("doa", 4), ("not as described", 2), ("poor quality", 2),
        ("cheap quality", 2), ("build quality", 1),         ("wobble", 1), ("snapped", 3), ("snap", 2), ("dead", 2),
        ("not charging", 3), ("wont charge", 3), ("won't charge", 3),
        ("bricked", 3), ("stopped charging", 3), ("wobbles", 2),
        ("tut gaya", 5), ("toot gaya", 5), ("kharab ho gaya", 5),
        ("damage ho gaya", 5), ("toot gaya hai", 5),
        ("loose", 1), ("tilted", 1), ("misaligned", 2), ("noisy", 1),
    ],
    "Late Delivery": [
        ("late", 3), ("delayed", 3), ("delay", 3), ("overdue", 3),
        ("not arrived", 5), ("has not arrived", 5), ("hasn't arrived", 5),
        ("didn't arrive", 5), ("did not arrive", 5), ("never arrived", 5),
        ("not received", 5), ("haven't received", 5), ("hasn't received", 5),
        ("not delivered", 5), ("undelivered", 4), ("still waiting", 4),
        ("where is my order", 5), ("where is my parcel", 5),
        ("order not came", 4), ("not come yet", 4), ("no delivery", 4),
        ("delivery pending", 4), ("shipment is stuck", 4), ("parcel stuck", 4),
        ("package stuck", 4), ("in transit", 3), ("out for delivery", 2),
        ("expected delivery date has passed", 5), ("expected date passed", 5),
        ("delivery date passed", 5), ("past the delivery date", 5),
        ("no delivery updates", 4), ("tracking not updated", 4),
        ("tracking is not updating", 4), ("no updates", 3),
        ("my parcel is missing", 5), ("package missing", 5),
        ("order missing", 5), ("lost package", 5), ("lost parcel", 5),
        ("parcel lost", 5), ("order lost", 5), ("never showed up", 5),
        ("not shown up", 5), ("still not", 3), ("taking too long", 4),
        ("too long", 3), ("taking forever", 4), ("days late", 4),
        ("week late", 4), ("shipped", 1), ("dispatch", 2), ("courier", 2),
        ("delivery boy", 2), ("rider", 1), ("logistics", 2),
        ("shipping", 2), ("transit", 2), ("undelivered", 4),
        ("not yet delivered", 5), ("order is stuck", 4),
        ("delivery is late", 5), ("arrived late", 4), ("came late", 4),
        ("one week late", 5), ("still not delivered", 5),
        ("not yet reached", 4), ("fake delivery", 4), ("showing fake", 4),
        ("delivery attempt", 2), ("reschedule delivery", 3),
        ("change delivery", 2), ("deliver fast", 2), ("when will it arrive", 4),
        ("when will i get my order", 5),
        ("tracking has not moved", 5), ("has not moved", 4),
        ("no movement", 4), ("not moved", 4), ("tracking", 2),
        ("abhi tak nahi aaya", 6), ("order nahi aaya", 5),
        ("parcel nahi mila", 6), ("delivery nahi hui", 5),
        ("kab tak aayega", 4), ("deliver nahi hua", 5),
    ],
    "Wrong Item": [
        ("wrong item", 5), ("wrong product", 5), ("wrong order", 5),
        ("incorrect item", 5), ("incorrect product", 5),
        ("different product", 5), ("different item", 5),
        ("not what i ordered", 5), ("not what i expected", 4),
        ("not what i wanted", 4), ("something else", 4),
        ("someone else", 4), ("received the wrong", 5),
        ("sent the wrong", 5), ("shipped the wrong", 5),
        ("instead of", 3), ("you sent me", 3), ("mixed up", 4),
        ("but got", 4), ("got the wrong", 4), ("delivered the wrong", 4),
        ("received a different", 4), ("send the wrong", 4),
        ("size does not fit", 3), ("did not match", 4),
        ("you sent", 4), ("you have sent", 4), ("sent me", 3),
        ("received the basic", 4), ("not the model i asked", 5),
        ("mismatch", 3), ("colour is different", 4), ("color is different", 4),
        ("size is wrong", 4), ("size mismatch", 4), ("wrong size", 4),
        ("wrong colour", 4), ("wrong color", 4), ("received something else", 5),
        ("got someone else order", 5), ("duplicate item", 3),
        ("extra item", 2), ("item is not what", 5),
        ("ordered a", 2), ("ordered the", 2), ("but received", 5),
        ("received instead", 4), ("swapped", 3), ("exchange wrong", 4),
        ("not the one i ordered", 5), ("is incorrect", 4),
        ("they sent", 3), ("delivery is wrong", 4),
    ],
    "Refund": [
        ("refund", 5), ("refunded", 5), ("refunding", 4),
        ("money back", 5), ("moneyback", 5), ("return my money", 5),
        ("give my money", 5), ("my money back", 5), ("get my money", 4),
        ("reimburse", 5), ("reimbursement", 4), ("reverse the payment", 4),
        ("cancel my order", 3), ("cancel the order", 3),
        ("cancel and refund", 5), ("want to return", 4),
        ("return the product", 4), ("return item", 4),
        ("return it", 3), ("send back", 3), ("give back", 3),
        ("credit back", 4), ("credited back", 4), ("amount back", 4),
        ("sum refunded", 4), ("when will i get refund", 5),
        ("refund status", 5), ("refund my amount", 5),
        ("please refund", 5), ("need a refund", 5), ("refund please", 5),
        ("how do i get my refund", 5), ("refund not received", 5),
        ("no refund", 5), ("still no refund", 5), ("refund my money", 5),
        ("money not returned", 5), ("amount not refunded", 5),
        ("want my amount", 4), ("return and refund", 5),
        ("not satisfied", 2), ("want to give back", 4),
        ("take it back", 3), ("reverse", 2), ("chargeback", 4),
        ("charge back", 4),
        ("money not credited", 6), ("not credited", 5), ("credited", 3),
        ("money wapas", 6), ("paisa wapas", 6), ("rupay wapas", 5),
        ("wapas chahiye", 6), ("refund kar", 5), ("cancel kar do", 5),
        ("paisa do", 4), ("refund nahi mila", 6), ("money nahi mila", 5),
        ("return delivered", 3), ("return kar diya", 4),
    ],
    "Payment Issue": [
        ("payment failed", 5), ("payment issue", 5),
        ("payment problem", 5), ("payment not working", 5),
        ("payment is failed", 5), ("payment stuck", 5),
        ("transaction failed", 5), ("transaction pending", 5),
        ("payment pending", 5), ("payment was not successful", 5),
        ("money deducted", 5), ("money was deducted", 5),
        ("amount deducted", 5), ("amount was debited", 5),
        ("debited but", 5), ("debited without", 5), ("charged twice", 5),
        ("charged thrice", 5), ("charged multiple times", 5),
        ("double charged", 5), ("multiple times", 4),
        ("card was charged", 5), ("card charged", 5),
        ("money taken", 5), ("amount taken", 5), ("payment deducted", 5),
        ("payment not received", 5), ("paid but no order", 5),
        ("paid but order not placed", 5), ("order not placed", 5),
        ("did not go through", 5), ("payment did not go through", 5),
        ("upi failed", 5), ("upi pending", 5), ("payment timeout", 5),
        ("payment gateway", 4), ("otp not received", 4),
        ("failed transaction", 5), ("auto debit", 4), ("debit", 3),
        ("deducted", 4), ("debited", 4), ("charged", 3),
        ("payment", 2), ("transaction", 3), ("paid", 2),
        ("billing issue", 4), ("wrong amount", 4), ("extra charge", 4),
        ("hidden charge", 4), ("overcharged", 5), ("emi", 3),
        ("cod", 2), ("failed", 2), ("reflected in statement", 5),
        ("bank statement", 4), ("money gone", 5), ("shows payment failed", 5),
        ("autodebit", 6), ("auto debited", 5), ("auto debit", 4),
        ("payment fail", 5), ("paisa kat gaya", 6), ("payment nahi hua", 5),
        ("amount cut", 5), ("money cut", 5),
    ],
}

# ============================================================
# FACT PATTERNS
# ============================================================

PRODUCTS = [
    "smartphone", "phone", "mobile", "mobile phone", "laptop", "notebook",
    "tablet", "ipad", "headphones", "headset", "earphones", "earbuds",
    "airpods", "speaker", "soundbar", "television", "tv", "monitor",
    "refrigerator", "fridge", "washing machine", "microwave", "dishwasher",
    "air conditioner", "ac", "cooler", "heater", "geyser", "blender",
    "mixer grinder", "grinder", "mixer", "juicer", "kettle", "iron",
    "vacuum cleaner", "water purifier", "ro system", "inverter", "fan",
    "watch", "smartwatch", "camera", "lens", "drone", "console",
    "playstation", "xbox", "nintendo", "keyboard", "mouse", "headset",
    "charger", "power bank", "adapter", "cable", "hard disk", "ssd",
    "pendrive", "memory card", "router", "printer", "scanner", "projector",
    "shoes", "sneakers", "sandals", "boots", "shirt", "t-shirt", "tshirt",
    "dress", "jacket", "jeans", "trousers", "kurta", "saree", "sweater",
    "watch strap", "bag", "backpack", "wallet", "belt", "sunglasses",
    "perfume", "makeup kit", "lipstick", "cream", "serum", "medicine",
    "supplements", "protein", "toy", "stroller", "baby seat", "mattress",
    "pillow", "sofa", "chair", "table", "wardrobe", "book", "novel",
    "furniture", "lamp", "curtain", "carpet", "helmet", "cycle", "treadmill",
    "dumbbell", "guitar", "speaker stand", "gas cylinder", "cylinder",
    "bottle", "flask", "lunch box", "cookware", "knife set", "induction",
    "otg", "printer cartridge", "toner", "cartridge",
]

PAYMENT_METHODS = [
    "upi", "gpay", "google pay", "phonepe", "paytm", "amazon pay",
    "credit card", "debit card", "visa", "mastercard", "rupay", "card",
    "net banking", "netbanking", "bank transfer", "neft", "imps",
    "cash on delivery", "cod", "paypal", "apple pay", "emi",
    "bajaj fintech", "wallet",
]

URGENCY_WORDS = [
    "furious", "angry", "frustrated", "disappointed", "annoyed", "upset",
    "unacceptable", "worst", "terrible", "horrible", "pathetic", "ridiculous",
    "still not", "again", "third time", "second time", "multiple times",
    "every time", "always", "never again", "urgent", "asap", "immediately",
    "right away", "escalate", "supervisor", "manager", "consumer court",
    "legal action", "chargeback", "twitter", "social media", "post online",
    "review", "complain to", "harassment", "ignored",
    "no response", "no one replied", "chatbot", "call center", "cheated",
    "fraud", "scam", "looted", "cheat", "worst service", "poor service",
    "totally disappointed", "fed up", "tired of", "help me", "please help",
]

REPEAT_WORDS = [
    "again", "second time", "third time", "multiple times", "every time",
    "repeatedly", "still", "no response", "no one replied", "ignored",
    "yet", "again and again",
]

ORDER_PATTERNS = [
    r"\b(ORD[-\s]?\d+(?:[-\s]\d+)*)\b",
    r"\b(?:order\s*(?:id|no|number|num)?\s*[:#\-]?\s*)([A-Za-z]{0,4}[-\s]?\d{3,}(?:[-\s]\d+)*)\b",
    r"\b(order\s*[#\-]?\s*\d{4,})\b",
    r"\b(#\d{5,})\b",
]

AMOUNT_PATTERN = re.compile(
    r"(?:₹|rs\.?|inr|\$|usd|€|eur)\s?(\d[\d,]*(?:\.\d{1,2})?)"
    r"|\b(\d[\d,]*(?:\.\d{1,2})?)\s?(?:rupees|inr|dollars|USD)\b",
    re.IGNORECASE,
)

DATE_PATTERNS = [
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b",
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?\b",
    r"\b(?:yesterday|today|last week|last month|two days ago|three days ago|"
    r"a week ago|since monday|since friday|past \d+ days|since \d+ days)\b",
]

MONTHS = "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"

EMOJI_MAP = {
    "😡": "angry", "🤬": "angry", "😤": "frustrated", "😠": "angry",
    "😭": "upset", "😢": "upset", "😞": "disappointed", "👎": "disappointed",
    "✅": "ok", "⚠️": "warning",
}


def _phrase_hit(text, phrase):
    parts = [re.escape(p) for p in phrase.split()]
    pattern = r"\b" + r"[\s\-]+".join(parts) + r"s?\b"
    return re.search(pattern, text) is not None


# ============================================================
# FACT EXTRACTION
# ============================================================

def extract_facts(text):
    raw = text
    text = text.lower()

    facts = {
        "order_ids": [],
        "amount": None,
        "dates": [],
        "product": None,
        "payment_method": None,
        "urgency": False,
        "repeat": False,
        "emotion": None,
        "asking_for_photo": False,
        "tracking": False,
        "delivery_mentioned": False,
        "missing_info": [],
    }

    upper = raw

    for pattern in ORDER_PATTERNS:
        for match in re.finditer(pattern, upper, re.IGNORECASE):
            value = match.group(1) if match.lastindex else match.group(0)
            value = value.strip(" ,.;:")
            if value and value.lower() not in {
                v.lower() for v in facts["order_ids"]
            }:
                facts["order_ids"].append(value)

    amount_match = AMOUNT_PATTERN.search(raw)
    if amount_match:
        number = amount_match.group(1) or amount_match.group(2)
        if number:
            symbol = "₹" if re.search(r"₹|rs\.?|inr|rupees", raw, re.I) else "$"
            facts["amount"] = f"{symbol}{number}"

    for pattern in DATE_PATTERNS:
        for match in re.finditer(pattern, text):
            facts["dates"].append(match.group(0))
    if re.search(r"\b" + MONTHS + r"+\s+\d{1,2}", text):
        facts["dates"].append("stated date")

    for product in PRODUCTS:
        if re.search(r"\b" + re.escape(product) + r"\b", text):
            facts["product"] = product
            break

    for method in PAYMENT_METHODS:
        if re.search(r"\b" + re.escape(method) + r"\b", text):
            facts["payment_method"] = method
            break

    facts["urgency"] = any(w in text for w in URGENCY_WORDS) or any(
        e in raw for e in EMOJI_MAP
    )
    facts["repeat"] = any(w in text for w in REPEAT_WORDS)
    facts["asking_for_photo"] = bool(
        re.search(r"\b(photo|picture|screenshot|image|video|attach)\w*\b", text)
    )
    facts["tracking"] = bool(
        re.search(r"\b(tracking|track|awb|waybill|shipment id)\b", text)
    )
    facts["delivery_mentioned"] = bool(
        re.search(
            r"\b(delivery|delivered|parcel|package|shipment|courier|order)\b",
            text,
        )
    )

    if re.search(r"\b(angry|furious|mad|rage)\b", text):
        facts["emotion"] = "angry"
    elif re.search(r"\b(disappointed|sad|upset|let down)\b", text):
        facts["emotion"] = "disappointed"
    elif re.search(r"\b(frustrated|annoyed|irritated|fed up)\b", text):
        facts["emotion"] = "frustrated"

    if not facts["order_ids"] and facts["delivery_mentioned"]:
        facts["missing_info"].append("Order ID")
    if not facts["amount"] and ("refund" in text or "charged" in text):
        facts["missing_info"].append("amount / transaction reference")
    if not facts["product"]:
        facts["missing_info"].append("product name")

    return facts


# ============================================================
# INTENT SCORING
# ============================================================

def score_intents(text):
    text = text.lower()
    scores = {}
    hits = {}

    for category, phrases in LEXICON.items():
        total = 0
        matched = []
        for phrase, weight in phrases:
            if _phrase_hit(text, phrase):
                total += weight
                matched.append(phrase)
        scores[category] = total
        hits[category] = matched

    return scores, hits


def decide_category(text, model_category=None, model_confidence=0.0):
    scores, hits = score_intents(text)

    if sum(scores.values()) <= 0:
        return GENERAL, 0.3, scores, hits

    if model_category in scores:
        bonus = 1.0 + 2.5 * float(model_confidence or 0.0)
        scores[model_category] = scores.get(model_category, 0) + bonus

    best = max(scores, key=lambda key: scores[key])
    best_score = scores[best]

    if best_score <= 0:
        return GENERAL, 0.25, scores, hits

    ordered = sorted(scores.values(), reverse=True)
    margin = ordered[0] - (ordered[1] if len(ordered) > 1 else 0)

    keyword_confidence = min(0.97, 0.55 + 0.06 * best_score + 0.04 * margin)
    if model_category == best:
        keyword_confidence = max(
            keyword_confidence, min(0.97, 0.6 + 0.4 * float(model_confidence or 0))
        )

    return best, round(keyword_confidence, 3), scores, hits


def should_show_upload(category, facts, text):
    text = text.lower()
    if category in ("Damaged Product", "Wrong Item", "Payment Issue"):
        return True
    return facts["asking_for_photo"]


def should_show_delivery_form(category, facts, text):
    if category == "Late Delivery":
        return True
    text = text.lower()
    if category in ("Refund", GENERAL) and facts["delivery_mentioned"]:
        return bool(re.search(r"\b(late|not arrived|delayed|missing|stuck)\b", text))
    return False


# ============================================================
# RESPONSE COMPOSER
# ============================================================

def _reference(facts):
    bits = []
    if facts["order_ids"]:
        bits.append(f"order {facts['order_ids'][0]}")
    if facts["amount"]:
        bits.append(f"worth {facts['amount']}")
    if not bits:
        return ""
    return " for " + ", ".join(bits)


def _opening(facts, empathy=True):
    lines = []
    if empathy and facts["urgency"]:
        if facts["repeat"]:
            lines.append(
                "I can see this has happened more than once and nobody got back "
                "to you — that is not the experience we want you to have, and "
                "I am treating this as a priority case."
            )
        else:
            lines.append(
                "I understand this is urgent for you, and I am handling it as a "
                "priority case right now."
            )
    elif facts["emotion"] in ("angry", "frustrated"):
        lines.append(
            "I hear the frustration in your message — you are right to expect "
            "better, so here is exactly what happens next."
        )
    elif facts["emotion"] == "disappointed":
        lines.append(
            "I am sorry this fell short of what you expected. Let me lay out "
            "how we make it right."
        )
    return " ".join(lines)


def _repeat_note(facts):
    if facts["repeat"]:
        return (
            " Because this is a repeat issue, a goodwill voucher will also be "
            "added to your account once the case is confirmed."
        )
    return ""


def _damaged(facts):
    item = facts["product"] or "item"
    ref = _reference(facts)
    opening = _opening(facts)

    issue = (
        f"{opening}Your {item} arriving damaged{ref} is covered by our damage "
        "protection policy — you do not have to prove anyone was at fault. "
        "You can choose a free replacement or a full refund, and we will "
        "arrange a doorstep pickup of the damaged piece, so you never have to "
        "visit a store or ship anything yourself. "
        f"Send one clear photo of the damage (and the box if you still have it) "
        f"and the claim is opened immediately.{_repeat_note(facts)}"
    )

    return {
        "summary": f"Damaged {item}{ref} — replacement or full refund available",
        "issue": issue,
        "analysis": (
            f"Your {item} reached you in a damaged state, which normally happens "
            "when the parcel is mishandled in transit or dropped at the hub. "
            "Since the item was already damaged on arrival, the cause does not "
            "work against you: anything that arrives broken is replaced or "
            "refunded in full. The photo you send is only used to log the "
            "condition and release the replacement — it is not a hurdle."
        ),
        "steps": [
            "Upload 1–2 clear photos of the damage and the outer packaging.",
            "Our quality team reviews the photos within 4 working hours and approves the claim.",
            "Tell us your choice — replacement or refund — in the same thread.",
            "We book a free doorstep pickup of the damaged item (no cost to you).",
            "Replacement is dispatched the same day, or the refund is initiated immediately.",
        ],
        "recovery": [
            {
                "title": "Free replacement",
                "detail": "Dispatched within 24 hours of approval, delivered in 2–3 days at no extra cost.",
            },
            {
                "title": "Full refund",
                "detail": "Credited back to your original payment method in 3–5 business days.",
            },
            {
                "title": "Repair covered",
                "detail": "For manufacturing defects we can send a technician or repair it at an authorised centre, free of charge.",
            },
            {
                "title": "Doorstep pickup",
                "detail": "The damaged piece is collected from your address — you do not ship it back.",
            },
        ],
        "alternatives": [
            "Keep the item with a partial refund (up to 30% of order value) if the damage is minor.",
            "Exchange it for a different colour, model or variant — you only pay the price difference.",
            "Cancel this order and reorder with express shipping at no extra charge.",
            "Upgrade to a higher model and pay only the difference in price.",
        ],
        "timeline": (
            "Photo verification: ~4 hours · Replacement dispatched: within 24 hours · "
            "Refund credited: 3–5 business days · Pickup: next working day."
        ),
        "need": _need(facts, ["Photo of the damaged item", "Photo of the packaging"]),
        "priority": "High" if facts["urgency"] else "Normal",
    }


def _late(facts):
    item = facts["product"] or "parcel"
    ref = _reference(facts)
    order = facts["order_ids"][0] if facts["order_ids"] else "your order"
    opening = _opening(facts)

    issue = (
        f"{opening}Your {item} has not reached you yet{ref}, and I have raised a "
        f"shipment trace with the delivery partner for {order} — this forces a "
        "physical status check at every hub the parcel passed through, not just "
        "an automated update. If the parcel is confirmed lost or stuck for more "
        "than 24 hours after the trace, you get an immediate replacement "
        "dispatch or a full refund — your choice, no back-and-forth. "
        f"Share the Order ID and expected delivery date so the trace can start "
        f"today.{_repeat_note(facts)}"
    )

    return {
        "summary": f"Delayed {item}{ref} — shipment trace raised, replacement or refund if lost",
        "issue": issue,
        "analysis": (
            "Delays come from one of three places: the parcel is genuinely still "
            "in transit, the courier missed or faked a delivery attempt, or it "
            "is sitting stuck at a sorting hub. The shipment trace pulls the "
            "scan history for every hop, so within a few hours we know exactly "
            "which of the three it is and can act instead of guessing."
        ),
        "steps": [
            f"We open a shipment trace on {order} with the courier (priority queue).",
            "Hub-by-hub scan history is reviewed to locate the parcel.",
            "The delivery partner is contacted directly for a re-attempt within 24 hours.",
            "If it is lost or undelivered after 24 hours, a replacement or refund is released without further delay.",
            "You get an update every 24 hours until this is closed, even if there is no news.",
        ],
        "recovery": [
            {
                "title": "Re-attempted delivery",
                "detail": "A new delivery slot is booked for the next working day once the parcel is located.",
            },
            {
                "title": "Instant replacement",
                "detail": "If the parcel is declared lost, a replacement ships the same day at no cost.",
            },
            {
                "title": "Full refund",
                "detail": "Alternatively, the complete amount is returned to your original payment method in 3–5 business days.",
            },
            {
                "title": "Late-delivery credit",
                "detail": "If the order is already past its expected date, a store credit is issued for the inconvenience.",
            },
        ],
        "alternatives": [
            "Cancel this order and get a full refund — no cancellation fee.",
            "Reorder the same item with priority/expedited shipping at no extra cost.",
            "Redirect delivery to a different address or a preferred time slot.",
            "Split the shipment if part of the order is already in transit.",
        ],
        "timeline": (
            "Trace opened: immediately · Courier response: within 12–24 hours · "
            "Re-delivery or replacement: next 1–2 working days · Refund: 3–5 business days."
        ),
        "need": _need(facts, ["Order ID", "Expected delivery date", "Delivery PIN code / address"]),
        "priority": "High" if facts["urgency"] else "Normal",
    }


def _wrong(facts):
    item = facts["product"] or "item"
    ref = _reference(facts)
    opening = _opening(facts)

    issue = (
        f"{opening}Receiving something you did not order{ref} is a fulfilment "
        "mistake at our end, and it is fully on us to correct it. The correct "
        "item is dispatched as soon as you send a photo of what you received "
        "with the shipping label visible — and you keep the wrongly delivered "
        "piece until the replacement reaches you, so you are never left with "
        "nothing. There is no extra charge for any of this."
        f"{_repeat_note(facts)}"
    )

    return {
        "summary": f"Wrong item received instead of the {item}{ref} — correct item ships fast",
        "issue": issue,
        "analysis": (
            "This is almost always a pick-and-pack error or a label mix-up at "
            "the warehouse — the parcel was packed correctly for a different "
            "order and shipped under your label. Because the mistake is ours, "
            "you are entitled to the correct item immediately, a full refund, "
            "or an exchange, and you are not expected to pay shipping in any "
            "scenario."
        ),
        "steps": [
            "Send a photo of the item you received plus the shipping label on the box.",
            "We verify the mismatch against the warehouse pick record (within 4 hours).",
            "The correct item is dispatched the same day — no need to return anything first.",
            "A free doorstep pickup of the wrong item is scheduled for a day that suits you.",
            "If you prefer a refund instead, it is initiated as soon as the pickup is scanned.",
        ],
        "recovery": [
            {
                "title": "Correct item, fast",
                "detail": "Dispatched the same day the mismatch is confirmed, delivered in 2–3 days free of cost.",
            },
            {
                "title": "Full refund",
                "detail": "100% returned to your original payment method within 3–5 business days.",
            },
            {
                "title": "Keep the wrong item",
                "detail": "For low-value mix-ups you may keep it with a partial refund instead of a return pickup.",
            },
            {
                "title": "Price difference waived",
                "detail": "If the item you received costs less than what you ordered, the difference is refunded automatically.",
            },
        ],
        "alternatives": [
            "Exchange for a different size, colour or model of the item you actually wanted.",
            "Cancel the whole order for a complete refund with no restocking fee.",
            "Take store credit with a 10% bonus and order again whenever you like.",
            "Upgrade to a higher variant and pay only the difference.",
        ],
        "timeline": (
            "Mismatch verified: ~4 hours · Correct item dispatched: same day · "
            "Doorstep pickup: next working day · Refund: 3–5 business days."
        ),
        "need": _need(facts, ["Photo of the item received", "Photo of the shipping label"]),
        "priority": "High" if facts["urgency"] else "Normal",
    }


def _refund(facts):
    item = facts["product"] or "order"
    ref = _reference(facts)
    order = facts["order_ids"][0] if facts["order_ids"] else "your order"
    opening = _opening(facts)

    issue = (
        f"{opening}Your refund request for {order}{ref} has been accepted — "
        "no further approval is needed from your side. Once it is released, "
        "the amount goes back to the original payment method: most wallets and "
        "UPI reflect it within 24 hours, cards and net banking within 3–7 "
        "business days depending on your bank. If it has already been longer "
        "than that, share the UTR/reference number and I will trace it with "
        "the payment gateway today and give you a firm date."
        f"{_repeat_note(facts)}"
    )

    return {
        "summary": f"Refund accepted for {order}{ref} — status traced end to end",
        "issue": issue,
        "analysis": (
            "Your refund is released from our side once the return is picked up "
            "or the request is approved, and then it travels through your bank "
            "or payment provider. The delay people usually see is at the bank "
            "end, not ours — so we track it with the gateway reference until it "
            "actually lands in your account, instead of telling you to 'wait "
            "and see'."
        ),
        "steps": [
            "We confirm the refund amount and release it against your order.",
            "A UTR / reference number is generated and shared with you.",
            "We track that reference daily until it is credited to your account.",
            "If the bank misses the SLA, an escalation is raised with the payment partner.",
            "You get a confirmation message the moment it is credited.",
        ],
        "recovery": [
            {
                "title": "Full refund to source",
                "detail": "Credited to the original payment method — UPI/wallet in 24 hours, cards in 3–7 business days.",
            },
            {
                "title": "Instant store credit",
                "detail": "Take the amount as an e-credit immediately and use it on any order, no waiting on the bank.",
            },
            {
                "title": "Replacement instead",
                "detail": "If you would rather have the product, we can swap the refund for a replacement at no cost.",
            },
            {
                "title": "Refund with return pickup",
                "detail": "Free doorstep pickup of the item so nothing needs to be shipped by you.",
            },
        ],
        "alternatives": [
            "Cancel any pending replacement and convert it to a refund.",
            "Transfer the refund to a different bank account or UPI ID.",
            "Take a 10% bonus store credit instead of the cash refund.",
            "Apply the amount against another open order instead of withdrawing it.",
        ],
        "timeline": (
            "Refund released: within 24 hours of approval · UPI/wallet: 24 hours · "
            "Card/net banking: 3–7 business days · Escalation if overdue: immediate."
        ),
        "need": _need(facts, ["Order ID", "Refund / UTR reference if you have one"]),
        "priority": "High" if facts["urgency"] else "Normal",
    }


def _payment(facts):
    item = facts["product"] or "order"
    ref = _reference(facts)
    method = facts["payment_method"] or "your payment method"
    order = facts["order_ids"][0] if facts["order_ids"] else "this transaction"
    opening = _opening(facts)

    issue = (
        f"{opening}When money is debited but the {item} is not confirmed{ref}, "
        "the amount is almost always held by your bank or payment provider as "
        "an authorisation that never completed — it has not been taken by us. "
        "Send the transaction ID and a screenshot of the debit and we reconcile "
        "it with the gateway: if the payment did not actually go through, an "
        "automatic reversal starts immediately and typically lands in 24–48 "
        "hours (some banks take up to 5 working days); if it did go through, "
        "we confirm your order on the spot so you pay only once."
        f"{_repeat_note(facts)}"
    )

    return {
        "summary": f"Payment problem on {order}{ref} — reversal or order confirmation within 48 hours",
        "issue": issue,
        "analysis": (
            "There are only two possible outcomes here and we check both: "
            "either the transaction failed after the debit (a temporary hold "
            "that auto-reverses), or it succeeded but the order confirmation "
            "never reached us (in which case we confirm it manually and you "
            "keep the payment). Either way the money is not lost — you will "
            "either get the product or the amount back, guaranteed."
        ),
        "steps": [
            "Share the transaction ID, amount, date and a screenshot of the debit.",
            "We match it against the payment gateway logs within 2 working hours.",
            "If failed: an auto-reversal is triggered and the UTR is shared with you.",
            "If successful: the order is confirmed manually and a receipt is re-issued.",
            "We follow up until the amount is actually back in your account or the order is confirmed.",
        ],
        "recovery": [
            {
                "title": "Automatic reversal",
                "detail": "Failed transactions reverse in 24–48 hours; banks may take up to 5 working days to post it.",
            },
            {
                "title": "Order confirmed manually",
                "detail": "If the money really went through, your order is activated without paying again.",
            },
            {
                "title": "Refund to source / different account",
                "detail": "If reversal is delayed beyond 5 days, we push a manual refund to the same or another account you choose.",
            },
            {
                "title": "Goodwill credit",
                "detail": "If the money was held longer than 5 days, a store credit is issued for the trouble.",
            },
        ],
        "alternatives": [
            "Retry the payment with a different method (UPI, card or COD) while the reversal runs.",
            "Get a fresh secure payment link so the pending amount is not double-charged.",
            "Cancel this attempt and place a fresh order — the old debit still reverses on its own.",
            "Raise a chargeback with your bank using our transaction details, if you prefer.",
        ],
        "timeline": (
            "Gateway reconciliation: ~2 hours · Auto-reversal: 24–48 hours · "
            "Bank posting: up to 5 working days · Order confirmation: same day if paid."
        ),
        "need": _need(facts, ["Transaction ID", "Screenshot of the debit", "Amount, date and payment method"]),
        "priority": "High" if facts["urgency"] else "Normal",
    }


def _general(facts, text):
    snippet = text.strip()
    if len(snippet) > 160:
        snippet = snippet[:157].rstrip() + "..."
    opening = _opening(facts)

    issue = (
        f"{opening}I have read your message in full: \"{snippet}\". This does "
        "not match a standard support case, so rather than force it into the "
        "wrong bucket I have routed it to a human specialist who will read it "
        "the same way I did. To solve it in one pass, send your Order ID (if "
        "this involves an order) and what you expected versus what actually "
        "happened — with those two details most issues close within 24 hours, "
        "and refunds, replacements or corrections can all be started from this "
        "same thread."
        f"{_repeat_note(facts)}"
    )

    return {
        "summary": "Routed to a specialist — one round of details is enough to close it",
        "issue": issue,
        "analysis": (
            "Your message does not clearly belong to damage, delivery, wrong "
            "item, refund or payment, so it has been marked as a general "
            "enquiry instead of being misclassified. From the wording, the "
            "core of it seems to be: "
            f"\"{snippet}\" — a specialist will confirm the exact issue with "
            "you rather than guess."
        ),
        "steps": [
            "Tell us the Order ID if your message relates to an order.",
            "Describe what you expected versus what actually happened, in one or two lines.",
            "Add any screenshot, bill or reference number that helps us verify it.",
            "A specialist reviews and replies within 24 hours (priority queue if urgent).",
            "If it turns out to be one of the standard cases, it converts instantly — you do not have to start over.",
        ],
        "recovery": [
            {
                "title": "Full resolution from this thread",
                "detail": "Once we confirm the exact issue, refund, replacement, correction or escalation can all be started right here.",
            },
            {
                "title": "Human review",
                "detail": "A support specialist reads your message personally within 24 hours — no chatbot loops.",
            },
            {
                "title": "Refund / replacement if eligible",
                "detail": "If this involves an order that did not go as promised, the standard remedies apply in full.",
            },
        ],
        "alternatives": [
            "Talk to a live agent now on chat or call for an immediate answer.",
            "Schedule a callback at a time that suits you.",
            "Check the help centre for instant answers on orders, refunds and returns.",
            "Rephrase the complaint in one line and re-run the analyzer — it will map to a standard case.",
        ],
        "timeline": (
            "First human reply: within 24 hours · Standard cases resolved: "
            "24–48 hours · Refunds after approval: 3–5 business days."
        ),
        "need": _need(facts, ["What you expected vs what happened", "Order ID if an order is involved"]),
        "priority": "High" if facts["urgency"] else "Normal",
    }


def _need(facts, base):
    needed = list(base)
    if not facts["order_ids"] and "Order ID" not in " ".join(needed):
        needed.append("Order ID")
    if facts["missing_info"]:
        for extra in facts["missing_info"]:
            if extra.lower() not in " ".join(needed).lower():
                needed.append(extra)
    seen = set()
    unique = []
    for item in needed:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


BUILDERS = {
    "Damaged Product": _damaged,
    "Late Delivery": _late,
    "Wrong Item": _wrong,
    "Refund": _refund,
    "Payment Issue": _payment,
}


def build_response(category, facts, text):
    if category in BUILDERS:
        return BUILDERS[category](facts)
    return _general(facts, text)


# ============================================================
# PUBLIC ENTRY
# ============================================================

def analyze(complaint, model_category=None, model_confidence=0.0):
    text = complaint or ""
    facts = extract_facts(text)

    category, confidence, scores, hits = decide_category(
        text, model_category, model_confidence
    )

    response = build_response(category, facts, text)

    response.update(
        {
            "complaint": text.strip(),
            "category": category,
            "confidence": confidence,
            "show_upload": should_show_upload(category, facts, text),
            "show_delivery_form": should_show_delivery_form(category, facts, text),
            "facts": {
                "orderIds": facts["order_ids"],
                "amount": facts["amount"],
                "product": facts["product"],
                "paymentMethod": facts["payment_method"],
                "dates": facts["dates"],
            },
            "signals": {
                "urgency": facts["urgency"],
                "repeat": facts["repeat"],
                "emotion": facts["emotion"],
            },
        }
    )
    return response
