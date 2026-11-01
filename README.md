# Liver Disease Prediction Using Machine Learning

A Django web application for exploring liver-disease patient data and comparing machine-learning classifiers. The project includes user registration and login, administrator pages, dataset preprocessing and viewing, model evaluation, and prediction-result pages.

> **Important:** This project is for academic and research purposes only. Its predictions are not medical advice and must not be used to diagnose or treat anyone.

## Project contents

- `CODE/Up_EvaluationLiverDiseasePrediction/` — Django application source code.
- `CODE/Up_EvaluationLiverDiseasePrediction/media/indian_liver_patient.csv` — patient dataset used by the application.
- `ABSTRACT/`, `BASEPAPER/`, and `DOCUMENTS/` — project abstract, reference paper, and supporting project documents.

The application evaluates Logistic Regression, Support Vector Machine (SVM), Decision Tree, Random Forest, and K-Nearest Neighbors (KNN) classifiers. The evaluation code reports accuracy, precision, sensitivity, and specificity.

## Requirements

- Python
- Django
- NumPy
- pandas
- seaborn
- Matplotlib
- scikit-learn

The repository does not currently include a pinned dependency file. Install the packages in your Python environment:

```powershell
python -m pip install Django numpy pandas seaborn matplotlib scikit-learn
```

## Setup and run

Run these commands from the Django project directory:

```powershell
cd CODE/Up_EvaluationLiverDiseasePrediction
```

Set a private Django signing key in PowerShell. Generate a fresh key for your environment; do not commit it:

```powershell
$env:DJANGO_SECRET_KEY = "<your-private-secret-key>"
```

Then initialize the local database and start the development server:

```powershell
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. The Django admin interface is available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Main application pages

- Home page and user registration/login.
- Administrator login and administration pages for registered users and prediction results.
- User pages for preprocessing and viewing the dataset.
- Model evaluation and classification-result pages.
- Liver disease prediction page.

## Data and local files

The CSV dataset is kept in `media/` because the application reads it during data processing and model evaluation. Local SQLite databases, environment files, and Python cache files are excluded from Git. The database is created locally by running migrations.

## Security and deployment

`DJANGO_SECRET_KEY` is required when Django loads the project settings. Keep it private and provide it through the deployment environment. The included settings are intended for local development; review Django's deployment checklist and configure production settings (including `DEBUG`, `ALLOWED_HOSTS`, HTTPS, static files, and a production database) before deploying publicly.
