from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from django.utils.http import urlencode
from django.utils.html import format_html
from store import models
from django.urls import reverse

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = "inventory"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("<10", "low")
        ]
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value == "<10":
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    autocomplete_fields = ["collection"]
    prepopulated_fields = {
        "slug" : ["title"]
    }
    actions = ["clear_inventory"]
    list_display = ["title", "unit_price", "inventory_status", "collection_title"] 
    list_editable = ["unit_price"]
    list_select_related = ["collection"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 10 

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering = "inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"
    
    @admin.action(description = "Clear Inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated."
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["firstname", "lastname", "membership", "orders_count"]
    list_editable = ["membership"]
    ordering = ["firstname", "lastname"]
    search_fields = ["firstname__istartswith", "lastname__istartswith"] 
    list_per_page = 10

    @admin.display(ordering = "orders_count")
    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({
                "customer__id" : str(customer.id)
            })
        )
        return format_html("<a href = '{}'>{}</a>", url, customer.orders_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            orders_count = Count("order")
        ) 

class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    min_num = 1
    max_num = 20
    autocomplete_fields = ["product"]
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "customer"]
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_per_page = 10

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering = "products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({
                "collection__id" : str(collection.id)
            })
        )
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)
        
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count = Count("product")
        )
