# zomark/models.py

from django.db import models
from accounts.models import ZomarkUser

class Image(models.Model):
    user = models.ForeignKey(ZomarkUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    watermarked_image = models.ImageField(upload_to='watermarked_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
