# Storing and visualising ship positional data

This app allows visualising positional data of sea ships
on a map.

The data can be stored by importing CSV files using the comand line as follows:

    code$ python manage.py load_positions <filename1> <filename2> ...
    
each file containing as many position records as it likes
    
Each row of a positions file has the structure

    <7-digit-imo>, <timestamp-with-tz>, <latitude>, <longitude>
    
## Notes

```
    /code # python manage.py shell
    Python 3.8.5 (default, Aug  4 2020, 04:11:56) 
    [GCC 9.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from fairing.models import Ship
    >>> new_data = dict(imo='7528843', name='RESOLVE PIONEER', ship_type='1005',)
    >>> new_ship = Ship(**new_data)
    >>> new_ship.save()
    >>> 
    now exiting InteractiveConsole...
    /code # python manage.py load_positions fairing/fixtures/
    .DS_Store            positions.csv        resolve_pioneer.csv
    /code # python manage.py load_positions fairing/fixtures/resolve_pioneer.csv 
    Total positions: 396
    /code # 
```