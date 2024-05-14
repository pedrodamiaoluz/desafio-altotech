import re
from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

PADRA_REGEX_LETRAS = r'^[a-zá-ú\s]+$'
PADRA_REGEX_TELEFONE = r'^\(?[0-9]{2}\)?[\s]?[9]?[0-9]{4}[-]?[0-9]{4}$'
PADRA_REGEX_CPF = r'^[0-9]{3}\.[0-9]{3}\.[0-9]{3}\-[0-9]{2}$'
PADRA_REGEX_EMAIL = r'^[a-z0-9._]+@[a-z]+\.([a-z]{3,})(\.[a-z]{2,})?$'


def eh_de_maior(data_nascimento):
    idade = relativedelta(date.today(), data_nascimento).years

    if idade < 18:
        raise ValidationError(
            "Data de nascimento inválida, o usuário tem que ser maior de idade"
        )
    return data_nascimento


def eh_valido_cpf(value):
    cpf = str(value)  # trasnforma o valor em String
    cpf = re.sub(r'[^0-9]', '',
                 cpf)  # remove qualquer caracter que não seja numero

    if not cpf or len(
            cpf
    ) != 11:  # se o cpf não for informado ou se ele não tiver 11 digitos numericos é levantado exeção de validação
        raise ValidationError('Digite um cpf valido')

    novo_cpf = cpf[:-2]  # pega os 9 primeiros digitos do cpf
    reverso = 10  # utilizado para a multiplicação do digito
    total = 0  # soma dos digitos para descobrir os digitos 10 e 11

    for index in range(
            19
    ):  # laço para soma os primeiros 9 e depois 10 digitos para descobrir os digitos 10 e 11
        if index > 8:  # index para descobrir o 10 digito
            index -= 9  # index para descobrir o 11 digito

        total += int(
            novo_cpf[index]
        ) * reverso  # pega o digito multiplca pelo valor de reverso

        reverso -= 1
        if reverso < 2:
            reverso = 11  # para encontra o digito 11
            d = 11 - (total % 11)  # encontra o digito

            if d > 9:
                d = 0
            total = 0
            novo_cpf += str(d)  # adiciona o digito ao novo_cpc

    sequencia = novo_cpf == str(novo_cpf[0]) * len(
        cpf
    )  # verifica se o numero é uma sequencia ex: 11111111111 ou 22222222222 ...

    if cpf == novo_cpf and not sequencia:
        return cpf

    raise ValidationError("cpf inválido")
