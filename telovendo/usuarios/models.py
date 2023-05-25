from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    email_verificado = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Persona(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=12)

    class Meta:
        abstract = True

class Trabajador(Persona):
    TRABAJADOR_CHOICES = [(1, "Administrador"), (2, "Staff")]
    tipo_trabajador = models.IntegerField(choices=TRABAJADOR_CHOICES)

class Cliente(Persona):
    forma_pago = models.ForeignKey("gestion.FormaPago", on_delete=models.SET_NULL, null=True)
    direccion = models.ForeignKey("Direccion", on_delete=models.CASCADE, related_name="cliente", null=True)

class Direccion(models.Model):
    calle = models.CharField(max_length=120)
    numero = models.CharField(max_length=5)
    departamento = models.CharField(max_length=5, null=True)
    codigo_postal = models.CharField(max_length=20)
    comuna = models.ForeignKey("gestion.Comuna", on_delete=models.PROTECT)
    nombre = models.CharField(max_length=15) # Ej: Casa
    descripcion = models.CharField(max_length=100) #Ej: población x, paradero número x, condominio x