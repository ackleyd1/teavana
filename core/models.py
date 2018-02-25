import uuid

from django.db import models, DataError
from django.utils.text import slugify
from django.urls import reverse

def tea_image_upload(instance, filename):
    ext = filename.split('.')[-1]
    return 'teas/{}.{}'.format(instance.slug, ext)

class TimeStampedModel(models.Model):
    """Abstract model for inheriting created and updated fields."""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tea(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(db_index=True, max_length=128, blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to=tea_image_upload)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tea-detail', kwargs={'pk': self.id })

    def save(self, *args, **kwargs):
        """Override save method to update unique slug based on the other fields."""
        slug = slugify(self.name)
        if Tea.objects.filter(slug=slug).exclude(id=self.id).exists():
            raise DataError('Tea with slug: {} already exists'.format(slug))
        else:
            self.slug = slug
        super().save(*args, **kwargs)
