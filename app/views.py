from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from serializers import SudokuImageSerializer

from PIL import Image
import numpy as np

from snapsudoku.sudoku import snap_sudoku

def index(request):
    return HttpResponse("Hello, world!")


@api_view(['POST'])
def solve(request):
    serializer = SudokuImageSerializer(data=request.data)
    print ("Here")
    if serializer.is_valid():
        serializer.save()
        im = Image.open(request.data['image'].file)
        color_img = np.asarray(im)
        return JsonResponse(snap_sudoku(color_img))
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
