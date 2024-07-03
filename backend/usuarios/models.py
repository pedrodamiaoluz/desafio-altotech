import re

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from usuarios.managers import CustomUserManager
from usuarios.validators import (
    PADRA_REGEX_CPF,
    PADRA_REGEX_EMAIL,
    PADRA_REGEX_LETRAS,
    PADRA_REGEX_TELEFONE,
    eh_de_maior,
    eh_valido_cpf,
)

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('endereço de email'),
                              unique=True,
                              validators=[
                                  RegexValidator(re.compile(PADRA_REGEX_EMAIL),
                                                 'Endereço de email inválido')
    ])
    nome_completo = models.CharField(
        _("nome"),
        max_length=100,
        validators=[
            RegexValidator(re.compile(PADRA_REGEX_LETRAS, re.I),
                           'Caracteres inválidos, insira apenas letras')
        ])
    cpf = models.CharField(_("CPF"),
                           max_length=14,
                           unique=True,
                           null=True,
                           validators=[
                               eh_valido_cpf,
                               RegexValidator(
                                   re.compile(PADRA_REGEX_CPF),
                                   'CPF não está no padrão exigido', 'invalid')
    ])
    data_nascimento = models.DateField(null=True,
                                       blank=False,
                                       validators=[eh_de_maior])
    telefone = models.CharField(max_length=20,
                                validators=[
                                    RegexValidator(
                                        re.compile(PADRA_REGEX_TELEFONE),
                                        'Número telefone inválido')
                                ])

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
