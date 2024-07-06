from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import (
    DjangoUnicodeDecodeError, force_bytes, smart_str
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
user_model = get_user_model()


class Util:
    url_resset_password = 'usuarios:nova_senha'

    @staticmethod
    def eh_valido_uid_token(uid: str, token: str):
        """ função para verificar se o uid e o token são válidos """
        user = Util.get_user(uid)
        if PasswordResetTokenGenerator().check_token(user, token):
            return user
        return None

    @staticmethod
    def get_user(uid: str) -> user_model | None:
        """ função para pegar o usuário pelo uid """
        try:
            id = smart_str(urlsafe_base64_decode(uid))
            user = user_model.objects.get(id=id)
            return user
        except (DjangoUnicodeDecodeError, ValueError):
            pass
        return None

    @staticmethod
    def get_uid_token(user: user_model) -> tuple[str, str]:
        """ função para gerar o uid e o token """
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        return (uid, token)

    @staticmethod
    def get_link_reset_senha(user: user_model,
                             url_resset_password: str | None = None):
        """ função para gerar o link de redefinição de senha """
        uid, token = Util.get_uid_token(user)
        if url_resset_password is None:
            url_resset_password = Util.url_resset_password
        return reverse(url_resset_password, kwargs={'uid': uid, 'token': token})

    @staticmethod
    def send_email_reset_password(user: user_model, link: str) -> None:
        """ função para enviar o email de redefinição de senha """

        context = {"user": user, "link": link}

        subject = "Redefinição de senha"

        message = render_to_string("usuarios/email/reset_password.txt",
                                   context=context)

        html_message = render_to_string("usuarios/email/reset_password.html",
                                        context=context)

        send_mail(
            subject=subject,
            message=message,
            from_email=  # caso seja None ele ira usar o valor configurado no
            None,  # settings na costante DEFAULT_FROM_EMAIL.
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False)
