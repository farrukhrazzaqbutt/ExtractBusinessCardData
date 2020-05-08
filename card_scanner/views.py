from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from card_scanner.models import ScanCard
from card_scanner.serializers import ScanCardSerializer
from rest_framework.decorators import api_view
from card_scanner.cardInfo import extractInfo
import requests


# Create your views here.
def index(request):
    parameters = {"lat": 40.71, "lon": -74}
    response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
    print(response.content)
    return render(request, 'index.html', {})


@api_view(['GET', 'POST', 'DELETE'])
def card_scanner_list(request):
    # GET list of ScanCard, POST a new ScanCard, DELETE all ScanCard
    if request.method == 'GET':
        ScanCardData = ScanCard.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            ScanCardData = ScanCard.objects.filter(title__icontains=title)
        ScanCard_serializer = ScanCardSerializer(ScanCardData, many=True)
        print(ScanCard_serializer.data)
        return JsonResponse(ScanCard_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        ScanCard_data = JSONParser().parse(request)
        print(ScanCard_data)
        ScanCard_serializer = ScanCardSerializer(data=ScanCard_data)
        if ScanCard_serializer.is_valid():
            ScanCard_serializer.save()
            data = ScanCard.objects.last()
            ImageUrl = data.image
            extractData = extractInfo(ImageUrl)
            obj = ScanCard.objects.get(id=data.id)
            obj.mobile = (extractData['mobile'])
            obj.email = (extractData['email'])
            obj.description = (extractData['output'])
            obj.save()
            return JsonResponse(ScanCard_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(ScanCard_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = ScanCard.objects.all().delete()
        return JsonResponse({'message': '{} ScanCard Records were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def card_scanner_detail(request, pk):
    # GET / PUT / DELETE ScanCard by pk (id)
    try:
        ScanCardDataPK = ScanCard.objects.get(pk=pk)
        if request.method == 'GET':
            ScanCard_serializer = ScanCardSerializer(ScanCardDataPK)
            return JsonResponse(ScanCard_serializer.data)
        elif request.method == 'PUT':
            ScanCard_data = JSONParser().parse(request)
            ScanCard_serializer = ScanCardSerializer(ScanCardDataPK, data=ScanCard_data)
            if ScanCard_serializer.is_valid():
                ScanCard_serializer.save()
                return JsonResponse(ScanCard_serializer.data)
            return JsonResponse(ScanCard_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            ScanCardDataPK.delete()
            return JsonResponse({'message': 'ScanCard Record was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except ScanCard.DoesNotExist:
        return JsonResponse({'message': 'The ScanCard does not exist'}, status=status.HTTP_404_NOT_FOUND)


