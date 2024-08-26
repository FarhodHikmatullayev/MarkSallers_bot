from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=221, null=True, blank=True)
    username = models.CharField(max_length=221, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return self.full_name


class Branch(models.Model):
    name = models.CharField(max_length=221)

    class Meta:
        db_table = 'branch'
        verbose_name = 'Branch'
        verbose_name_plural = "Filiallar"


class Sellers(models.Model):
    code = models.BigIntegerField(null=True, blank=True, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=221, null=True, blank=True)
    last_name = models.CharField(max_length=221, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)

    class Meta:
        db_table = 'seller'
        verbose_name = 'Seller'
        verbose_name_plural = 'Sotuvchilar'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    title = models.CharField(max_length=221)

    class Meta:
        db_table = 'category'
        verbose_name = "Category"
        verbose_name_plural = "Baholash kategoriyalari"

    def __str__(self):
        return self.title


class Marks(models.Model):
    seller = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mark = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ])
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'mark'
        verbose_name = 'Mark'
        verbose_name_plural = 'Baholar/Izohlar'

    def __str__(self):
        return f"{self.user.full_name} ning {self.seller} uchun {self.category} bo'yicha bildirgan bahosi va izohi"
