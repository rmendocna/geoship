import sys

from django.db import migrations
from django.core.management import call_command


SHIPS = [
    dict(name="Mathilde Maersk", imo='9632179', flag='DEN', build='2015-06',
         ship_type='Container Ship (Fully Cellular)'),
    dict(name='Australian Spirit', imo='9247455', flag='BHS', build='2004-01',
         ship_type='Crude Oil Tanker'),
    dict(name='MSC Preziosa', imo='9595321', flag='PAN', build='2013-03',
         ship_type='Passenger/Cruise'),
]


def add_ships(apps, schema):
    _ship = apps.get_model('fairing', 'ship')
    for data in SHIPS:
        ship = _ship(**data)
        try:
            ship.save()
        except Exception as e:
            sys.stderr.write('Could not create Ship record: %s' % e)


def import_positions(apps, schema):
    call_command('load_positions', 'fairing/fixtures/positions.csv')


class Migration(migrations.Migration):

    dependencies = [
        ('fairing', '0002_auto_20200907_1552'),
    ]

    operations = [
        migrations.RunPython(add_ships),
        migrations.RunPython(import_positions),
    ]
