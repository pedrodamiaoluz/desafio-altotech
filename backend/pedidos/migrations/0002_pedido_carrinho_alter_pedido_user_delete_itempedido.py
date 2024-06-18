# Generated by Django 5.0.6 on 2024-06-18 18:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carrinho", "0001_initial"),
        ("pedidos", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="carrinho",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="carrinho.carrinho",
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="pedidos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="ItemPedido",
        ),
    ]
