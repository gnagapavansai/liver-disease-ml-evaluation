from django.contrib import admin
from django.urls import path
from EvaluationLiverDiseasePrediction import views as mainView
from admins import views as admins
from users import views as usr
from admins.models import Prediction
from users.utility import ProcessLiverDiseas

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", mainView.index, name="index"),
    path("AdminLogin/", mainView.AdminLogin, name="AdminLogin"),
    path("UserLogin/", mainView.UserLogin, name="UserLogin"),
    path("UserRegister/", mainView.UserRegister, name="UserRegister"),

    # Adminviews
    path("AdminLoginCheck/", admins.AdminLoginCheck, name="AdminLoginCheck"),
    path("AdminHome/", admins.AdminHome, name="AdminHome"),
    path('RegisterUsersView/', admins.RegisterUsersView, name='RegisterUsersView'),
    path('ActivaUsers/', admins.ActivaUsers, name='ActivaUsers'),
    path('admin_view_results/', admins.admin_view_results, name='admin_view_results'),

    # NEW Prediction URLs
    path("predict_liver_disease/", admins.predict_liver_disease, name="predict_liver_disease"),
    path("admin_view_predictions/", admins.admin_view_predictions, name="admin_view_predictions"),

    # User Views
    path("UserRegisterActions/", usr.UserRegisterActions, name="UserRegisterActions"),
    path("UserLoginCheck/", usr.UserLoginCheck, name="UserLoginCheck"),
    path("UserHome/", usr.UserHome, name="UserHome"),
    path("PreProcess/", usr.PreProcess, name="PreProcess"),
    path("View_Data/", usr.View_Data, name="View_Data"),
    path("ML/", usr.ML, name="ML"),
    path("MLResult/", usr.MLResult, name="MLResult"),
    path("user_classification_results/", usr.user_classification_results, name="user_classification_results"),


]