# Generated by Django 4.0.4 on 2022-05-27 13:37

import airplane.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('passenger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='AirplaneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='airplane type')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='type description')),
                ('weight', models.PositiveIntegerField(blank=True, null=True, verbose_name='weight')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='height')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('destination_from', models.CharField(max_length=250, verbose_name='from')),
                ('destination_to', models.CharField(max_length=250, verbose_name='to')),
                ('deptures', models.DateTimeField(verbose_name='depture')),
                ('arrives', models.DateTimeField(default=airplane.models.Flight.arrives_default, verbose_name='arrives')),
                ('airplane', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='flights', to='airplane.airplane')),
                ('passengers', models.ManyToManyField(related_name='flights', to='passenger.passenger', verbose_name='passengers')),
            ],
        ),
        migrations.AddField(
            model_name='airplane',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='airplane.airplanetype'),
        ),
    ]