import os
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
import mimetypes

def serve_protected_document(request, file):
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename=" + file
    response["Content-Type"] = mimetypes.guess_type(file)
    # nginx uses this path to serve the file
    response["X-Accel-Redirect"] = os.path.join("/files/", file) # path to file
    return response