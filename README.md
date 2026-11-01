# Liver Disease Prediction

Django project for evaluating machine-learning approaches to liver disease prediction.

## Configuration

Set `DJANGO_SECRET_KEY` in the environment before running Django commands. For example, in PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = "your-generated-secret-key"
```

Keep this key private and do not commit it to the repository.

## Run locally

From `CODE/Up_EvaluationLiverDiseasePrediction`, run:

```powershell
python manage.py migrate
python manage.py runserver
```

The liver patient CSV used by the project is in `media/indian_liver_patient.csv`. Local SQLite databases and Python cache files are intentionally excluded from Git.
