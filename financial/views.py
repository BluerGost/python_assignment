import json

from django.shortcuts import render
from django.http import JsonResponse

from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from .models import FinancialDataModel
from .serializers import FinancialDataSerializer

# Create your views here.
# @api_view(["GET"])
# def get_financial_data(request, *args, **kwargs):
#     """
#     DRF API View
#     """
#     instance = FinancialDataModel.objects.all().order_by("?").first()
#     data = {}

#     if instance:
#         # data = model_to_dict(model_data, fields=['symbol', 'date', 'open_price', 'close_price', 'volume'])
#         data = FinancialDataSerializer(instance).data

#     return Response(data)

class FinancialDataListAPIView(generics.ListAPIView):
    queryset = FinancialDataModel.objects.all()
    serializer_class = FinancialDataSerializer
    