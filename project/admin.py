from django.contrib import admin
from .models import User, Branch, Sellers, Marks


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(Sellers)
class SellerAdmin(admin.ModelAdmin):
    pass


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    pass
