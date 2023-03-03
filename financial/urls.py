from django.urls import path
from . import views

urlpatterns = [
    path(route='financial_data/', view=views.FinancialDataListAPIView.as_view()),
    path(route='statistics/', view=views.StatisticsAPIView.as_view())  
]
