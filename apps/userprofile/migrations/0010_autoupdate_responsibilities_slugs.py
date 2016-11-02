from __future__ import unicode_literals

from django.db import migrations, models
from django.template.defaultfilters import slugify


def update_all_slugs(apps, schema_editor):

    db_alias = schema_editor.connection.alias

    Responsibility = apps.get_model("userprofile", "Responsibility")

    without_slug = Responsibility.objects.using(db_alias).filter(slug=None)

    for item in without_slug:

        try:
            item.slug = slugify(item.name)
            item.save()
        except Exception:
            print('Fail when update slug from item: [{}]'.format(item.pk))


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_responsibility_slug'),
    ]

    operations = [
        migrations.RunPython(update_all_slugs),
    ]