# Generated by Django 3.2.13 on 2023-02-10 16:12

from django.db import migrations, connection
from psycopg2 import sql

from baserow.contrib.database.fields.models import (
    CreatedOnField,
    DateField,
    FormulaField,
    LastModifiedField,
)


def forward(apps, schema_editor):
    # since all the datetimes saved in the database are in UTC, we need to set the
    # `date_force_timezone` to UTC for all the fields and set `date_show_tzinfo` to
    # True so the user can be aware of the timezone.
    for qs in [
        DateField.objects.filter(date_include_time=True),
        FormulaField.objects.filter(formula_type="date", date_include_time=True),
    ]:
        qs.update(date_force_timezone="UTC", date_show_tzinfo=True)

    # for the created_on and last_modified fields we need to set the
    # `date_force_timezone` to the timezone saved in in the field
    cursor = connection.cursor()
    with connection.schema_editor():
        for Field in [CreatedOnField, LastModifiedField]:
            cursor.execute(
                sql.SQL(
                    "UPDATE {table_name} SET "
                    "date_force_timezone = timezone, date_show_tzinfo = true "
                    "WHERE date_include_time = true"
                ).format(
                    table_name=sql.Identifier(Field._meta.db_table),
                )
            )


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0101_add_timezone_attrs_for_datetimes"),
    ]

    operations = [
        migrations.RunPython(forward, migrations.RunPython.noop),
    ]
