const DATASET = [
  ["My product arrived damaged", "Damaged Product"],
  ["The product is broken", "Damaged Product"],
  ["I received a cracked item", "Damaged Product"],
  ["My item has damage", "Damaged Product"],
  ["The package contained a broken product", "Damaged Product"],
  ["My product is cracked", "Damaged Product"],
  ["The product was damaged during delivery", "Damaged Product"],
  ["I received a damaged phone", "Damaged Product"],
  ["My phone arrived broken", "Damaged Product"],
  ["The screen is shattered", "Damaged Product"],
  ["The item arrived in pieces", "Damaged Product"],
  ["The product is defective", "Damaged Product"],
  ["My product is not working", "Damaged Product"],
  ["The item is dented and scratched", "Damaged Product"],
  ["My order has not arrived", "Late Delivery"],
  ["My order is late", "Late Delivery"],
  ["My package has been delayed", "Late Delivery"],
  ["I have not received my order", "Late Delivery"],
  ["My delivery has not come yet", "Late Delivery"],
  ["The expected delivery date has passed", "Late Delivery"],
  ["My package is delayed", "Late Delivery"],
  ["I am still waiting for my order", "Late Delivery"],
  ["My parcel is missing", "Late Delivery"],
  ["The order never arrived", "Late Delivery"],
  ["My order was not delivered", "Late Delivery"],
  ["Where is my order", "Late Delivery"],
  ["The shipment is taking too long", "Late Delivery"],
  ["My package shows no delivery updates", "Late Delivery"],
  ["I received the wrong product", "Wrong Item"],
  ["I received the wrong item", "Wrong Item"],
  ["The item I received is incorrect", "Wrong Item"],
  ["You sent me a different product", "Wrong Item"],
  ["My order contains the wrong product", "Wrong Item"],
  ["I ordered a phone but received headphones", "Wrong Item"],
  ["I got the wrong order", "Wrong Item"],
  ["The product delivered is not what I ordered", "Wrong Item"],
  ["I received something else", "Wrong Item"],
  ["I got someone else order", "Wrong Item"],
  ["The colour I received is not what I ordered", "Wrong Item"],
  ["I want a refund", "Refund"],
  ["Please refund my money", "Refund"],
  ["I need my money back", "Refund"],
  ["I want to get my payment refunded", "Refund"],
  ["How can I get a refund", "Refund"],
  ["I want to return the product and get a refund", "Refund"],
  ["Please process my refund", "Refund"],
  ["When will I receive my refund", "Refund"],
  ["Please cancel my order and refund me", "Refund"],
  ["I want my amount reversed", "Refund"],
  ["My payment failed", "Payment Issue"],
  ["I have a problem with my payment", "Payment Issue"],
  ["My payment was not successful", "Payment Issue"],
  ["I was charged but my order failed", "Payment Issue"],
  ["My transaction failed", "Payment Issue"],
  ["Money was deducted but the order was not placed", "Payment Issue"],
  ["I was charged twice", "Payment Issue"],
  ["There is an issue with my payment", "Payment Issue"],
  ["The payment did not go through", "Payment Issue"],
  ["My card was charged but no order was placed", "Payment Issue"],
  ["The amount was debited from my account", "Payment Issue"]
];

