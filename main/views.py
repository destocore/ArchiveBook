from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from django.conf import settings

import os

def main(req):
    if req.method == "POST":
        pos = req.POST.get('pos')
        typ = req.POST.get('typ')    
        return redirect(f'/find/{typ}/{pos}/')
    return render(req, 'index.html', {"lp": [f for f in os.listdir(os.path.join(settings.MEDIA_ROOT, 'notes'))]})



def find(req, typ:str,topic:str):
    if req.method == "POST":
        pos = req.POST.get('pos')
        typ_raw = req.POST.get('typ')

        if pos and typ_raw:
            return redirect(f'/find/{typ}/{pos}/')
    files = [f for f in os.listdir(os.path.join(settings.MEDIA_ROOT, 'notes', typ)) if topic.lower() in f.lower() and f.endswith('.pdf')]
    if len(files) == 1 and topic.lower() == files[0].replace('.pdf', '').lower():
        return redirect(f"/media/notes/{typ}/{files[0]}")
    else:
        return render(req, 'find.html', {'topic': topic, 'files': files, 'typ': typ, "lp": [f for f in os.listdir(os.path.join(settings.MEDIA_ROOT, 'notes'))]})

def mediaN(req, typ:str, topic:str):
    clean_topic = topic.strip('/') 
    
    path = os.path.join(settings.MEDIA_ROOT, 'notes', typ, clean_topic)
    
    if os.path.exists(path):
        return FileResponse(open(path, 'rb'))
    
    return redirect('/')

def media(req, path:str):
    full_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, path))
    if not full_path.startswith(str(settings.MEDIA_ROOT)):
        raise Http404()

    if os.path.exists(full_path):
        if req.user.is_superuser:
            return FileResponse(open(full_path, 'rb'))
        if path.startswith(('admin/', 'secret/')):
            raise Http404()
        try:
            return FileResponse(open(full_path, 'rb'))
        except:
            raise Http404()
    
    raise Http404()