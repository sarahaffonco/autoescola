from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_studentprofile_license_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructorvehicle',
            name='last_license_exercise',
            field=models.DateField(blank=True, null=True, verbose_name='Exercício do Último Licenciamento'),
        ),
    ]
