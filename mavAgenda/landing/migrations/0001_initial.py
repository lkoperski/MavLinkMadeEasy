# Generated by Django 2.1.2 on 2018-11-01 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building_name', models.CharField(max_length=45)),
                ('building_roomNumber', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus_name', models.CharField(choices=[('North Campus', 'North Campus'), ('Scott (South) Campus', 'Scott (South) Campus'), ('Center Street Campus', 'Center Street Campus'), ('Remote', 'Remote')], default=None, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Complete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=75)),
                ('course_subject', models.CharField(max_length=15)),
                ('course_num', models.CharField(max_length=15)),
                ('course_semester', models.CharField(choices=[('All', 'All'), ('Spring', 'Spring'), ('Fall', 'Fall'), ('Summer', 'Summer'), ('Year-Only', 'Year-Only'), ('Spring/Summer', 'Spring/Summer'), ('Fall/Summer', 'Fall/Summer')], default='All', max_length=10)),
                ('course_credits', models.IntegerField()),
                ('course_special', models.CharField(choices=[('No', 'No'), ('Lab', 'Lab'), ('Waiver', 'Waiver')], default=None, max_length=15)),
                ('course_comment', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_diploma', models.CharField(choices=[('Bachelor of Science', 'Bachelor of Science'), ('Master of Science', 'Master of Science'), ('Doctor of Science', 'Doctor of Science')], default='Bachelor of Science', max_length=50)),
                ('degree_type', models.CharField(choices=[('Major', 'Major'), ('Minor', 'Minor'), ('Concentration', 'Concentration')], default='Major', max_length=50)),
                ('degree_track', models.CharField(choices=[('Computer Science', 'Computer Science'), ('Management Information Systems', 'Management Information Systems'), ('Bioinformatics', 'Bioinformatics'), ('IT Innovation', 'IT Innovation'), ('Cybersecurity', 'Cybersecurity')], default='Computer Science', max_length=50)),
                ('degree_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructor_firstName', models.CharField(max_length=20)),
                ('instructor_lastName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offering_time', models.CharField(max_length=20)),
                ('offering_sectionNum', models.IntegerField()),
                ('offering_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landing.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Prereq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prereq_type', models.CharField(choices=[('Corequisite', 'Corequisite'), ('Prerequisite', 'Prerequisite')], max_length=20, null=True)),
                ('prereq_courses', models.ManyToManyField(to='landing.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req_name', models.CharField(max_length=50)),
                ('req_credits', models.IntegerField()),
                ('req_degrees', models.ManyToManyField(to='landing.Degree')),
            ],
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pref_minCredits', models.IntegerField()),
                ('pref_maxCredits', models.IntegerField()),
                ('pref_summer', models.BooleanField()),
                ('pref_summerMinCredits', models.IntegerField()),
                ('pref_summerMaxCredits', models.IntegerField()),
                ('pref_nextSSF', models.CharField(max_length=10, null=True)),
                ('pref_nextYear', models.IntegerField(null=True)),
                ('pref_nextSemMinCredit', models.IntegerField(null=True)),
                ('pref_nextSemMaxCredit', models.IntegerField(null=True)),
                ('pref_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Weekday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday_name', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default=None, max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='offering',
            name='offering_days',
            field=models.ManyToManyField(to='landing.Weekday'),
        ),
        migrations.AddField(
            model_name='offering',
            name='offering_instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landing.Instructor'),
        ),
        migrations.AddField(
            model_name='offering',
            name='offering_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landing.Building'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_requirements',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='landing.Requirement'),
        ),
        migrations.AddField(
            model_name='complete',
            name='complete_courses',
            field=models.ManyToManyField(to='landing.Course'),
        ),
        migrations.AddField(
            model_name='complete',
            name='complete_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='building',
            name='building_campus',
            field=models.ManyToManyField(to='landing.Campus'),
        ),
    ]
