from django.shortcuts import render
from django.http import JsonResponse
import cv2
import numpy as np
import face_recognition
from .face_recognition_service import recognize_face
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io

def home_view(request):
    return render(request, 'home.html')

@csrf_exempt  
def face_recognition_view(request):
    if request.method == "POST":
        if 'image' not in request.FILES:
            return JsonResponse({"error": "No image provided"}, status=400)

        # Convert image to OpenCV format
        image_file = request.FILES['image']
        image = Image.open(io.BytesIO(image_file.read()))
        frame = np.array(image)

        # Recognize face
        processed_frame, recognized_name = recognize_face(frame)

        return JsonResponse({"recognized_name": recognized_name})

    return JsonResponse({"error": "Invalid request"}, status=400)
