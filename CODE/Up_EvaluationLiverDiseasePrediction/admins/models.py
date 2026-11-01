from django.db import models


class Patient(models.Model):

    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    total_bilirubin = models.FloatField()
    direct_bilirubin = models.FloatField()
    alkaline_phosphotase = models.FloatField()

    alamine_aminotransferase = models.FloatField()
    aspartate_aminotransferase = models.FloatField()

    total_proteins = models.FloatField()
    albumin = models.FloatField()
    albumin_globulin_ratio = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient {self.id} - Age {self.age}"

    class Meta:
        db_table = "patients"
        ordering = ["-created_at"]


class Prediction(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="predictions"
    )

    algorithm_used = models.CharField(max_length=100)
    prediction_result = models.CharField(max_length=50)
    accuracy = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.algorithm_used} - {self.prediction_result}"

    class Meta:
        db_table = "predictions"
        ordering = ["-created_at"]