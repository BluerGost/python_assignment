from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.FinancialDataListAPIView.as_view())    
]
