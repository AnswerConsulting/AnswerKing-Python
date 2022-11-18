# Generated by Django 4.1.3 on 2022-11-17 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('Created', 'Created'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled')], default='Created', max_length=10)),
                ('order_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=18)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=18)),
                ('retired', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('retired', models.BooleanField(default=False)),
                ('products', models.ManyToManyField(to='answerking_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=18)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answerking_app.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answerking_app.product')),
            ],
            options={
                'unique_together': {('order', 'product')},
            },
        ),
    ]
