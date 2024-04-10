from requests import request
import requests


from webapp.tyresapp.models import Tyre

access_token = "80e9d6f8d66283f2d16b974666020bf46ae83d7a"

response = request(
    "GET",
    "https://api.moysklad.ru/api/remap/1.2/entity/assortment",
    headers={
        "Authorization": f"Bearer {access_token}",
        "Accept-Encoding": "gzip"
    }
)

codes = Tyre.objects.only("code").all()
for data in response.json()["rows"]:
    name = data["name"]

    if name[:4] != "Тест" and "code" in data.keys():
        code = data["code"]
        attributes = data["attributes"]


        # if code not in codes:
        #     try:
        #         attributes = data["attributes"]
        #     except KeyError:
        #         continue
        #
        #     price = data.get("salePrices")
        #     if price is not None:
        #         price = price[0]["value"]
        #
        #     if code in codes:
        #         continue
        #     else:
        #         wheels_or_tires = attributes[0]["value"]
        #         if "колеса" in wheels_or_tires.lower() or "колёса" in wheels_or_tires.lower() or "колес" in wheels_or_tires.lower() or "резина" in wheels_or_tires.lower() or "диск" in wheels_or_tires.lower():
        #             # print(code, attributes)
        #             brand_model = attributes[1]["value"]
        #             season = attributes[2]["value"]
        #             tire_parameters = attributes[3]["value"]
        #             status = attributes[5]["value"]
        #             google_disk_link = None
        #
        #             print(status, code)
        #
        #             if status.lower() in ["отличное", "плохое", "среднее", "хорошее", "нормальное", "средние"]:
        #                 status = attributes[6]["value"]
        #
        #             storage = None
        #             stage = None
        #             disk_parameters = None
        #             for num in range(3, 14):
        #                 try:
        #                     if attributes[num]["name"] == "Склад":
        #                         storage = attributes[num]["value"]
        #                     elif attributes[num]["name"] == "Ссылка на фотографии":
        #                         google_disk_link = attributes[num]["value"]
        #                     elif attributes[num]["name"] == "Состояние":
        #                         stage = attributes[num]["value"]
        #                     elif attributes[num]["name"] == "Цена продажи для магазина":
        #                         price = attributes[num]["value"]
        #                     elif attributes[num]["name"] == "Остаток протектора":
        #                         tread_remain = attributes[num]["value"]
        #                 except IndexError:
        #                     continue
        #             photo_url = data["images"]["meta"]["href"]
        #
        #             try:
        #                 photo_download = request("GET", photo_url,
        #                                          headers={"Authorization": f"Bearer {access_token}"}).json()
        #
        #             except requests.exceptions.ReadTimeout:
        #                 continue
        #
        #             if len(photo_download["rows"]) > 0:
        #                 photo = request("GET", photo_download["rows"][0]["meta"]["downloadHref"],
        #                                 headers={"Authorization": f"Bearer {access_token}"}).content
        #
        #                 if (status.lower() in ["принят", "подтвержден",
        #                                        "подтверждён", "принято",
        #                                        "подтверждено"] and price is not None and price > 0 and
        #                         str(code) not in codes and storage is not None):
        #                     lots_codes.append(code)
        #                     db.add_lot(
        #                         name=name,
        #                         code=code,
        #                         model=brand_model,
        #                         season=season,
        #                         storage=storage,
        #                         tires=tire_parameters,
        #                         disks=disk_parameters,
        #                         price=price // 100,
        #                         photo=photo,
        #                         google_link=google_disk_link,
        #                         stage=stage
        #                     )
        #
        #         elif wheels_or_tires.lower() in ["шины", "шина"]:
        #             brand_model = attributes[1]["value"]
        #             season = attributes[2]["value"]
        #             tire_parameters = attributes[3]["value"]
        #             status = attributes[4]["value"]
        #             if status.lower() in ["отличное", "плохое", "среднее", "хорошее", "нормальное"]:
        #                 status = attributes[5]["value"]
        #
        #             storage = None
        #             google_disk_link = None
        #             stage = None
        #             for num in range(3, 14):
        #                 try:
        #                     if attributes[num]["name"] == "Склад":
        #                         storage = attributes[num]["value"]
        #                     elif attributes[num]["name"] == "Ссылка на фотографии":
        #                         google_disk_link = attributes[num]["value"]
        #                     elif attributes[num]["name"] == "Состояние":
        #                         stage = attributes[num]["value"]
        #                     elif attributes[num]["name"] == "Цена продажи для магазина":
        #                         price = attributes[num]["value"]
        #                     elif attributes[num]["name"] == "Остаток протектора":
        #                         tread_remain = attributes[num]["value"]
        #                 except IndexError:
        #                     continue
        #             photo_url = data["images"]["meta"]["href"]
        #             try:
        #                 photo_download = request("GET", photo_url,
        #                                          headers={"Authorization": f"Bearer {access_token}"}).json()
        #
        #             except requests.exceptions.ReadTimeout:
        #                 continue
        #
        #             print(f"{status =} {price =} {code =} {storage =}")
        #             if len(photo_download["rows"]) > 0:
        #                 photo = request("GET", photo_download["rows"][0]["meta"]["downloadHref"],
        #                                 headers={"Authorization": f"Bearer {access_token}"}).content
        #                 if status.lower() in ["принят", "подтвержден",
        #                                       "подтверждён", "принято",
        #                                       "подтверждено"] and price is not None and price > 0 and str(
        #                     code) not in codes and storage is not None:
        #
        #                     db.add_lot(
        #                         name=name,
        #                         code=code,
        #                         model=brand_model,
        #                         season=season,
        #                         storage=storage,
        #                         tires=tire_parameters,
        #                         disks=None,
        #                         price=price // 100,
        #                         photo=photo,
        #                         google_link=google_disk_link,
        #                         stage=stage
        #                     )
