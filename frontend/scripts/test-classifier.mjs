import { analyzeComplaint } from "../src/lib/classifier.js";

const EXPECTED = [
  ["My product arrived damaged", "Damaged Product"],
  ["The product is broken", "Damaged Product"],
  ["I received a cracked item", "Damaged Product"],
  ["My item has damage", "Damaged Product"],
  ["The package contained a broken product", "Damaged Product"],
  ["My product is cracked", "Damaged Product"],
  ["The product was damaged during delivery", "Damaged Product"],
  ["I received a damaged phone", "Damaged Product"],
  ["My order has not arrived", "Late Delivery"],
  ["My order is late", "Late Delivery"],
  ["My package has been delayed", "Late Delivery"],
  ["I have not received my order", "Late Delivery"],
  ["My delivery has not come yet", "Late Delivery"],
  ["The expected delivery date has passed", "Late Delivery"],
  ["My package is delayed", "Late Delivery"],
  ["I am still waiting for my order", "Late Delivery"],
  ["I received the wrong product", "Wrong Item"],
  ["I received the wrong item", "Wrong Item"],
  ["The item I received is incorrect", "Wrong Item"],
  ["You sent me a different product", "Wrong Item"],
  ["My order contains the wrong product", "Wrong Item"],
  ["I ordered a phone but received headphones", "Wrong Item"],
  ["I got the wrong order", "Wrong Item"],
  ["The product delivered is not what I ordered", "Wrong Item"],
  ["I want a refund", "Refund"],
  ["Please refund my money", "Refund"],
  ["I need my money back", "Refund"],
  ["I want to get my payment refunded", "Refund"],
  ["How can I get a refund", "Refund"],
  ["I want to return the product and get a refund", "Refund"],
  ["Please process my refund", "Refund"],
  ["When will I receive my refund", "Refund"],
  ["My payment failed", "Payment Issue"],
  ["I have a problem with my payment", "Payment Issue"],
  ["My payment was not successful", "Payment Issue"],
  ["I was charged but my order failed", "Payment Issue"],
  ["My transaction failed", "Payment Issue"],
  ["Money was deducted but the order was not placed", "Payment Issue"],
  ["I was charged twice", "Payment Issue"],
  ["There is an issue with my payment", "Payment Issue"],

  ["My product is missing", "Late Delivery"],
  ["The parcel never showed up", "Late Delivery"],
  ["It has been two weeks and my order has not come", "Late Delivery"],
  ["Where is my order, no updates from courier", "Late Delivery"],
  ["My order still has not arrived", "Late Delivery"],
  ["The box was crushed and my phone screen broke", "Damaged Product"],
  ["My laptop arrived with a cracked screen", "Damaged Product"],
  ["The blender I got is defective and does not work", "Damaged Product"],
  ["I ordered the blue shirt but got a red one", "Wrong Item"],
  ["You sent me the wrong size", "Wrong Item"],
  ["I want my money back please", "Refund"],
  ["Please reverse the payment", "Payment Issue"],
  ["Money got debited twice from my account", "Payment Issue"],
  ["My card was charged but no order was placed", "Payment Issue"],
  ["The item arrived broken", "Damaged Product"],
  ["Cancel my order I need a refund", "Refund"],
  ["My order is overdue", "Late Delivery"],
  ["I received headphones instead of the phone I ordered", "Wrong Item"],
  ["The product does not work at all", "Damaged Product"],
  ["Tracking shows no delivery yet", "Late Delivery"]
];

const EXPECT_FORM = {
  "Damaged Product": { upload: true, delivery: false },
  "Wrong Item": { upload: true, delivery: false },
  "Payment Issue": { upload: true, delivery: false },
  "Late Delivery": { upload: false, delivery: true },
  Refund: { upload: false, delivery: false }
};

let failed = 0;

EXPECTED.forEach(([complaint, expected]) => {
  const result = analyzeComplaint(complaint);
  const form = EXPECT_FORM[result.category];
  const formOk =
    form &&
    result.showUpload === form.upload &&
    result.showDeliveryForm === form.delivery;
  const ok = result.category === expected && formOk && result.issue.length > 40;

  if (!ok) {
    failed += 1;
    console.log(
      `FAIL  "${complaint}"\n      expected=${expected} got=${result.category} conf=${result.confidence.toFixed(2)} upload=${result.showUpload} delivery=${result.showDeliveryForm}`
    );
  }
});

console.log(
  `\n${EXPECTED.length - failed}/${EXPECTED.length} cases passed`
);
process.exit(failed === 0 ? 0 : 1);
