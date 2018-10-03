# Generated by Django 2.1.2 on 2018-10-02 22:05

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
            name='SoccerMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('finished', models.BooleanField(default=False)),
                ('home_result', models.PositiveIntegerField(blank=True, null=True)),
                ('away_result', models.PositiveIntegerField(blank=True, null=True)),
                ('home_penalty', models.PositiveIntegerField(blank=True, null=True)),
                ('away_penalty', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Soccer matches',
                'db_table': 'psh_soccer_match',
                'ordering': ['start_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SoccerMatchPrediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normal_badge', models.PositiveIntegerField(blank=True, choices=[(0, 'Royal'), (1, 'Full House'), (2, 'Straight'), (3, 'Eyeless')], null=True)),
                ('exceptional_badge', models.PositiveIntegerField(blank=True, choices=[(4, 'Oracle'), (5, 'Nostradamus'), (6, 'Trelawney'), (8, 'Nothing')], null=True)),
                ('created_on', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField()),
                ('edit_count', models.PositiveIntegerField(default=0)),
                ('concluded', models.BooleanField(default=False)),
                ('home_result', models.PositiveIntegerField()),
                ('away_result', models.PositiveIntegerField()),
                ('home_penalty', models.PositiveIntegerField(blank=True, null=True)),
                ('away_penalty', models.PositiveIntegerField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='web.SoccerMatch')),
                ('foreteller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'psh_soccer_prediction',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SoccerTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fifa_code', models.CharField(blank=True, max_length=10, null=True)),
                ('iso2', models.CharField(blank=True, max_length=3, null=True)),
                ('flag', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'psh_soccer_team',
            },
        ),
        migrations.CreateModel(
            name='SoccerTournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('web_link', models.URLField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('finished', models.BooleanField(default=False)),
                ('number_of_teams', models.PositiveIntegerField()),
                ('type', models.PositiveIntegerField(choices=[(0, 'League Tournament'), (1, 'Knockout Tournament'), (2, 'Mixed Tournament')])),
            ],
            options={
                'db_table': 'psh_soccer_tournament',
                'ordering': ['start_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('royal', models.PositiveIntegerField(default=0)),
                ('full_house', models.PositiveIntegerField(default=0)),
                ('straight', models.PositiveIntegerField(default=0)),
                ('eye_less', models.PositiveIntegerField(default=0)),
                ('oracle', models.PositiveIntegerField(default=0)),
                ('nostradamus', models.PositiveIntegerField(default=0)),
                ('trelawney', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'summaries',
                'db_table': 'psh_summary',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'psh_topic',
            },
        ),
        migrations.AddField(
            model_name='soccertournament',
            name='summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Summary'),
        ),
        migrations.AddField(
            model_name='soccertournament',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='soccertournament_set', to='web.Topic'),
        ),
        migrations.AddField(
            model_name='soccermatchprediction',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='web.SoccerTeam'),
        ),
        migrations.AddField(
            model_name='soccermatch',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_matches', to='web.SoccerTeam'),
        ),
        migrations.AddField(
            model_name='soccermatch',
            name='event_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='matches', to='web.SoccerTournament'),
        ),
        migrations.AddField(
            model_name='soccermatch',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_matches', to='web.SoccerTeam'),
        ),
        migrations.AddField(
            model_name='soccermatch',
            name='summary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Summary'),
        ),
        migrations.AddField(
            model_name='soccermatch',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.SoccerTeam'),
        ),
        migrations.AlterUniqueTogether(
            name='soccermatchprediction',
            unique_together={('foreteller', 'event')},
        ),
    ]
