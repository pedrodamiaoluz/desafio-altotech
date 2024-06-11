from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

user_model = get_user_model()

class Util:
    url_resset_password = 'https://localhost:8000/usuarios/nova-senha/%s/%s'

    @staticmethod
    def eh_valido_uid_token(uid, token):
        user = Util.get_user(uid)
        if PasswordResetTokenGenerator().check_token(user, token):
            return user
        return None

    @staticmethod
    def get_user(uid):
        try:
            id = smart_str(urlsafe_base64_decode(uid))
            user = user_model.objects.get(id=id)
            return user
        except (DjangoUnicodeDecodeError, ValueError):
            pass
        return None


    @staticmethod
    def get_uid_token(user):
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        return (uid, token)

    @staticmethod
    def get_link_reset_senha(user, url_resset_password=None):
        uid, token = Util.get_uid_token(user)
        if url_resset_password:
            return url_resset_password % (uid, token)
        return Util.url_resset_password % (uid, token)

    @staticmethod
    def send_email_reset_password(user, link):
        context = {"user": user, "link": link}

        subject = "Redefinição de senha"

        message = render_to_string("usuarios/email/reset_password.txt",
                                   context=context)

        html_message = render_to_string("usuarios/email/reset_password.html",
                                        context=context)

        send_mail(
            subject=subject,
            message=message,
            from_email=
            None,  # caso seja None ele ira usar o valor configurado no settings na costante DEFAULT_FROM_EMAIL.
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False)
