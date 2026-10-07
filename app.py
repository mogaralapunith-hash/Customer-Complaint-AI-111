from flask import Flask, render_template, request, jsonify, url_for
import os
import math
import pickle
from werkzeug.utils import secure_filename

from analyzer import analyze


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

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ==========================================
# ANALYSIS IS HANDLED BY analyzer.py
# ==========================================


# ==========================================
# CONFIDENCE OF AI PREDICTION
# ==========================================

def prediction_confidence(pipeline, text):

    try:

        margins = pipeline.decision_function([text])[0]

        ordered = sorted(margins, reverse=True)

        top = ordered[0]

        runner_up = ordered[1] if len(ordered) > 1 else 0.0

        margin = top - runner_up

        confidence = min(0.98, max(0.05, 1 / (1 + math.exp(-margin))))

    except Exception:

        confidence = 0.72

    return round(confidence, 3)


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

    prediction = model.predict(
        [complaint]
    )[0]

    confidence = prediction_confidence(
        model,
        complaint
    )

    result = analyze(
        complaint,
        model_category=prediction,
        model_confidence=confidence
    )

    return render_template(
        "index.html",

        complaint=complaint,

        prediction=result["category"],

        issue=result["issue"],

        summary=result["summary"],

        analysis=result["analysis"],

        steps=result["steps"],

        recovery=result["recovery"],

        alternatives=result["alternatives"],

        timeline=result["timeline"],

        need_from_you=result["need"],

        priority=result["priority"],

        show_upload=result["show_upload"],

        show_delivery_form=result[
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

    if image and image.filename and allowed_file(image.filename):

        filename = secure_filename(
            image.filename
        )

        unique_filename = (
            f"{os.path.splitext(filename)[0]}-{os.urandom(3).hex()}"
            f"{os.path.splitext(filename)[1]}"
        )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
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

            uploaded_image=unique_filename
        )

    return render_template(
        "index.html",

        issue=(
            "Please select a valid image file "
            "(PNG, JPG, WEBP or GIF) before uploading."
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
        "order_id",
        ""
    ).strip()

    delivery_date = request.form.get(
        "delivery_date",
        ""
    ).strip()

    if not order_id or not delivery_date:

        return render_template(
            "index.html",

            issue=(
                "Please provide both your Order ID "
                "and Expected Delivery Date."
            )
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
# HEALTH CHECK (API)
# ==========================================

@app.route("/api/health", methods=["GET"])
def api_health():

    return jsonify(
        status="ok",
        service="Customer Complaint AI API",
        version="1.0.0"
    )


# ==========================================
# PREDICT COMPLAINT (API)
# ==========================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def api_predict():

    complaint = request.form.get(
        "complaint",
        request.json.get("complaint", "") if request.is_json else ""
    ).strip()

    if not complaint:

        return jsonify(
            error="Please enter a complaint."
        ), 400

    prediction = model.predict(
        [complaint]
    )[0]

    confidence = prediction_confidence(
        model,
        complaint
    )

    result = analyze(
        complaint,
        model_category=prediction,
        model_confidence=confidence
    )

    return jsonify(
        complaint=result["complaint"],
        category=result["category"],
        confidence=result["confidence"],
        summary=result["summary"],
        issue=result["issue"],
        analysis=result["analysis"],
        steps=result["steps"],
        recovery=result["recovery"],
        alternatives=result["alternatives"],
        timeline=result["timeline"],
        needFromYou=result["need"],
        priority=result["priority"],
        facts=result["facts"],
        signals=result["signals"],
        showUpload=result["show_upload"],
        showDeliveryForm=result[
            "show_delivery_form"
        ]
    )


# ==========================================
# IMAGE UPLOAD (API)
# ==========================================

@app.route(
    "/api/upload",
    methods=["POST"]
)
def api_upload():

    image = request.files.get(
        "image"
    )

    if not image or not image.filename:

        return jsonify(
            error="Please select an image before uploading."
        ), 400

    if not allowed_file(image.filename):

        return jsonify(
            error="Please select a valid image file "
                  "(PNG, JPG, WEBP or GIF)."
        ), 400

    filename = secure_filename(
        image.filename
    )

    unique_filename = (
        f"{os.path.splitext(filename)[0]}-{os.urandom(3).hex()}"
        f"{os.path.splitext(filename)[1]}"
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    image.save(filepath)

    return jsonify(
        message=(
            "Thank you! Your image has been uploaded successfully. "
            "Our support team will verify the product and get back "
            "to you within 24 hours."
        ),
        filename=unique_filename,
        url=url_for("static", filename=f"uploads/{unique_filename}")
    )


# ==========================================
# DELIVERY DETAILS (API)
# ==========================================

@app.route(
    "/api/delivery_details",
    methods=["POST"]
)
def api_delivery_details():

    data = request.form if request.form else (request.json or {})

    order_id = data.get(
        "order_id",
        ""
    ).strip()

    delivery_date = data.get(
        "delivery_date",
        ""
    ).strip()

    if not order_id or not delivery_date:

        return jsonify(
            error=(
                "Please provide both your Order ID "
                "and Expected Delivery Date."
            )
        ), 400

    return jsonify(
        message=(
            f"Thank you. Your delivery details have been received. "
            f"Order ID: {order_id}. Expected Delivery Date: "
            f"{delivery_date}. Our support team will check your "
            f"shipment and provide an update within 24 hours."
        ),
        orderId=order_id,
        deliveryDate=delivery_date
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