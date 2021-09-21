from django.db import models


# Clase abstracta, no se crea una tabla en la bd
class ModelAuditory(models.Model):
    date_crea = models.DateTimeField(auto_now_add=True)
    date_updat = models.DateTimeField(auto_now=True)

    ACTIVE = "Active"
    INACTIVE = "Inactive"
    STATE_OPTIONS = [
        (ACTIVE, "Active"),  # ACTIVE valor y Active valor a mostrar
        (INACTIVE, "Inactive"),
    ]
    state = models.CharField(
        max_length=8, choices=STATE_OPTIONS, default=ACTIVE)

    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(models.Model):
    description = models.CharField(max_length=50, unique=True)
    date_crea = models.DateTimeField(auto_now_add=True)
    date_updat = models.DateTimeField(auto_now=True)
    # Toma por defecto el valor true cada vez que se cree uno
    active = models.BooleanField(default=True)

    # Retorna una representaciónn de cadena de cualquier objeto. Ese método lo usará tanto python y django para mostrar texto plano cuando se haga referencia a una instancia a un objeto en este caso (Category)
    # Es requerido
    def __str__(self):
        return self.description

    # Guardar las descripciones en mayúsucla. Se sobreescribe este método de la clase Model
    def save(self):
        self.description = self.description.upper()
        # Ejecutado el comando save del modelo padre
        super(Category, self).save()

    # Hacer referencia al modelo en plural en el admin de django
    class Meta:
        verbose_name_plural = "Categories"
