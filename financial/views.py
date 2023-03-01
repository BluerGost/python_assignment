import json

from django.shortcuts import render
from django.http import JsonResponse

from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import FinancialDataModel
from .serializers import FinancialDataSerializer

# Create your views here.
@api_view(["GET"])
def get_financial_data(request, *args, **kwargs):
    """
    DRF API View
    """
    instance = FinancialDataModel.objects.all().order_by("?").first()
    print(f'Came HERE(1)')
    data = {}

    if instance:
        # data = model_to_dict(model_data, fields=['symbol', 'date', 'open_price', 'close_price', 'volume'])
        data = FinancialDataSerializer(instance).data
    print(f'Came HERE(2)')

    return Response(data)