const LEXICON = {
  "Damaged Product": [
    ["damaged", 2],
    ["damage", 2],
    ["broken", 2],
    ["break", 1],
    ["cracked", 2],
    ["crack", 2],
    ["shattered", 2],
    ["dented", 2],
    ["scratched", 1],
    ["defective", 2],
    ["not working", 2],
    ["does not work", 2],
    ["doesn't work", 2],
    ["stopped working", 2],
    ["in pieces", 2],
    ["dead on arrival", 3]
  ],
  "Late Delivery": [
    ["not arrived", 3],
    ["never arrived", 3],
    ["did not arrive", 3],
    ["didn't arrive", 3],
    ["never showed up", 3],
    ["never shown up", 3],
    ["hasn't shown up", 3],
    ["has not shown up", 3],
    ["has not arrived", 3],
    ["hasn't arrived", 3],
    ["not received", 3],
    ["haven't received", 3],
    ["hasn't received", 3],
    ["not delivered", 3],
    ["no delivery", 2],
    ["where is my order", 3],
    ["still waiting", 2],
    ["expected delivery", 2],
    ["date has passed", 3],
    ["too long", 1],
    ["no updates", 2],
    ["is missing", 2],
    ["missing", 1],
    ["late", 1],
    ["delayed", 1],
    ["delay", 1],
    ["overdue", 2],
    ["lost", 2],
    ["not come", 2],
    ["shipping", 1],
    ["courier", 1]
  ],
  "Wrong Item": [
    ["wrong item", 3],
    ["wrong product", 3],
    ["wrong order", 3],
    ["incorrect item", 3],
    ["is incorrect", 2],
    ["incorrect", 1],
    ["different product", 3],
    ["not what i ordered", 3],
    ["something else", 2],
    ["someone else", 2],
    ["instead of", 2],
    ["you sent me", 2],
    ["not what i wanted", 3],
    ["received the wrong", 3]
  ],
  Refund: [
    ["refund", 3],
    ["refunded", 3],
    ["money back", 3],
    ["moneyback", 3],
    ["return my money", 3],
    ["give my money", 3],
    ["reimburse", 3],
    ["reverse", 1],
    ["cancel my order", 1]
  ],
  "Payment Issue": [
    ["payment failed", 3],
    ["payment issue", 3],
    ["money deducted", 3],
    ["amount was debited", 3],
    ["charged twice", 3],
    ["double charged", 3],
    ["card was charged", 3],
    ["did not go through", 2],
    ["not successful", 2],
    ["transaction failed", 3],
    ["payment", 1],
    ["transaction", 2],
    ["charged", 2],
    ["deducted", 2],
    ["debited", 2],
    ["paid", 1],
    ["upi", 2],
    ["card", 1]
  ]
};

const CATEGORIES = Object.keys(LEXICON);

const tokenize = (text) =>
  text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .split(" ")
    .filter((token) => token.length >= 2);

const ngrams = (tokens) => {
  const grams = [...tokens];
  for (let i = 0; i < tokens.length - 1; i += 1) {
    grams.push(`${tokens[i]} ${tokens[i + 1]}`);
  }
  return grams;
};

const termCounts = (text) => {
  const counts = new Map();
  ngrams(tokenize(text)).forEach((gram) => {
    counts.set(gram, (counts.get(gram) || 0) + 1);
  });
  return counts;
};

const documents = DATASET.map(([complaint]) => termCounts(complaint));

const documentFrequency = new Map();
documents.forEach((counts) => {
  counts.forEach((_, gram) => {
    documentFrequency.set(gram, (documentFrequency.get(gram) || 0) + 1);
  });
});

const idf = new Map();
const totalDocuments = documents.length;
documentFrequency.forEach((df, gram) => {
  idf.set(gram, Math.log((1 + totalDocuments) / (1 + df)) + 1);
});

const vectorize = (text) => {
  const counts = termCounts(text);
  const vector = new Map();
  let norm = 0;

  counts.forEach((count, gram) => {
    const weight =
      count * (idf.get(gram) ?? Math.log((1 + totalDocuments) / 1) + 1);
    if (weight !== 0) {
      vector.set(gram, weight);
      norm += weight * weight;
    }
  });

  norm = Math.sqrt(norm) || 1;
  vector.forEach((weight, gram) => vector.set(gram, weight / norm));
  return vector;
};

const dot = (a, b) => {
  let score = 0;
  const [small, large] = a.size <= b.size ? [a, b] : [b, a];
  small.forEach((value, key) => {
    if (large.has(key)) score += value * large.get(key);
  });
  return score;
};

