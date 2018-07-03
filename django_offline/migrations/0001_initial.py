# Generated by Django 2.0.6 on 2018-07-03 10:45

import _socket
from django.db import migrations, models
import django.db.models.deletion
import django_revision.revision_field
import edc_base.sites.managers
import edc_base.utils
import edc_model_fields.fields.hostname_modification_field
import edc_model_fields.fields.userfield
import edc_model_fields.fields.uuid_auto_field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_model_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_model_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=200, unique=True)),
                ('port', models.IntegerField(default='80')),
                ('api_name', models.CharField(default='v1', max_length=15)),
                ('format', models.CharField(default='json', max_length=15)),
                ('authentication', models.CharField(default='api_key', max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('last_sync_datetime', models.DateTimeField(blank=True, null=True)),
                ('last_sync_status', models.CharField(blank=True, default='-', max_length=250, null=True)),
                ('comment', models.TextField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['hostname', 'port'],
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_model_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_model_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=100, unique=True)),
                ('hostname', models.CharField(max_length=100)),
                ('sent_datetime', models.DateTimeField(default=edc_base.utils.get_utcnow)),
            ],
            options={
                'verbose_name': 'Sent History',
                'verbose_name_plural': 'Sent History',
                'ordering': ('-sent_datetime',),
            },
        ),
        migrations.CreateModel(
            name='IncomingTransaction',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_model_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_model_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('tx', models.BinaryField()),
                ('tx_name', models.CharField(max_length=64)),
                ('tx_pk', models.UUIDField(db_index=True)),
                ('producer', models.CharField(db_index=True, help_text='Producer name', max_length=200)),
                ('action', models.CharField(choices=[('I', 'Insert'), ('U', 'Update'), ('D', 'Delete')], max_length=1)),
                ('timestamp', models.CharField(db_index=True, max_length=50)),
                ('consumed_datetime', models.DateTimeField(blank=True, null=True)),
                ('consumer', models.CharField(blank=True, max_length=200, null=True)),
                ('is_ignored', models.BooleanField(default=False)),
                ('is_error', models.BooleanField(default=False)),
                ('error', models.TextField(blank=True, max_length=1000, null=True)),
                ('prev_batch_id', models.CharField(blank=True, max_length=100, null=True)),
                ('batch_id', models.CharField(blank=True, max_length=100, null=True)),
                ('is_consumed', models.BooleanField(default=False)),
                ('is_self', models.BooleanField(default=False)),
                ('site', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'ordering': ['timestamp'],
            },
            managers=[
                ('on_site', edc_base.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='OutgoingTransaction',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_model_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_model_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('tx', models.BinaryField()),
                ('tx_name', models.CharField(max_length=64)),
                ('tx_pk', models.UUIDField(db_index=True)),
                ('producer', models.CharField(db_index=True, help_text='Producer name', max_length=200)),
                ('action', models.CharField(choices=[('I', 'Insert'), ('U', 'Update'), ('D', 'Delete')], max_length=1)),
                ('timestamp', models.CharField(db_index=True, max_length=50)),
                ('consumed_datetime', models.DateTimeField(blank=True, null=True)),
                ('consumer', models.CharField(blank=True, max_length=200, null=True)),
                ('is_ignored', models.BooleanField(default=False)),
                ('is_error', models.BooleanField(default=False)),
                ('error', models.TextField(blank=True, max_length=1000, null=True)),
                ('prev_batch_id', models.CharField(blank=True, max_length=100, null=True)),
                ('batch_id', models.CharField(blank=True, max_length=100, null=True)),
                ('is_consumed_middleman', models.BooleanField(default=False)),
                ('is_consumed_server', models.BooleanField(default=False)),
                ('using', models.CharField(max_length=25, null=True)),
                ('site', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'ordering': ['timestamp'],
            },
            managers=[
                ('on_site', edc_base.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_model_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_model_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_model_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=200, unique=True)),
                ('port', models.IntegerField(default='80')),
                ('api_name', models.CharField(default='v1', max_length=15)),
                ('format', models.CharField(default='json', max_length=15)),
                ('authentication', models.CharField(default='api_key', max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('last_sync_datetime', models.DateTimeField(blank=True, null=True)),
                ('last_sync_status', models.CharField(blank=True, default='-', max_length=250, null=True)),
                ('comment', models.TextField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['hostname', 'port'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='server',
            unique_together={('hostname', 'port')},
        ),
        migrations.AlterUniqueTogether(
            name='history',
            unique_together={('filename', 'hostname')},
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('hostname', 'port')},
        ),
    ]
