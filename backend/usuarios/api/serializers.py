from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from produtos.models import Carrinho

user_model = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField()

    def usuario_ehAutenticado(self):
        email = self.data['email']
        senha = self.data['senha']

        user = authenticate(email=email, password=senha)
        if user is None:
            raise serializers.ValidationError("Usuário não encontrado")
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model
        fields = ("id", "nome_completo", 'cpf', 'data_nascimento', 'telefone',
                  'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        user = user_model.objects.create_user(**validated_data)
        Carrinho.objects.create(proprietario=user)
        return user


class UserChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model
        fields = (
            "id",
            "nome_completo",
            'cpf',
            'data_nascimento',
            'telefone',
            'email',
        )


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8,
                                     max_length=255,
                                     style={'input_type': 'password'})


class UserEnderecoSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model
        fields = ('cep', 'estado', 'cidade', 'bairro',
                  'complemento', 'rua', 'numero')
