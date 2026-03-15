from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os
import uuid

from . import utils

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def classify_image(request):
    if request.method == 'POST':

        if request.FILES.get('image'):
            try:
                image_file = request.FILES['image']

                file_ext = os.path.splitext(image_file.name)[1]
                filename = f"{uuid.uuid4()}{file_ext}"

                file_path = default_storage.save(f'uploads/{filename}', image_file)
                full_path = default_storage.path(file_path)

                # call MODEL function
                result = utils.classify_image(full_path)

                if os.path.exists(full_path):
                    os.remove(full_path)

                return JsonResponse(result)

            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })

        return JsonResponse({'success': False, 'error': 'No image provided'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})