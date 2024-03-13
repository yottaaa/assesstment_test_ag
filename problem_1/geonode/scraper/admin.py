from django.contrib import admin
from datetime import datetime
from .models import Proxy
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
)

# Register your models here.
class ProxyAdmin(admin.ModelAdmin):
    list_display = ["ip", "port", "protocol", "country", "uptime", "created_at"]
    list_filter = (
        ("created_at", DateRangeFilterBuilder(
            title="Scrape DateTime Quick Filter",
        )),
        (
            "created_at",
            DateTimeRangeFilterBuilder(
                title="Scrape DateTime Quick Filter Advance Filter",
                default_start=datetime.now(),
                default_end=datetime.now(),
            ),
        )
    )

admin.site.register(Proxy,ProxyAdmin)
