# Generated by Django 3.2.4 on 2021-11-06 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_alter_recipe_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=100000)),
                ('file', models.FileField(upload_to='images/instructions_images/')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructions', to='recipe.recipe')),
            ],
        ),
    ]
