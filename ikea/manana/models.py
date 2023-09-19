from django.db import models



class Outs(models.Model):
    puertas_enlance = (
        ('', 'Seleccione puerta'),
        ('Puerta1', 'P1'),
        ('Puerta2', 'P2'),
        ('Puerta3', 'P3'),
        ('Plataforma', 'Plataforma'),
    )

    motivo_out = (
        ('', 'Seleccione motivo'),
        ('Llenado', 'LLenado'),
        ('Picking', 'Picking'),
        ('PlanB', 'PlanB'),
        ('Guardia', 'Guardia'),
        ('L-L','L-L'),
    )


    code = models.CharField(max_length=8, blank=False, verbose_name="Referencia")
    down = models.BooleanField(default=False , blank=True,null=True, verbose_name="Bajado")
    ubicacion = models.CharField(max_length=6, blank=False,null=True, verbose_name="Ubicacion")
    puertas = models.CharField(max_length=10,  choices=puertas_enlance , blank=False, default='')
    motivo = models.CharField(max_length=10,  choices=motivo_out , blank=False, default='')
    hora = models.DateTimeField(auto_now_add=True, verbose_name="Hora")

    def save(self, *args, **kwargs):
        # Completar el código con ceros al principio si tiene menos de 8 caracteres
        self.code = self.code.zfill(8)
        super().save(*args, **kwargs)