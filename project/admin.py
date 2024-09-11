from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'phone', 'telegram_id')
    search_fields = ('full_name', 'username', 'phone', 'telegram_id')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Sellers)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'code', 'branch')
    search_fields = ('first_name', 'last_name', 'phone', 'code', 'branch__name')


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'user', 'category', 'mark', 'created_at')
    search_fields = ('seller__first_name', 'seller_last_name', 'category__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
