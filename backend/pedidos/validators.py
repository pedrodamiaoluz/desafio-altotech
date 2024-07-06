import re

from django.core.validators import RegexValidator

from usuarios.validators import PADRA_REGEX_LETRAS

REGEX_ENDERECO = RegexValidator(re.compile(
    PADRA_REGEX_LETRAS, re.I),
    message='Não é aceito caracteres especiais nem números'
)

REGEX_NUMERO_ENDERECO = RegexValidator(re.compile(
    r'^[a-z0-9]+$', re.I), message="Não é aceito caracteres especias")
REGEX_CEP = RegexValidator(re.compile(
    r'^[0-9]+$'), message='Digite apenas números')
