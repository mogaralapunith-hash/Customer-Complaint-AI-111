# Customer Complaint AI

A Flask web app that classifies customer complaints with a trained scikit-learn model and displays a suggested response.

## Project contents

- `app.py` - Flask application and request handlers
- `models/classifier.pkl` - pre-trained complaint classifier
- `dataset/complaints.csv` - sample training data
- `train_model.py` - script to retrain the classifier
- `templates/` and `static/` - HTML template and styles

## Run locally

Use Python 3. Install the dependencies and start the app:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5001> in your browser.

To retrain the model using the included dataset, run:

```bash
python train_model.py
```

## Add this project to GitHub

Create a repository on GitHub, extract the project ZIP, then upload the extracted files to that repository. Alternatively, from the extracted project folder:

```bash
git init
git add .
git commit -m "Add Customer Complaint AI"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

GitHub stores the source code but does not run Flask applications on GitHub Pages. A hosting service that supports Python is needed to make this app available as a live website.