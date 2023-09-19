from django.db import models

class AltaRotacionCheck(models.Model):
    lv_checked = models.BooleanField(default=False)
    bajado_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"Item {self.pk}"