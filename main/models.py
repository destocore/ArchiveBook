from django.db import models
from django.conf import settings
import os

class Note(models.Model):
    def get_upload_path(instance, filename):
        return os.path.join('notes', instance.subj, filename)

    def get_folder_choices():
        path = os.path.join(settings.MEDIA_ROOT, 'notes')
        if not os.path.exists(path):
            return [('notes', 'notes')]
        
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        return [(f, f) for f in folders]

    subj = models.CharField(
        max_length=100, 
        choices=get_folder_choices(),
        verbose_name="Папка предмета"
    )

    file = models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return f"{self.subj} - {self.file.name}"
