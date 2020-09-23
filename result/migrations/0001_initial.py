# Generated by Django 3.0.7 on 2020-09-23 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_score', models.IntegerField(default=0)),
                ('exam_score', models.IntegerField(default=0)),
                ('current_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Class')),
                ('current_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Section')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.AcademicSession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Subject')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.AcademicTerm')),
            ],
            options={
                'ordering': ['subject'],
            },
        ),
    ]