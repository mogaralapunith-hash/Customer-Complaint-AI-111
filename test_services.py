"""Test every service response of the Customer Complaint AI Flask app."""

import io
import os
import unittest
import warnings

warnings.filterwarnings("ignore")

import app as customer_app


class CustomerComplaintServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        customer_app.app.config.update(TESTING=True)
        cls.client = customer_app.app.test_client()

    def test_01_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Customer Complaint", response.get_data(as_text=True))

    def test_02_predict_empty(self):
        response = self.client.post("/predict", data={"complaint": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Please enter a complaint.", response.get_data(as_text=True))

    def test_03_predict_html_all_categories(self):
        cases = [
            ("My product arrived damaged", "Damaged Product"),
            ("My order is late and has not arrived", "Late Delivery"),
            ("I received the wrong item instead of the phone", "Wrong Item"),
            ("I want a refund for my order", "Refund"),
            ("My payment failed but money was deducted", "Payment Issue"),
            ("What is the weather today in Tokyo", None),
        ]
        for complaint, expected in cases:
            response = self.client.post("/predict", data={"complaint": complaint})
            self.assertEqual(response.status_code, 200)
            body = response.get_data(as_text=True)
            self.assertIn("AI Prediction", body)
            self.assertIn("Issue Resolution", body)
            if expected:
                self.assertIn(expected, body)

    def test_04_upload_no_file(self):
        response = self.client.post("/upload", data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn("valid image", response.get_data(as_text=True))

    def test_05_upload_invalid_file(self):
        data = {"image": (io.BytesIO(b"not an image"), "notes.txt")}
        response = self.client.post("/upload", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 200)
        self.assertIn("valid image", response.get_data(as_text=True))

    def test_06_upload_valid_image(self):
        png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64
        data = {"image": (io.BytesIO(png), "proof.png")}
        with customer_app.app.test_request_context():
            response = self.client.post("/upload", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("uploaded successfully", body)
        uploads = os.listdir(customer_app.app.config["UPLOAD_FOLDER"])
        self.assertTrue(any(name.startswith("proof-") for name in uploads))

    def test_07_delivery_details_valid(self):
        response = self.client.post(
            "/delivery_details",
            data={"order_id": "ORD-2026-77821", "delivery_date": "2026-10-15"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("ORD-2026-77821", body)
        self.assertIn("2026-10-15", body)

    def test_08_delivery_details_missing(self):
        response = self.client.post("/delivery_details", data={"order_id": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Order ID", response.get_data(as_text=True))

    def test_09_health_api(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("Customer Complaint AI", payload["service"])

    def test_10_api_predict_json(self):
        cases = [
            ("My phone arrived broken", "Damaged Product", True, False),
            ("My order is delayed and has not arrived", "Late Delivery", False, True),
            ("I received the wrong product", "Wrong Item", True, False),
            ("I want my money back for a refund", "Refund", False, False),
            ("My payment was charged twice", "Payment Issue", True, False),
            ("I had a great holiday trip", "General Enquiry", False, False),
        ]
        for complaint, expected, upload, delivery in cases:
            response = self.client.post(
                "/api/predict", json={"complaint": complaint}
            )
            self.assertEqual(response.status_code, 200, complaint)
            payload = response.get_json()
            self.assertEqual(payload["category"], expected, complaint)
            self.assertEqual(payload["showUpload"], upload, complaint)
            self.assertEqual(payload["showDeliveryForm"], delivery, complaint)
            self.assertLessEqual(payload["confidence"], 0.98)
            self.assertGreaterEqual(payload["confidence"], 0.0)

    def test_11_api_predict_form(self):
        response = self.client.post("/api/predict", data={"complaint": "I request a refund please"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["category"], "Refund")

    def test_12_api_predict_empty(self):
        response = self.client.post("/api/predict", json={"complaint": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_13_api_upload_no_file(self):
        response = self.client.post("/api/upload", data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_14_api_upload_invalid_type(self):
        data = {"image": (io.BytesIO(b"x"), "file.exe")}
        response = self.client.post("/api/upload", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 400)

    def test_15_api_upload_valid(self):
        png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64
        data = {"image": (io.BytesIO(png), "complaint-photo.png")}
        response = self.client.post("/api/upload", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("uploads/", payload["url"])
        self.assertIn("thank you", payload["message"].lower())

    def test_16_api_delivery_valid_form(self):
        response = self.client.post(
            "/api/delivery_details",
            data={"order_id": "ORD-55", "delivery_date": "2026-11-02"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["orderId"], "ORD-55")
        self.assertIn("ORD-55", payload["message"])

    def test_17_api_delivery_valid_json(self):
        response = self.client.post(
            "/api/delivery_details",
            json={"order_id": "ORD-99", "delivery_date": "2026-12-25"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["orderId"], "ORD-99")

    def test_18_api_delivery_missing(self):
        response = self.client.post("/api/delivery_details", json={"order_id": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        CustomerComplaintServiceTest
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    total = suite.countTestCases()
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"\n=== {passed}/{total} service tests passed ===")
    raise SystemExit(0 if result.wasSuccessful() else 1)