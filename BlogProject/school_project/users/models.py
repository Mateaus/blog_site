from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
# database for profiles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#delete everything if user deleted
    image = models.ImageField(default='default.png', upload_to='profile_pics') #insert default.jpg as default

    # returns the username in the query
    def __str__(self):
        return f'{self.user.username} Profile'

    # handles the way an image is being saved
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        # resize images if they are bigger than 300x300
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('profile-view', kwargs={'pk':self.pk})
