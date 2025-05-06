from django.db import models

# Create your models here.
from django.utils.text import slugify


class Products(models.Model):
    # ... existing fields ...
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)
