from django.db import models
from django.contrib.auth.models import User

IMAGE_STYLES = [
    ("no_style", "No Style"),
    ("photo", "Photo"),
    ("illustration", "Illustration"),
    ("3d", "3D"),
    ("cartoon_fun", "Cartoon Fun"),
    ("comic", "Comic"),
    ("dark", "Dark"),
    ("watercolor", "Watercolor"),
    ("pixel_art", "Pixel Art"),
    ("oil_painting", "Oil Painting"),
    ("nature", "Nature"),
    ("ink_print", "Ink Print"),
    ("pencil", "Pencil"),
    ("retrowave", "Retrowave"),
]

class GeneratedImage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="generated_images",
    )
    prompt = models.TextField()
    style = models.CharField(max_length=50, choices=IMAGE_STYLES)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.style} - {self.prompt[:20]}"

VIDEO_STYLE_CHOICES = (
    ("cinematic", "Cinematic"),
    ("fantasy", "Fantasy"),
    ("documentary", "Documentary"),
)


class GeneratedVideo(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="generated_video",
    )
    prompt=models.TextField()
    style = models.CharField(max_length=50, choices=VIDEO_STYLE_CHOICES)
    video_url=models.URLField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.prompt[:20]}"
    
