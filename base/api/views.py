from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Bill
from .serializers import BillSerializer
from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/bills',
        'GET /api/bills/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getBills(request):
    bills = Bill.objects.all()
    serializer = BillSerializer(bills, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getBill(request, pk):
    bill = Bill.objects.get(id=pk)
    serializer = BillSerializer(bill, many=False)
    return Response(serializer.data)
