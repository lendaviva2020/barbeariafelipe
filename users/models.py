from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("user", "Usuário"),
        ("barber", "Barbeiro"),
        ("admin", "Administrador"),
    ]

    email = models.EmailField(unique=True, verbose_name="E-mail")
    name = models.CharField(max_length=255, verbose_name="Nome")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="user", verbose_name="Função"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_barber(self):
        return self.role == "barber"
