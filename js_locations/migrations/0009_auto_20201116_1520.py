# Generated by Django 2.2.10 on 2020-11-16 15:20

from django.db import migrations, models
import django.db.models.deletion
import parler.fields


class Migration(migrations.Migration):

    dependencies = [
        ('js_locations', '0008_auto_20201026_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationtranslation',
            name='link',
            field=models.CharField(blank=True, max_length=255, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='locationtranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='js_locations.Location'),
        ),
    ]