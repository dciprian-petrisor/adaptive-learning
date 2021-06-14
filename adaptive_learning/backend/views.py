import os
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def serve_protected_document(request, file):
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename=" + file
    # nginx uses this path to serve the file
    response["X-Accel-Redirect"] = os.path.join("/files/", file) # path to file
    return response