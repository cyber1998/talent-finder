import os

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response as JSONResponse

from talent.helpers import process_resume


# Create your views here.



@api_view(['POST'])
def upload_resume(request):
    resume_file = request.FILES.get('resume')
    if not resume_file:
        return JSONResponse({'error': 'No file was uploaded'}, status=400)

    if not resume_file.name.endswith('.pdf'):
        return JSONResponse({'error': 'Only PDF files are supported'}, status=400)

    # store the file under the files directory / AWS S3


    if os.environ.get('EXEC_ENV') == 'local':
        # Create a resumes directory if it does not exist. Later we can change this to a S3 bucket.
        if not os.path.exists('resumes'):
            os.makedirs('resumes')

        with open(f'resumes/{resume_file.name}', 'wb') as f:
            f.write(resume_file.read())
            f_path = f.name

    else:
        pass

    success = process_resume(f_path)

    if not success:
        return JSONResponse({'error': 'An error occurred while processing the resume'}, status=500)

    return JSONResponse({'success': True}, status=200)

