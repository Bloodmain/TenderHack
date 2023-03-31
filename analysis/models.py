from django.db import models


# Create your models here.
class Companies(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название компании")
    supplier_inn = models.PositiveBigIntegerField(verbose_name="ИНН компании", unique=True, primary_key=True)  # :NOTE: validate min_Value
    supplier_kpp = models.PositiveBigIntegerField(verbose_name="КПП компании", unique=True)
    okved = models.CharField(max_length=100, verbose_name="Номера ОКВЭД компании")

    COMPANY_STATUS = (  # :NOTE: add active, blocked
        ()
    )

    status = models.CharField(max_length=15, choices=COMPANY_STATUS,
                              verbose_name="Статус компании(Активная или Заблокирована)")
    count_managers = models.IntegerField(verbose_name="Кол - во контактный лиц компании")  # :NOTE: min value


class Purchases(models.Model):
    # :NOTE: max_length for char field
    id = models.PositiveBigIntegerField(primary_key=True, unique=True, verbose_name="Номер закупки")
    purchase_name = models.CharField(max_length=100, verbose_name="Название закупки", blank=False)
    lot_name = models.CharField(max_length=100, verbose_name="Название лота", blank=False)
    price = models.IntegerField(verbose_name="Начальная максимальная цена закупки, предложенная заказчиком",
                                blank=False)  # :NOTE: validate min_value
    customer_inn = models.ForeignKey(to=Companies, on_delete=models.CASCADE,
                                     verbose_name="ИНН заказчика")
    delivery_region = models.CharField(max_length=100, verbose_name="Регион доставки товара")
    publish_date = models.DateField(verbose_name="Дата публикации закупки")
    contract_category = models.CharField(max_length=100, verbose_name=" Категория контракта(КС или Потребность)")


class Participants(models.Model):
    part_id = models.ForeignKey(Purchases, on_delete=models.CASCADE, verbose_name="Номер закупки")
    supplier_inn = models.ForeignKey(to=Companies, on_delete=models.CASCADE,
                                     verbose_name="ИНН поставщика (участника)")
    is_winner = models.BooleanField(blank=False)
