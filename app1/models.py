from django.db import models
from datetime import date
from django.utils.text import slugify


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
        abstract = True  # Para no crear la tabla


class Category(ModelAuditory):
    description = models.CharField(max_length=50, unique=True)
    # date_crea = models.DateTimeField(auto_now_add=True)
    # date_updat = models.DateTimeField(auto_now=True)
    # Toma por defecto el valor true cada vez que se cree uno
    # active = models.BooleanField(default=True)

    # Retorna una representación de cadena de cualquier objeto. Ese método lo usará tanto python y django para mostrar texto plano cuando se haga referencia a una instancia a un objeto en este caso (Category)
    # Es requerido
    def __str__(self):
        return self.description

    # Guardar las descripciones en mayúsucula. Se sobreescribe este método de la clase Model
    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        # Ejecutado el comando save del modelo padre
        super(Category, self).save(*args, **kwargs)

    # Hacer referencia al modelo en plural en el admin de django
    class Meta:
        verbose_name_plural = "Categories"


class Person(ModelAuditory):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_birth = models.DateField(null=False, blank=False)

    @property  # Decorador, no afecta la base de datos
    def age(self):
        today = date.today()
        age = today.year - self.date_birth.year - \
            ((today.month, today.day) <
             (self.date_birth.month, self.date_birth.day))
        return age

    @property
    def complete_name(self):
        return "{} {}".format(self.name, self.last_name)

    def __str__(self):
        return "{} {}".format(self.name, self.last_name)

    def save(self):
        self.name = self.name.capitalize()
        self.last_name = self.last_name.capitalize()
        super(Person, self).save()

    class Meta:
        verbose_name_plural = "People"


class Book(ModelAuditory):
    name = models.CharField(max_length=50)
    price = models.FloatField(
        default=1,
        help_text=" en dólares"
    )
    weight = models.PositiveIntegerField(
        help_text=" en libras"
    )

    VIRTUAL = 'Virtual'
    FISIC = 'Físico'
    OPTIONS = [
        (VIRTUAL, 'Virtual'),
        (FISIC, 'Físico'),
    ]
    type = models.CharField(
        max_length=7,
        choices=OPTIONS,
        default=FISIC,
    )

    url_download = models.URLField(default=None)

    def __str__(self):
        return "{}[{}]".format(self.name, self.type)

    def save(self):
        self.name = self.name.upper()
        super(Book, self).save()

    class Meta:
        verbose_name_plural = "Books"
        # Lista de campos que va ejecutar el filtro de no repetir tipo de libro
        unique_together = ('name', 'type')


class Progenitor(ModelAuditory):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    father = models.CharField(max_length=50)
    mother = models.CharField(max_length=50)

    def _str_(self):
        return "{} - {} - - {}".format(self.person, self.mother, self.dad)

    class Meta:
        verbose_name_plural = "Progenitors"


class Father(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Son(models.Model):
    # PROTECT: no se puede borrar un registro de la tabla padre si tiene registro en la tabla hijo
    father = models.ForeignKey(Father, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{} hijo de {}".format(self.name, self.father)


class Publication(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, default="")

    def __str__(self):
        return self.title

# Agregar slug
    def save(self):
        self.slug = slugify(self.title)
        super(Publication, self).save()


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    def __str__(self):
        return self.headline


# Uso de self join
class Employee(models.Model):
    name = models.CharField(max_length=100)
    supervisor = models.ForeignKey(
        'self', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# Otra forma de usar el self join
class Employee2(models.Model):
    name = models.CharField(max_length=100)
    supervisor = models.ForeignKey(
        'app1.Employee2', null=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name


# Vincular el modelo a una vista creada
class ViewFatherSon(models.Model):
    idfather = models.IntegerField()
    namefather = models.CharField(max_length=50)
    idson = models.IntegerField()
    nameson = models.CharField(max_length=50)

    def __str__(self):
        return "{} -> {}".format(self.namefather, self.nameson)

    class Meta:
        managed = False  # Se crea el modelo pero django no va poder manipular este modelo
        db_table = "view_fatherson"  # Referencia a una tabla


class NewModel(models.Model):
    name = models.CharField(max_length=50)
    # Cambiar el nombre de la columna al que esta escrito en el modelo
    a = models.CharField(max_length=50, db_column="another_name", default="")

    class Meta:
        db_table = "new_name"  # Cambiar el nombre de la tabla


class UniqueModel(models.Model):
    name = models.CharField(max_length=100)

    # Restringir modelo a un único registro
    # Siempre es bueno cuando se sobreescribe el mmétodo self, pasarle los argumentos *args y **kwargs
    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__objects.first().pk
        super().save(*args, **kwargs)
