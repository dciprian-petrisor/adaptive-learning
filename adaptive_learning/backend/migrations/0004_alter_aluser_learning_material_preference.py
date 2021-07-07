# Generated by Django 3.2.4 on 2021-06-29 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_aluser_learning_material_preference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluser',
            name='learning_material_preference',
            field=models.CharField(choices=[('visual', 'Visual'), ('verbal', 'Verbal')], default='visual', max_length=100),
        ),
    ]