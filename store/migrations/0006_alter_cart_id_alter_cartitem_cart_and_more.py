# Generated by Django 4.2 on 2023-05-03 09:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_review_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="store.cart",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="cartitem", unique_together={("cart", "product")},
        ),
    ]
