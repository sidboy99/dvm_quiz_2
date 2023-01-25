from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    choices = [
        ('QM', 'QM'),
        ('QT', 'QT'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    user_type = models.CharField(default='QT', choices=choices, max_length=2)

    def __str__(self):
        return f'{self.user.username} {self.user_type} Profile'

    def save(self):
        super().save() # runs the save method from the parent class

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


