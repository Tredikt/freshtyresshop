from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from aiogram import Bot

from .models import Tyre, Order, Sorting


class TyresListView(ListView):
    def get_queryset(self):
        return Tyre.objects.all()

    def get_orders(self):
        return Order.objects.all()

    def get(self, request):
        tyres = self.get_queryset()
        orders = self.get_orders()
        tyres_list = []
        tyres_pk_list = [order.tyre_id for order in orders]

        for tyre in tyres:
            if tyre.status not in ["booked", "sold"] and tyre.pk not in tyres_pk_list:
                tyres_list.append(tyre)

        context = {"tyres": tyres_list, "search_value": ""}
        return render(request, "tyresapp/index.html", context=context)

    def post(self, request):
        search = request.POST.get("search")
        tyres = self.get_queryset()
        tyres_list = []

        for tyre in tyres:
            if search.lower() in tyre.name.lower() and tyre.status == "stock":
                tyres_list.append(tyre)

        context = {"tyres": tyres_list, "search_value": search}
        return render(request, "tyresapp/index.html", context=context)


class TyreDetails(DetailView):
    def get_queryset(self, pk):
        return Tyre.objects.filter(pk=pk)

    def get(self, request, pk, tg_id):
        tyre = self.get_queryset(pk=pk)
        context = {"tyre": tyre[0]}

        return render(request, "tyresapp/product_card.html", context=context)

    def post(self, request, pk, tg_id):
        tg_id = int(request.POST.get("tg_id"))
        Order.objects.create(
            tg_id=tg_id,
            tyre_id=pk
        )

        booked_tyre = Tyre.objects.filter(pk=pk)[0]
        booked_tyre.status = "booked"
        booked_tyre.save()

        tyre = self.get_queryset(pk=pk)
        context = {"tyre": tyre[0]}

        return render(request, "tyresapp/product_card_added.html", context=context)


class BasketView(ListView):
    context_object_name = "orders"

    def get_queryset(self, tg_id):
        return Order.objects.filter(tg_id=tg_id)

    def get(self, request, tg_id):
        orders = self.get_queryset(tg_id)
        tyres = []
        end_price = 0
        for elem in orders:
            end_price += Tyre.objects.filter(pk=elem.tyre_id)[0].price
            tyres.append(Tyre.objects.filter(pk=elem.tyre_id)[0])

        context = {"tyres": tyres, "tg_id": tg_id, "end_price": end_price}
        return render(request, "tyresapp/basket.html", context=context, status=404)

    def post(self, request, tg_id):
        isClear = request.post.get("isClear")
        if isClear == "1":
            orders = self.get_queryset(tg_id=tg_id)
            for order in orders:
                elem = Order.objects.get(pk=order.pk)
                elem.delete()

            context = {"tyres": [], "tg_id": tg_id, "end_price": 0}

        else:
            tyre_id = request.post.get("deleteOne")
            orders = self.get_queryset(tg_id=tg_id)
            for order in orders:
                if order.tyre_id == int(tyre_id):
                    elem = Order.objects.get(pk=order.pk)
                    elem.delete()

            tyres = []
            end_price = 0
            for elem in orders:
                end_price += Tyre.objects.filter(pk=elem.tyre_id)[0].price
                tyres.append(Tyre.objects.filter(pk=elem.tyre_id)[0])

            context = {"tyres": tyres, "tg_id": tg_id, "end_price": end_price}

        return render(request, "tyresapp/basket.html", context=context, status=404)


class OrderView(TemplateView):
    async def get_queryset(self, tg_id):
        return Order.objects.filter(tg_id=tg_id)

    async def get(self, request, tg_id):
        orders = await self.get_queryset(tg_id=tg_id)
        warehouses = []
        full_price = 0
        codes = []
        for elem in orders:
            codes.append(Tyre.objects.filter(pk=elem.tyre_id)[0].code)
            warehouse = Tyre.objects.filter(pk=elem.tyre_id)[0].location
            if warehouse not in warehouses:
                warehouses.append(warehouse)
            full_price += Tyre.objects.filter(pk=elem.tyre_id)[0].price

        context = {"warehouses": warehouses, "full_price": full_price, "tg_id": tg_id}
        return render(request, "tyresapp/order.html", context=context)

    async def post(self, request, tg_id):
        if request.method == "POST":
            orders = await self.get_queryset(tg_id=tg_id)

            FIO = request.POST.get("fio")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            comment = request.POST.get("comment")

            text = "Новый заказ!\n" \
                   "Коды:"

            for num, elem in enumerate(orders):
                tyre_info = Tyre.objects.filter(pk=elem.tyre_id)[0]
                text += f"{num + 1}) Код: {tyre_info.code}\n" \
                        f"Наименование: {tyre_info.name}\n" \
                        f"Размерность: {tyre_info.tyres_parameters}\n" \
                        f"Цена: {tyre_info.price}\n"

            user_data = f"\nФИО: {FIO}\n" \
                        f"Телефон: {phone}\n" \
                        f"Email: {email}\n\n" \
                        f"Комментарий к заказу: {comment}"

            bot = Bot(token="7085291557:AAFY3UT9CJyDj4GZIEBCFQVZ3SpYu-_PaSM")
            await bot.send_message(
                chat_id=-1002051098884,
                text=text + user_data
            )

            orders = Order.objects.filter(tg_id=tg_id)
            for order in orders:
                tyre = Tyre.objects.filter(pk=order.tyre_id)[0]
                tyre.status = "sold"
                tyre.save()

                order_object = Order.objects.get(pk=order.pk)
                order_object.delete()


            return render(request, "tyresapp/end_order.html")


class SortingView(TemplateView):
    def get(self, request, tg_id):
        return render(request, "tyresapp/sorting.html")

    def post(self, request, tg_id):
        method = request.POST.get("method")
        # Sorting.objects.create(
        #     tg_id=tg_id,
        #     method=method
        # )

        tyres = self.get_queryset()
        orders = self.get_orders()
        tyres_list = []
        tyres_pk_list = [order.tyre_id for order in orders]

        for tyre in tyres:
            if tyre.status not in ["booked", "sold"] and tyre.pk not in tyres_pk_list:
                tyres_list.append(tyre)

        if method == "new":
            tyres_list = tyres_list.sort(key=lambda lst: lst.created_at)

        elif method == "ascending":
            tyres_list = tyres_list.sort(key=lambda lst: lst.price)

        elif method == "descending":
            tyres_list = tyres_list.sort(key=lambda lst: lst.price, reverse=True)

        context = {"tyres": tyres_list, "search_value": ""}
        return render(request, "tyresapp/index.html", context=context)


class FiltrationView(TemplateView):
    def get(self, request):
        return render(request, "tyresapp/filtration.html")
    

class ExampleView(TemplateView):
    def get(self, request):
        return render(request, "tyresapp/pixels.html")