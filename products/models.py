from django.db import models
from django.core.validators import MinLengthValidator

from django.utils.text import slugify


class Catagories(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Enter a catagorie (e.g. Electronics)',
        validators=[MinLengthValidator(
            2, "Make must be greater than 1 character")]
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Products(models.Model):
    product_name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Write the name of the product")]
    )
    price = models.FloatField()
    discription = models.CharField(max_length=600)
    Catagorie = models.ForeignKey(
        'Catagories', on_delete=models.CASCADE, null=False)

    image = models.ImageField(upload_to="media/photos/")

    # Shows up in the admin list
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
