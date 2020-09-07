import csv
import logging

from django.core.management.base import BaseCommand, CommandError
from fairing.models import Ship, ShipPosition

logger = logging.getLogger('command')


class Command(BaseCommand):
    help = """
    Loads ship position data from CSV files in the format
        <IMO:7-digits>, <timestamp:isodatetime+tz>, <latitude:float>, <longitude:float> 
        
    You must declare the full relative or absolute paths, how many you may want to.
    This will NOT update existing records
    """

    def add_arguments(self, parser):
        parser.add_argument('csv_files', nargs='+', type=str)

    def handle(self, *args, **options):

        failed = 0
        success = 0
        verbosity = options['verbosity']

        ship_ids = dict([(a, b) for a, b in Ship.objects.values_list('imo', 'pk')])
        for filename in options['csv_files']:
            with open(filename) as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    try:
                        si = ship_ids[row[0]]
                    except KeyError:
                        msg = 'Could not find Ship with IMO `%s`' % row[0]
                        if verbosity > 1:
                            self.stderr.write(msg)
                        failed += 1
                        logger.error(msg)
                        continue

                    position = ShipPosition(ship_id=si, timestamp=row[1],
                                            latitude=row[2], longitude=row[3])
                    try:
                        position.save()
                    except Exception as e:
                        msg = '%s' % e
                        if verbosity > 1:
                            self.stderr.write(msg)
                        logger.error(msg)
                        failed += 1
                    else:
                        success += 1
        self.stdout.write('Total positions: %d' % (failed + success))
        if failed:
            self.stderr.write('Failed %d' % failed)
            self.stdout.write('Succeeded: %d' % success)
