import json

from django.shortcuts import render
from django.http import JsonResponse

from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination

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

#https://www.django-rest-framework.org/api-guide/filtering/#api-guide
# https://www.django-rest-framework.org/api-guide/requests/

class FinancialDataListAPIView(generics.ListAPIView):
    queryset = FinancialDataModel.objects.all()
    serializer_class = FinancialDataSerializer

    def get_queryset(self):
        queryset = FinancialDataModel.objects.all()

        # Filter by symbol if the symbol parameter is provided
        symbol = self.request.query_params.get('symbol')
        if symbol:
            queryset = queryset.filter(symbol=symbol)

        # Filter by start_date if the start_date parameter is provided
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#gte
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        # Filter by end_date if the end_date parameter is provided
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Pagination
        limit = request.query_params.get('limit', 5)
        paginator = Paginator(queryset, limit)
        page = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page)

        # Serializing the data and creating the response
        serializer = self.get_serializer(page_obj, many=True)

        response_data = {
            'data': serializer.data,
            'pagination': {
                'count': paginator.count,
                'page': page_obj.number,
                'limit': int(limit),
                'pages': paginator.num_pages
            },
            'info': {'error': ''}
        }

        return Response(response_data)
    
# class CustomPagination(PageNumberPagination):
#     page_size = 5
#     page_query_param = 'page'
