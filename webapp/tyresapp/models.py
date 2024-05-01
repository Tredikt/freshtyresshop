from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
# Create your models here.


def tyre_preview_directory_path(instance: "TyreImage", filename: str) -> str:
    return "tyres/tyre{pk}/preview/{filename}".format(
        pk=instance.tyre.pk,
        filename=filename
    )


class Tyre(models.Model):
    code = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    tyres_parameters = models.CharField(max_length=100)
    disks_parameters = models.CharField(max_length=100, null=True)
    tread_remain = models.CharField(max_length=100)
    stage = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default=0)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tyre(pk={self.pk}, name={self.name!r})"

    def get_absolute_url(self):
        return reverse("tyresapp:tyre_details", kwargs={"pk": self.pk})


def tyre_images_directory_path(instance: "TyreImage", filename: str) -> str:
    return "tyres/tyre_{pk}/images/{filename}".format(
        pk=instance.tyre.pk,
        filename=filename
    )


class TyreImage(models.Model):
    tyre = models.ForeignKey(Tyre, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=tyre_preview_directory_path)


class Order(models.Model):
    tg_id = models.IntegerField(default=0)
    tyre_id = models.IntegerField(default=0)
