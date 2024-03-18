from django.contrib import admin

from rentals.models import Car, Rental, Insurance


admin.site.register(Insurance)
admin.site.register(Car)


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("car", "renter")
        return queryset