const centroids = (() => {
  const sums = new Map();
  const totals = new Map();

  DATASET.forEach(([complaint, category], index) => {
    if (!sums.has(category)) {
      sums.set(category, new Map());
      totals.set(category, 0);
    }
    const sum = sums.get(category);
    documents[index].forEach((count, gram) => {
      const weight =
        count * (idf.get(gram) ?? Math.log((1 + totalDocuments) / 1) + 1);
      sum.set(gram, (sum.get(gram) || 0) + weight);
    });
    totals.set(category, totals.get(category) + 1);
  });

  const result = new Map();
  sums.forEach((sum, category) => {
    const centroid = new Map();
    let norm = 0;
    sum.forEach((value, gram) => {
      const weight = value / totals.get(category);
      centroid.set(gram, weight);
      norm += weight * weight;
    });
    norm = Math.sqrt(norm) || 1;
    centroid.forEach((value, gram) => centroid.set(gram, value / norm));
    result.set(category, centroid);
  });

  return result;
})();

const escapeRegex = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

const keywordScore = (text) => {
  const scores = {};
  CATEGORIES.forEach((category) => {
    scores[category] = 0;
    LEXICON[category].forEach(([phrase, weight]) => {
      const pattern = new RegExp(`\\b${escapeRegex(phrase)}\\b`, "i");
      if (pattern.test(text)) scores[category] += weight;
    });
  });
  return scores;
};

const similarityScore = (text) => {
  const vector = vectorize(text);
  const scores = {};
  CATEGORIES.forEach((category) => {
    scores[category] = Math.max(0, dot(vector, centroids.get(category)));
  });
  return scores;
};

export const predict = (complaint) => {
  const text = complaint.toLowerCase();
  const keywords = keywordScore(text);
  const similarity = similarityScore(text);

  const scored = CATEGORIES.map((category) => ({
    category,
    score: keywords[category] * 10 + similarity[category] * 30
  })).sort((a, b) => b.score - a.score);

  const bestKeyword = Math.max(...CATEGORIES.map((c) => keywords[c]));
  const bestSimilarity = Math.max(...CATEGORIES.map((c) => similarity[c]));

  if (bestKeyword === 0 && bestSimilarity < 0.08) {
    return { category: "Other", confidence: 0.3 };
  }

  const total = scored.reduce((sum, entry) => sum + entry.score, 0);
  const confidence = Math.min(0.98, 0.35 + 0.63 * (scored[0].score / total));

  return { category: scored[0].category, confidence };
};

const RESOLUTIONS = {
  "Damaged Product": {
    issue:
      "We are sorry that your product arrived damaged. Please upload one clear photo of the damaged product. Our support team will verify the damage and arrange a refund or replacement. You will receive an update within 24 hours.",
    showUpload: true,
    showDeliveryForm: false
  },
  "Late Delivery": {
    issue:
      "We are sorry for the delay in your order. Please provide your Order ID and Expected Delivery Date. Our support team will check the shipment status and contact the delivery partner if required. You will receive an update within 24 hours. If the package is confirmed lost, we can arrange a replacement or full refund.",
    showUpload: false,
    showDeliveryForm: true
  },
  "Wrong Item": {
    issue:
      "We are sorry that you received the wrong product. Please upload a clear photo of the product you received. Our support team will verify it and arrange a replacement as soon as possible.",
    showUpload: true,
    showDeliveryForm: false
  },
  Refund: {
    issue:
      "Your refund request has been noted. Once the refund is processed, the amount may take 5–7 business days to appear in your account, depending on your bank or payment provider.",
    showUpload: false,
    showDeliveryForm: false
  },
  "Payment Issue": {
    issue:
      "We are sorry for the payment issue. Please provide your Transaction ID and a screenshot of the payment. Our support team will verify the transaction and assist you.",
    showUpload: true,
    showDeliveryForm: false
  }
};

const DEFAULT_RESOLUTION = {
  issue:
    "Thank you for contacting Customer Complaint AI. Our support team has received your complaint and will review it shortly.",
  showUpload: false,
  showDeliveryForm: false
};

export const generateResolution = (category) =>
  RESOLUTIONS[category] || DEFAULT_RESOLUTION;

export const analyzeComplaint = (complaint) => {
  const { category, confidence } = predict(complaint);
  const resolution = generateResolution(category);

  return {
    category,
    confidence,
    issue: resolution.issue,
    showUpload: resolution.showUpload,
    showDeliveryForm: resolution.showDeliveryForm
  };
};

export { CATEGORIES };
