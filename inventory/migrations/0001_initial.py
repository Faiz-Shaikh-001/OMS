# Generated by Django 5.2 on 2025-06-13 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Frames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=True)),
                ('frame_type', models.CharField(choices=[('3 Piece/Rimless', '3 Piece/Rimless'), ('Half Rimless/Supra', 'Half Rimless/Supra'), ('Full metal', 'Full metal'), ('Full Shell/Plastic', 'Full Shell/Plastic'), ('Goggles', 'Goggles')], max_length=20)),
                ('name', models.CharField(max_length=2000)),
                ('code', models.CharField(max_length=2000)),
                ('color', models.CharField(max_length=100)),
                ('size', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('purchase_price', models.IntegerField()),
                ('sales_price', models.IntegerField()),
                ('barcode', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Lenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lens_type', models.CharField(choices=[('Single Vision', 'Single Vision'), ('Bifocal', 'Bifocal'), ('Contact Lens', 'Contact Lens'), ('Progressive', 'Progressive')], max_length=20)),
                ('company_name', models.CharField(max_length=1000)),
                ('product_name', models.CharField(max_length=1000)),
                ('material_type', models.CharField(choices=[('Mineral Lens', 'Mineral Lens'), ('Plastic Lens', 'Plastic Lens'), ('Polycarbonate Lens', 'Polycarbonate Lens'), ('Trivex Lens', 'Trivex Lens'), ('Organic Lens', 'Organic Lens')], max_length=20)),
                ('index', models.IntegerField()),
                ('dia', models.IntegerField()),
                ('spherical', models.IntegerField()),
                ('cylindrical', models.IntegerField()),
                ('axis', models.IntegerField()),
                ('add', models.IntegerField()),
                ('pair', models.IntegerField()),
                ('purchase_price', models.IntegerField()),
                ('sales_price', models.IntegerField()),
            ],
        ),
    ]
