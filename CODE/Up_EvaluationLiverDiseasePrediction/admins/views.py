from django.shortcuts import render
from django.contrib import messages
from users.models import UserRegistrationModel
from admins.models import Patient, Prediction
from users.utility import ProcessLiverDiseas


# Admin login
def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')

        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')

    return render(request, 'AdminLogin.html')


# Admin home
def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


# View registered users
def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/viewregisterusers.html', {'data': data})


# Activate users
def ActivaUsers(request):
    id = request.GET.get('uid')
    status = 'activated'
    UserRegistrationModel.objects.filter(id=id).update(status=status)

    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/viewregisterusers.html', {'data': data})


# -------------------------
# Prediction System
# -------------------------

def predict_liver_disease(request):

    if request.method == "POST":

        age = request.POST.get("age")
        gender = request.POST.get("gender")
        total_bilirubin = request.POST.get("total_bilirubin")
        direct_bilirubin = request.POST.get("direct_bilirubin")
        alkaline_phosphotase = request.POST.get("alkaline_phosphotase")

        alamine_aminotransferase = request.POST.get("alamine_aminotransferase")
        aspartate_aminotransferase = request.POST.get("aspartate_aminotransferase")

        total_proteins = request.POST.get("total_proteins")
        albumin = request.POST.get("albumin")
        albumin_globulin_ratio = request.POST.get("albumin_globulin_ratio")

        patient = Patient.objects.create(
            age=age,
            gender=gender,
            total_bilirubin=total_bilirubin,
            direct_bilirubin=direct_bilirubin,
            alkaline_phosphotase=alkaline_phosphotase,
            alamine_aminotransferase=alamine_aminotransferase,
            aspartate_aminotransferase=aspartate_aminotransferase,
            total_proteins=total_proteins,
            albumin=albumin,
            albumin_globulin_ratio=albumin_globulin_ratio
        )

        # Example algorithm call
        accuracy, precision, sensitivity, specificity = ProcessLiverDiseas.start_random_forest()

        result = "Liver Disease Detected" if accuracy > 0.5 else "No Liver Disease"

        Prediction.objects.create(
            patient=patient,
            algorithm_used="Random Forest",
            prediction_result=result,
            accuracy=accuracy
        )

        return render(request, "users/result.html", {"result": result})

    return render(request, "users/predict.html")


# Admin prediction table
def admin_view_predictions(request):
    predictions = Prediction.objects.select_related('patient').all()
    return render(request, "admins/view_predictions.html", {"predictions": predictions})


def admin_view_results(request):
    from users.utility import ProcessLiverDiseas

    lg_accuracy, lg_precision, lg_sensitivity, lg_specificity = ProcessLiverDiseas.start_logistic_regression()
    svm_accuracy, svm_precision, svm_sensitivity, svm_specificity = ProcessLiverDiseas.start_svm()

    dt_accuracy, dt_precision, dt_sensitivity, dt_specificity = ProcessLiverDiseas.start_decision_tree()
    rf_accuracy, rf_precision, rf_sensitivity, rf_specificity = ProcessLiverDiseas.start_random_forest()
    knn_accuracy, knn_precision, knn_sensitivity, knn_specificity = ProcessLiverDiseas.start_knn()

    lg = {
        "accuracy": lg_accuracy,
        "precision": lg_precision,
        "sensitivity": lg_sensitivity,
        "specificity": lg_specificity
    }

    svm = {
        "accuracy": svm_accuracy,
        "precision": svm_precision,
        "sensitivity": svm_sensitivity,
        "specificity": svm_specificity
    }

    dt = {
        "accuracy": dt_accuracy,
        "precision": dt_precision,
        "sensitivity": dt_sensitivity,
        "specificity": dt_specificity
    }

    rf = {
        "accuracy": rf_accuracy,
        "precision": rf_precision,
        "sensitivity": rf_sensitivity,
        "specificity": rf_specificity
    }

    knn = {
        "accuracy": knn_accuracy,
        "precision": knn_precision,
        "sensitivity": knn_sensitivity,
        "specificity": knn_specificity
    }

    return render(request, "admins/reports.html", {
        "lg": lg,
        "svm": svm,
        "dt": dt,
        "rf": rf,
        "knn": knn
    })