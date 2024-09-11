from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=221, null=True, blank=True, verbose_name='F.I.Sh')
    username = models.CharField(max_length=221, null=True, blank=True, verbose_name='USERNAME')
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name='TELEFON RAQAM')
    telegram_id = models.BigIntegerField(unique=True, verbose_name='TELEGRAM ID')

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return self.full_name


class Branch(models.Model):
    name = models.CharField(max_length=221, verbose_name='FILIAL NOMI')

    class Meta:
        db_table = 'branch'
        verbose_name = 'Branch'
        verbose_name_plural = "Filiallar"

    def __str__(self):
        return self.name


class Sellers(models.Model):
    code = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name='MAXSUS KOD')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='FILIAL')
    first_name = models.CharField(max_length=221, null=True, blank=True, verbose_name='ISM')
    last_name = models.CharField(max_length=221, null=True, blank=True, verbose_name='FAMILIYA')
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name='TELEFON RAQAM')

    class Meta:
        db_table = 'seller'
        verbose_name = 'Seller'
        verbose_name_plural = 'Sotuvchilar'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    title = models.CharField(max_length=221, verbose_name='KATEGORIYA NOMI')

    class Meta:
        db_table = 'category'
        verbose_name = "Category"
        verbose_name_plural = "Baholash kategoriyalari"

    def __str__(self):
        return self.title


class Marks(models.Model):
    seller = models.ForeignKey(Sellers, on_delete=models.CASCADE, verbose_name='SAVDOGAR')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='BAHO BERGAN SHAXS')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='KATEGORIYA NOMI')
    mark = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ], verbose_name='BAHO')
    description = models.TextField(null=True, blank=True, verbose_name='IZOH')
    created_at = models.DateTimeField(null=True, blank=True, verbose_name='YARATILGAN VAQT')

    class Meta:
        db_table = 'mark'
        verbose_name = 'Mark'
        verbose_name_plural = 'Baholar/Izohlar'

    def __str__(self):
        return f"{self.user.full_name} -> {self.seller} ({self.category})"
