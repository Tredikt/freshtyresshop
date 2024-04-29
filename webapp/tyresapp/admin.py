from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from django.core.files.base import ContentFile
from .models import Tyre, TyreImage
from .config import access_token

from requests import request
import requests
import random
import string


@admin.action(description="TEST")
def test(modeladmin: admin.ModelAdmin, user_request: HttpRequest, queryset: QuerySet):
    tyre = Tyre()
    new_photo = TyreImage()
    new_photo.tyre_id = 2


@admin.action(description="import tyres")
def import_tyres(modeladmin: admin.ModelAdmin, user_request: HttpRequest, queryset: QuerySet):
    response = request(
        "GET",
        "https://api.moysklad.ru/api/remap/1.2/entity/assortment",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept-Encoding": "gzip"
        }
    )

    tyres = Tyre.objects.all()
    codes = []
    for elem in tyres:
        codes.append(elem.code)
    for data in response.json()["rows"]:
        name = data["name"]

        if name[:4] != "Тест" and "code" in data.keys():
            code = data["code"]
            attributes = data["attributes"]
            if code not in codes:
                status = attributes[4]["value"]
                if status.lower() != "оплачено/выдано":
                    if status.lower() in ["отличное", "плохое", "среднее", "хорошее", "нормальное"]:
                        status = attributes[5]["value"]
                try:
                    attributes = data["attributes"]
                except KeyError:
                    continue

                price = data.get("salePrices")
                if price is not None:
                    price = price[0]["value"]

                if code in codes:
                    continue
                else:
                    wheels_or_tires = attributes[0]["value"]
                    if "колеса" in wheels_or_tires.lower() or "колёса" in wheels_or_tires.lower() or "колес" in wheels_or_tires.lower() or "резина" in wheels_or_tires.lower() or "диск" in wheels_or_tires.lower():
                        # print(code, attributes)
                        brand_model = attributes[1]["value"]
                        season = attributes[2]["value"]
                        tire_parameters = attributes[3]["value"]
                        status = attributes[5]["value"]
                        google_disk_link = None

                        if status.lower() != "оплачено/выдано":
                            if status.lower() in ["отличное", "плохое", "среднее", "хорошее", "нормальное", "средние"]:
                                status = attributes[6]["value"]

                            storage = None
                            stage = None
                            disk_parameters = None
                            for num in range(3, 14):
                                try:
                                    if attributes[num]["name"] == "Склад":
                                        storage = attributes[num]["value"]["name"]
                                    elif attributes[num]["name"] == "Ссылка на фотографии":
                                        google_disk_link = attributes[num]["value"]
                                    elif attributes[num]["name"] == "Состояние":
                                        stage = attributes[num]["value"]
                                    elif attributes[num]["name"] == "Цена продажи для магазина":
                                        price = attributes[num]["value"]
                                    elif attributes[num]["name"] == "Остаток протектора":
                                        tread_remain = attributes[num]["value"]
                                    elif attributes[num]["name"] == "Параметры дисков":
                                        disk_parameters = attributes[num]["value"]
                                except IndexError:
                                    continue
                            photo_url = data["images"]["meta"]["href"]

                            try:
                                photo_download = request("GET", photo_url,
                                                         headers={"Authorization": f"Bearer {access_token}"}).json()

                            except requests.exceptions.ReadTimeout:
                                continue

                            if len(photo_download["rows"]) > 0:
                                photo = request("GET", photo_download["rows"][0]["meta"]["downloadHref"],
                                                headers={"Authorization": f"Bearer {access_token}"}).content

                                if (status.lower() in ["принят", "подтвержден",
                                                       "подтверждён", "принято",
                                                       "подтверждено"] and price is not None and price > 0 and
                                        str(code) not in codes and storage is not None):
                                    tyre = Tyre.objects.create(
                                        name=name,
                                        code=code,
                                        model=brand_model,
                                        season=season,
                                        location=storage,
                                        tyres_parameters=tire_parameters,
                                        disks_parameters=disk_parameters,
                                        price=price,
                                        stage=stage,
                                        status="stock",
                                        tread_remain=tread_remain
                                    )

                                    new_photo = TyreImage()
                                    filename = f"{''.join(random.choice(string.ascii_letters) for _ in range(8))}.png"
                                    new_photo.tyre_id = tyre.pk
                                    new_photo.image.save(filename, ContentFile(photo), save=True)
                                    new_photo.save()

                        elif wheels_or_tires.lower() in ["шины", "шина"]:
                            brand_model = attributes[1]["value"]
                            season = attributes[2]["value"]
                            tire_parameters = attributes[3]["value"]
                            status = attributes[4]["value"]

                            storage = None
                            google_disk_link = None
                            stage = None
                            for num in range(3, 14):
                                try:
                                    if attributes[num]["name"] == "Склад":
                                        storage = attributes[num]["value"]["name"]
                                    elif attributes[num]["name"] == "Ссылка на фотографии":
                                        google_disk_link = attributes[num]["value"]
                                    elif attributes[num]["name"] == "Состояние":
                                        stage = attributes[num]["value"]
                                    elif attributes[num]["name"] == "Цена продажи для магазина":
                                        price = attributes[num]["value"]
                                    elif attributes[num]["name"] == "Остаток протектора":
                                        tread_remain = attributes[num]["value"]
                                except IndexError:
                                    continue
                            photo_url = data["images"]["meta"]["href"]
                            try:
                                photo_download = request("GET", photo_url,
                                                         headers={"Authorization": f"Bearer {access_token}"}).json()

                            except requests.exceptions.ReadTimeout:
                                continue

                            if len(photo_download["rows"]) > 0:
                                photo = request("GET", photo_download["rows"][0]["meta"]["downloadHref"],
                                                headers={"Authorization": f"Bearer {access_token}"}).content
                                if status.lower() in ["принят", "подтвержден",
                                                      "подтверждён", "принято",
                                                      "подтверждено"] and price is not None and price > 0 and str(
                                    code) not in codes and storage is not None:
                                    tyre = Tyre.objects.create(
                                        name=name,
                                        code=code,
                                        model=brand_model,
                                        season=season,
                                        location=storage,
                                        tyres_parameters=tire_parameters,
                                        disks_parameters=None,
                                        price=price,
                                        stage=stage,
                                        status="stock",
                                        tread_remain=tread_remain
                                    )

                                    new_photo = TyreImage()
                                    filename = f"{''.join(random.choice(string.ascii_uppercase) for _ in range(8))}.png"
                                    new_photo.tyre_id = tyre.pk
                                    new_photo.image.save(filename, ContentFile(photo), save=True)
                                    new_photo.save()



@admin.register(Tyre)
class TyreProduct(admin.ModelAdmin):
    actions = [
        import_tyres,
        test
    ]

    list_display = "pk", "code", "model", "tyres_parameters", "disks_parameters", "tread_remain", "stage", "season", "status", "location"
    list_display_links = "pk", "code"

