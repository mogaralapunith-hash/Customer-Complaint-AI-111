const post = async (url, body, isForm = false) => {
  const response = await fetch(url, {
    method: "POST",
    body,
    headers: isForm ? undefined : { "Content-Type": "application/json" }
  });

  let data;
  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    const message = data.error || "Something went wrong. Please try again.";
    throw new Error(message);
  }

  return data;
};

export const fetchPrediction = (complaint) =>
  post("/api/predict", JSON.stringify({ complaint }));

export const uploadImage = (file) => {
  const form = new FormData();
  form.append("image", file);
  return post("/api/upload", form, true);
};

export const submitDelivery = (orderId, deliveryDate) =>
  post(
    "/api/delivery_details",
    JSON.stringify({ order_id: orderId, delivery_date: deliveryDate })
  );