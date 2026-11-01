from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

from .forms import UserRegistrationForm
from .models import UserRegistrationModel

# ADD THIS IMPORT
from admins.models import Patient, Prediction


# User Registration
def UserRegisterActions(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()

            return render(request, 'UserRegistrations.html', {'form': form})

        else:
            messages.success(request, 'Email or Mobile Already Existed')

    else:
        form = UserRegistrationForm()

    return render(request, 'UserRegistrations.html', {'form': form})


# User Login
def UserLoginCheck(request):

    if request.method == "POST":

        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')

        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)

            status = check.status

            if status == "activated":

                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email

                return render(request, 'users/UserHomePage.html', {})

            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')

        except:
            messages.success(request, 'Invalid Login id and password')

    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


# PreProcessing
def PreProcess(request):

    import pandas as pd
    import os
    from django.conf import settings

    path = os.path.join(settings.MEDIA_ROOT, 'indian_liver_patient.csv')

    data = pd.read_csv(path)

    data['Dataset'] = data['Dataset'].map({2: 0, 1: 1})

    data['Albumin_and_Globulin_Ratio'].fillna(value=0, inplace=True)

    data_num_features = data.drop(['Gender', 'Dataset'], axis=1)

    return render(request, 'PreProcess.html', {"data": data_num_features.to_html})


# View Dataset
def View_Data(request):

    import pandas as pd
    import os
    from django.conf import settings

    path = os.path.join(settings.MEDIA_ROOT, 'indian_liver_patient.csv')

    df = pd.read_csv(path)

    df = df[['Age','Gender','Total_Bilirubin','Direct_Bilirubin',
             'Alkaline_Phosphotase','Alamine_Aminotransferase',
             'Aspartate_Aminotransferase','Total_Protiens',
             'Albumin','Albumin_and_Globulin_Ratio']]

    df = df.head(584).to_html(classes='table-sm')

    return render(request, 'users/readDataset.html', {'data': df})


# ML Page
def ML(request):
    return render(request, 'users/ML.html')


# ML Prediction
def MLResult(request):

    if request.method == "POST":

        import pandas as pd
        from django.conf import settings
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score

        age = float(request.POST.get('age'))
        gender = float(request.POST.get('gender'))

        Total_Bilirubin = float(request.POST.get('Total_Bilirubin'))
        Direct_Bilirubin = float(request.POST.get('Direct_Bilirubin'))
        Alkaline_Phosphotase = float(request.POST.get('Alkaline_Phosphotase'))

        Alamine_Aminotransferase = float(request.POST.get('Alamine_Aminotransferase'))
        Aspartate_Aminotransferase = float(request.POST.get('Aspartate_Aminotransferase'))

        Total_Protiens = float(request.POST.get('Total_Protiens'))
        Albumin = float(request.POST.get('Albumin'))
        Albumin_and_Globulin_Ratio = float(request.POST.get('Albumin_and_Globulin_Ratio'))

        path = settings.MEDIA_ROOT + "\\" + "indian_liver_patient.csv"

        data = pd.read_csv(path)

        # Convert labels
        data['Dataset'] = data['Dataset'].map({1:1, 2:0})

        # Handle missing values
        data.fillna(data.mean(), inplace=True)

        X = data.drop('Dataset', axis=1)
        y = data['Dataset']

        # Convert Gender column
        X['Gender'] = X['Gender'].map({'Male':1, 'Female':0})

        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )

        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()

        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight='balanced'
        )

        model.fit(X_train, y_train)

        test_set = [[
            age,
            gender,
            Total_Bilirubin,
            Direct_Bilirubin,
            Alkaline_Phosphotase,
            Alamine_Aminotransferase,
            Aspartate_Aminotransferase,
            Total_Protiens,
            Albumin,
            Albumin_and_Globulin_Ratio
        ]]

        test_set = scaler.transform(test_set)

        y_pred = model.predict(test_set)

        prediction = y_pred[0]

        accuracy = accuracy_score(y_test, model.predict(X_test))
        accuracy = round(accuracy * 100, 2)

        if prediction == 1:
            msg = "Liver Disease Detected"
        else:
            msg = "No Liver Disease Detected"

        algorithm = "Random Forest"

        # SAVE PATIENT DATA
        patient = Patient.objects.create(
            age=age,
            gender=gender,
            total_bilirubin=Total_Bilirubin,
            direct_bilirubin=Direct_Bilirubin,
            alkaline_phosphotase=Alkaline_Phosphotase,
            alamine_aminotransferase=Alamine_Aminotransferase,
            aspartate_aminotransferase=Aspartate_Aminotransferase,
            total_proteins=Total_Protiens,
            albumin=Albumin,
            albumin_globulin_ratio=Albumin_and_Globulin_Ratio
        )

        # SAVE PREDICTION RESULT
        Prediction.objects.create(
            patient=patient,
            algorithm_used=algorithm,
            prediction_result=msg,
            accuracy=accuracy
        )

        return render(request,'users/ML.html',{
            'msg': msg,
            'algorithm': algorithm,
            'accuracy': accuracy
        })

# Classification Report
def user_classification_results(request):

    from .utility import ProcessLiverDiseas

    lg_accuracy, lg_precision, lg_sensitivity, lg_specificity = ProcessLiverDiseas.start_logistic_regression()

    svm_accuracy, svm_precision, svm_sensitivity, svm_specificity = ProcessLiverDiseas.start_svm()

    dt_accuracy, dt_precision, dt_sensitivity, dt_specificity = ProcessLiverDiseas.start_decision_tree()

    rf_accuracy, rf_precision, rf_sensitivity, rf_specificity = ProcessLiverDiseas.start_random_forest()

    knn_accuracy, knn_precision, knn_sensitivity, knn_specificity = ProcessLiverDiseas.start_knn()


    lg = {
        "accuracy": round(lg_accuracy*100,2),
        "precision": round(lg_precision,2),
        "sensitivity": round(lg_sensitivity,2),
        "specificity": round(lg_specificity,2)
    }

    svm = {
        "accuracy": round(svm_accuracy*100,2),
        "precision": round(svm_precision,2),
        "sensitivity": round(svm_sensitivity,2),
        "specificity": round(svm_specificity,2)
    }

    dt = {
        "accuracy": round(dt_accuracy*100,2),
        "precision": round(dt_precision,2),
        "sensitivity": round(dt_sensitivity,2),
        "specificity": round(dt_specificity,2)
    }

    rf = {
        "accuracy": round(rf_accuracy*100,2),
        "precision": round(rf_precision,2),
        "sensitivity": round(rf_sensitivity,2),
        "specificity": round(rf_specificity,2)
    }

    knn = {
        "accuracy": round(knn_accuracy*100,2),
        "precision": round(knn_precision,2),
        "sensitivity": round(knn_sensitivity,2),
        "specificity": round(knn_specificity,2)
    }


    return render(request,"users/classification_report.html",{
        "lg":lg,
        "svm":svm,
        "dt":dt,
        "rf":rf,
        "knn":knn
    })