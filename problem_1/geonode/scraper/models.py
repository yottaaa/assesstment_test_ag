from django.db import models

class Proxy(models.Model):
    ip = models.CharField(max_length=100, null=True)
    port = models.CharField(max_length=100, null=True)
    protocol = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    uptime = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "proxies"