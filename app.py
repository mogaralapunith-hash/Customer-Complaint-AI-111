from flask import Flask, render_template, request
import os
import pickle
from werkzeug.utils import secure_filename


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================
# MODEL PATH
# ==========================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "classifier.pkl"
)


# ==========================================
# LOAD TRAINED AI MODEL
# ==========================================

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


# ==========================================
# UPLOAD FOLDER
# ==========================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================================
# SMART ISSUE RESPONSE
# ==========================================

def generate_response(complaint):

    text = complaint.lower()


    # --------------------------------------
    # DAMAGED PRODUCT
    # --------------------------------------

    if any(word in text for word in [
        "damaged",
        "damage",
        "broken",
        "crack",
        "cracked"
    ]):

        return {
            "issue": (
                "We are sorry that your product arrived damaged. "
                "Please upload one clear photo of the damaged product. "
                "Our support team will verify the damage and arrange "
                "a refund or replacement. You will receive an update "
                "within 24 hours."
            ),

            "show_upload": True,

            "show_delivery_form": False
        }


    # --------------------------------------
    # LATE DELIVERY
    # --------------------------------------

    elif any(word in text for word in [
        "late",
        "delay",
        "delayed",
        "not arrived",
        "not received",
        "didn't arrive",
        "did not arrive",
        "order not came",
        "not come",
        "haven't received",
        "hasn't arrived"
    ]):

        return {
            "issue": (
                "We are sorry for the delay in your order. "
                "Please provide your Order ID and Expected Delivery Date. "
                "Our support team will check the shipment status and "
                "contact the delivery partner if required. "
                "You will receive an update within 24 hours. "
                "If the package is confirmed lost, we can arrange "
                "a replacement or full refund."
            ),

            "show_upload": False,

            "show_delivery_form": True
        }


    # --------------------------------------
    # WRONG ITEM
    # --------------------------------------

    elif any(word in text for word in [
        "wrong item",
        "wrong product",
        "incorrect item",
        "different product",
        "wrong order"
    ]):

        return {
            "issue": (
                "We are sorry that you received the wrong product. "
                "Please upload a clear photo of the product you received. "
                "Our support team will verify it and arrange a replacement "
                "as soon as possible."
            ),

            "show_upload": True,

            "show_delivery_form": False
        }


    # --------------------------------------
    # REFUND
    # --------------------------------------

    elif any(word in text for word in [
        "refund",
        "money back",
        "moneyback",
        "return my money"
    ]):

        return {
            "issue": (
                "Your refund request has been noted. "
                "Once the refund is processed, the amount may take "
                "5–7 business days to appear in your account, "
                "depending on your bank or payment provider."
            ),

            "show_upload": False,

            "show_delivery_form": False
        }


    # --------------------------------------
    # PAYMENT
    # --------------------------------------

    elif any(word in text for word in [
        "payment",
        "paid",
        "transaction",
        "charged",
        "payment failed",
        "payment issue"
    ]):

        return {
            "issue": (
                "We are sorry for the payment issue. "
                "Please provide your Transaction ID and a screenshot "
                "of the payment. Our support team will verify the "
                "transaction and assist you."
            ),

            "show_upload": True,

            "show_delivery_form": False
        }


    # --------------------------------------
    # DEFAULT RESPONSE
    # --------------------------------------

    else:

        return {
            "issue": (
                "Thank you for contacting Customer Complaint AI. "
                "Our support team has received your complaint and "
                "will review it shortly."
            ),

            "show_upload": False,

            "show_delivery_form": False
        }


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# PREDICT COMPLAINT
# ==========================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    complaint = request.form.get(
        "complaint",
        ""
    ).strip()


    if not complaint:

        return render_template(
            "index.html",
            issue="Please enter a complaint."
        )


    # AI prediction

    prediction = model.predict(
        [complaint]
    )[0]


    # Smart response

    response = generate_response(
        complaint
    )


    return render_template(
        "index.html",

        complaint=complaint,

        prediction=prediction,

        issue=response["issue"],

        show_upload=response["show_upload"],

        show_delivery_form=response[
            "show_delivery_form"
        ]
    )


# ==========================================
# IMAGE UPLOAD
# ==========================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    image = request.files.get(
        "image"
    )


    if image and image.filename:

        filename = secure_filename(
            image.filename
        )


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )


        image.save(filepath)


        return render_template(
            "index.html",

            issue=(
                "Thank you! Your image has been "
                "uploaded successfully. Our support "
                "team will verify the product and "
                "get back to you within 24 hours."
            ),

            uploaded_image=filename
        )


    return render_template(
        "index.html",

        issue=(
            "Please select an image "
            "before uploading."
        )
    )


# ==========================================
# DELIVERY DETAILS
# ==========================================

@app.route(
    "/delivery_details",
    methods=["POST"]
)
def delivery_details():

    order_id = request.form.get(
        "order_id"
    )

    delivery_date = request.form.get(
        "delivery_date"
    )


    return render_template(
        "index.html",

        issue=(
            f"Thank you. Your delivery details "
            f"have been received. Order ID: "
            f"{order_id}. Expected Delivery Date: "
            f"{delivery_date}. Our support team "
            f"will check your shipment and provide "
            f"an update within 24 hours."
        )
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )