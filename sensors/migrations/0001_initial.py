# Generated by Django 2.2.2 on 2019-06-17 06:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('sensor_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TestConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum_temp', models.FloatField(default=-10, null=True)),
                ('activation_energy', models.FloatField(default=41000, null=True)),
                ('gas_constant', models.FloatField(default=8.314, null=True)),
                ('ref_temp', models.FloatField(default=23.0, null=True)),
                ('ultimate_strength', models.FloatField(default=50.0, null=True)),
                ('a', models.FloatField(default=3.45, null=True)),
                ('b', models.FloatField(default=0.9, null=True)),
                ('sensor', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sensors.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Strength_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concrete_age', models.FloatField()),
                ('concrete_strength', models.FloatField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('sensor', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sensors.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Maturity_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equivalent_age', models.FloatField()),
                ('matu_index', models.FloatField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('sensor', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sensors.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_taken', models.DateTimeField()),
                ('ave_temp', models.FloatField()),
                ('ave_hum', models.FloatField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensors.Sensor')),
            ],
        ),
    ]
