# Generated by Django 2.1 on 2019-07-13 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collegeName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degreeName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DegreeYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userDegreeYear', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=100)),
                ('college', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rsearch.College')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rsearch.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skillName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkillCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userSkillCount', models.PositiveIntegerField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rsearch.PersonalDetails')),
                ('userSkill', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rsearch.Skill')),
            ],
        ),
        migrations.AddField(
            model_name='degreeyear',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rsearch.PersonalDetails'),
        ),
        migrations.AddField(
            model_name='degreeyear',
            name='userDegree',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rsearch.Degree'),
        ),
    ]
