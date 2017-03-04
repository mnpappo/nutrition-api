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


import scipy.misc
from PIL import Image
from scipy.ndimage.interpolation import zoom
import numpy as np

from .predict import predict_from_model

def get_pred(full_filename):
    img = np.array(Image.open(full_filename).convert('RGB'))
    # img = img.reshape((3,512,512))
    img = scipy.misc.imresize(img, (64,64,3))
    img = np.rollaxis(img, 2, 0)

    return predict_from_model(img)

class PhotoList(APIView):

    def get(self, request, format=None):
        pass

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

            result = get_pred(full_filename)
            veg_index = np.argmax(result)

            return Response({'key': result, veg_index:veg_index}, status=status.HTTP_201_CREATED)
        except Exception as inst:
            raise inst
            return Response({'key': 'NOT SAVED'}, status=status.HTTP_201_CREATED)

        return Response({'key': 'value'}, status=status.HTTP_201_CREATED)



class PhotoDetail(APIView):
    pass
