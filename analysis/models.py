from django.db import models


# Create your models here.
class Purchases(models.Model):
    # :NOTE: max_length for char field
    id = models.PositiveBigIntegerField(primary_key=True, unique=True, verbose_name="Номер закупки")
    purchase_name = models.CharField(max_length=100, verbose_name="Название закупки", blank=False)
    lot_name = models.CharField(max_length=100, verbose_name="Название лота", blank=False)
    price = models.IntegerField(verbose_name="Начальная максимальная цена закупки, предложенная заказчиком",
                                blank=False)  # :NOTE: validate min_value
    customer_inn = models.ForeignKey(verbose_name="ИНН заказчика")
    customer_name = models.CharField(max_length=100, verbose_name="Название заказчика")
    delivery_region = models.CharField(max_length=100, verbose_name="Регион доставки товара")
    publish_date = models.DateField(verbose_name="Дата публикации закупки")
    contract_category = models.CharField(max_length=100, verbose_name=" Категория контракта(КС или Потребность)")


class Companies(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название компании")
    supplier_inn = models.PositiveBigIntegerField(verbose_name="ИНН компании")  # :NOTE: validate min_Value
    supplier_kpp = models.PositiveBigIntegerField(verbose_name="КПП компании")
    okved = models.CharField(max_length=100, verbose_name="Номера ОКВЭД компании")

    COMPANY_STATUS = [ # :NOTE: add active, blocked
        ()
    ]

    status = models.CharField(max_length=15, choices=COMPANY_STATUS,
                              verbose_name="Статус компании(Активная или Заблокирована)")
    count_managers = models.IntegerField(verbose_name="Кол - во контактный лиц компании")  # :NOTE: min value
