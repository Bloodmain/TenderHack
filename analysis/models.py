from django.db import models


# Create your models here.
MAX_LENGTH = 200
class Companies(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название компании")
    supplier_inn = models.PositiveBigIntegerField(verbose_name="ИНН компании", unique=True, primary_key=True)
    supplier_kpp = models.PositiveBigIntegerField(verbose_name="КПП компании", unique=True)
    okved = models.CharField(max_length=MAX_LENGTH, verbose_name="Номера ОКВЭД компании")

    ACTIVE = "A"
    BLOCKED = "B"

    COMPANY_STATUS = [
        (ACTIVE, "active"),
        (BLOCKED, "blocked")
    ]

    status = models.CharField(max_length=15, choices=COMPANY_STATUS,
                              verbose_name="Статус компании(Активная или Заблокирована)")
    count_managers = models.PositiveIntegerField(verbose_name="Кол - во контактный лиц компании")


class Purchases(models.Model):
    # :NOTE: max_length for char field
    id = models.PositiveBigIntegerField(primary_key=True, unique=True, verbose_name="Номер закупки")
    purchase_name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название закупки", blank=False)
    purchase_name_end = models.CharField(max_length=MAX_LENGTH, default="")
    lot_name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название лота", blank=False)
    price = models.PositiveIntegerField(verbose_name="Начальная максимальная цена закупки, предложенная заказчиком",
                                        blank=False)
    vector = models.BinaryField(default=bytes(0))
    customer_inn = models.ForeignKey(to=Companies, on_delete=models.CASCADE,
                                     verbose_name="ИНН заказчика")
    delivery_region = models.CharField(max_length=MAX_LENGTH, verbose_name="Регион доставки товара")
    publish_date = models.DateField(verbose_name="Дата публикации закупки")
    contract_category = models.BooleanField(verbose_name=" Категория контракта(КС или Потребность)")


class Participants(models.Model):
    part_id = models.ForeignKey(Purchases, on_delete=models.CASCADE, verbose_name="Номер закупки")
    supplier_inn = models.ForeignKey(to=Companies, on_delete=models.CASCADE,
                                     verbose_name="ИНН поставщика (участника)")
    is_winner = models.BooleanField(blank=False)


class Contracts(models.Model):
    contract_id = models.ForeignKey(Purchases, on_delete=models.CASCADE, verbose_name="Номер закупки")
    contract_reg_number = models.CharField(max_length=30, blank=False, verbose_name="Номер регистрации контракта")
    price = models.PositiveIntegerField(verbose_name="Цена заключенного контракта", blank=False)
    contract_conclusion_date = models.DateField(verbose_name="Дата заключения контракта", blank=False)
