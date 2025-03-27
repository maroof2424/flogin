# from django.shortcuts import render
# import base64
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.base import ContentFile
# from .models import *


# # Create your views here.

# @csrf_exempt
# def register(request):
#     if request.method =="POST":
#         username = request.POST.get('username')
#         face_image_data = request.POST['face_image']
#         face_image_data = face_image_data.split(",")[1]
#         face_image = ContentFile(base64.b64decode(face_image_data),name = f"{username}_.jpg")
#         print(face_image)
#         try:
#             user = User.objects.create(username = username)
#         except Exception as e:
#             return JsonResponse({
#             "status":"error",
#             "message":"Username already taken",
#         })
#         UserImage.object.create(user = user, face_image = face_image)
#         return JsonResponse({
#             "status":"sucess",
#             "message":"User registered successfully",
#         })
#     return render(request, 'register.html')

from django.shortcuts import render
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import User, UserImage
from django.db import IntegrityError
import face_recognition

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        face_image_data = request.POST.get('face_image')

        if not username or not face_image_data:
            return JsonResponse({
                "status": "error",
                "message": "Username and face image are required",
            }, status=400)

        try:
            # Decode Base64 image
            if "," in face_image_data:
                face_image_data = face_image_data.split(",")[1]  # Remove metadata if present
            
            face_image = ContentFile(base64.b64decode(face_image_data), name=f"{username}.jpg")

            # Create User
            user = User.objects.create(username=username)

            # Save Image
            UserImage.objects.create(user=user, face_image=face_image)

            return JsonResponse({
                "status": "success",
                "message": "User registered successfully",
            })

        except IntegrityError:
            return JsonResponse({
                "status": "error",
                "message": "Username already taken",
            }, status=400)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e),
            }, status=500)

    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        face_image_data = request.POST['face_image']

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "User not found",
            })
        face_image_data = face_image_data.split(",")[1]
        uploaded_image = face_image = ContentFile(base64.b64decode(face_image_data), name=f"{username}.jpg")

        uploaded_face_image = face_recognition.load_image_file(uploaded_image)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_face_image)
        if uploaded_face_encoding:
            uploaded_face_encoding = uploaded_face_encoding[0]
            use_image = UserImage.objects.filter(user = user).last()
            stored_face_image = face_recognition.load_image_file(user_image.face_image.path)
            stored_face_encoding = face_recognition.face_encodings(uploaded_face_image)

            match = face_recognition.compare_faces([stored_face_encoding],uploaded_face_encoding)
            if match[0]:
                return JsonResponse({
                    "status": "success",
                    "message": "Login successful",
                })
        return JsonResponse({
                "status": "error",
                "message": "not found",
            })
    return render(request,"login.html")