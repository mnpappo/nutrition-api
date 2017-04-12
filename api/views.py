import numpy as np
np.random.seed(1337)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import base64
import os
from django.core.files import File
from .models import MyPhoto
from .serializers import PhotoSerializer
from rest_framework import status
from django.http import Http404
from django.core.files.base import ContentFile
from django.http import HttpResponse

import scipy.misc
from PIL import Image
from scipy.ndimage.interpolation import zoom
import numpy as np

from .predict import predict_from_model


def index(request):
    return HttpResponse("Hello, world.")


def api_test(request):
    return HttpResponse("One more step :)")



def get_pred(full_filename):
    # Image.open(full_filename).convert('RGB').show()
    img = np.array(Image.open(full_filename).convert('RGB'))
    print(img.shape)

    # img = img.reshape((3,512,512))
    img = scipy.misc.imresize(img, (128,128,3))
    print(img.shape)
    # img = np.rollaxis(img, 2, 0)


    return predict_from_model(img)

class PhotoList(APIView):

    def get(self, request, format=None):
        return Response({'key': 'value'}, status=status.HTTP_201_CREATED)

    def post(self,request,format=None):
        folder = 'predic_images/' #request.path.replace("/", "_")
        uploaded_filename = request.FILES['file'].name
        BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # create the folder if it doesn't exist.
        try:
            os.mkdir(os.path.join(BASE_PATH, folder))
        except:
            pass

        # save the uploaded file inside that folder.
        full_filename = os.path.join(BASE_PATH, folder, uploaded_filename)
        fout = open(full_filename, 'wb+')

        file_content = ContentFile( request.FILES['file'].read() )

        try:
            # Iterate through the chunks.
            for chunk in file_content.chunks():
                fout.write(chunk)
            fout.close()

            allpreds, veg_index, veg_name = get_pred(full_filename)

            os.remove(full_filename)

            return Response({'key': allpreds, 'veg_index' : veg_index, 'veg_name' : veg_name}, status=status.HTTP_201_CREATED)
        except Exception as inst:
            raise inst
            return Response({'key': 'NOT SAVED'}, status=status.HTTP_201_CREATED)

        return Response({'key': 'value'}, status=status.HTTP_201_CREATED)



class PhotoDetail(APIView):
    pass
