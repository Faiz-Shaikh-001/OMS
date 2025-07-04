# Generated by Django 5.2 on 2025-06-13 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_rename_frames_frame_rename_lenses_lensproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='lensproduct',
            name='b_c',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='frame',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='frame',
            name='purchase_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='frame',
            name='sales_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='lensproduct',
            name='add',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lensproduct',
            name='axis',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lensproduct',
            name='cylindrical',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='lensproduct',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lensproduct',
            name='material_type',
            field=models.CharField(blank=True, choices=[('Mineral Lens', 'Mineral Lens'), ('Plastic Lens', 'Plastic Lens'), ('Polycarbonate Lens', 'Polycarbonate Lens'), ('Trivex Lens', 'Trivex Lens'), ('Organic Lens', 'Organic Lens')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='lensproduct',
            name='purchase_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='lensproduct',
            name='sales_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='lensproduct',
            name='spherical',
            field=models.FloatField(),
        ),
    ]
