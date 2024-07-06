from django.contrib.auth.models import BaseUserManager

# A Manager é a interface através da qual operações de consulta de banco de
# dados são fornecidas aos modelos Django. Pelo menos uma Manager existe para
# cada modelo em um aplicativo Django.


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    # criar usuários
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        # set a senha com hash
        user.set_password(password)
        user.save(using=self._db)
        return user

    # cria um usuário comun
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    # cria um super usuário que tem todas as permissôes do sistema e terá acesso
    # a admin do django
    def create_superuser(self, email, password=None, **extra_fields):
        # permitirá que faça login
        extra_fields.setdefault("is_admin", True)
        # fornece todos os privilégios
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
