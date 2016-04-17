#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import click

from calendar import month_abbr
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


FILLED = u'\u25CF'
EMPTY = u'\u25CB'


row_label_formats = {
    'year': '{year:<{max_year_width}}',
    'age': 'Age {age:<{max_age_width}}'
}


class Date(click.ParamType):

    name = 'date'

    def __init__(self, format="%d-%m-%Y"):
        self.format = format

    def convert(self, value, param, ctx):
        try:
            return datetime.strptime(value, self.format).date()
        except ValueError:
            self.fail('%s is not a valid date' % value, param, ctx)


def header(fill=' ', default_width=9, widths={'Feb': 8}):
    return ''.join('{month:{fill}<{width}}'
                   .format(month=abbr, fill=fill,
                           width=widths.get(abbr, default_width))
                   for abbr in month_abbr[1:])


# Week of the year
yweek = lambda d: timedelta(days=d.timetuple().tm_yday) // timedelta(weeks=1)


@click.command()
@click.option('--birth-date',
              '-d',
              type=Date(),
              help='Date of birth (dd-mm-YYYY)',
              prompt='Date of birth (dd-mm-YYYY)')
@click.option('--life-expectancy',
              '-l',
              'expected_years',
              type=int,
              default=85,
              help='Number of years you expect to live')
@click.option('--row-label',
              '-r',
              type=click.Choice(['year', 'age']),
              default='year',
              help='Label for rows')
@click.option('--row-label-period',
              type=int,
              default=5,
              help='Show label after every duration')
@click.option('--highlight-date',
              '-h',
              multiple=True,
              type=Date(),
              help='Dates to highlight')
def main(birth_date, expected_years, row_label, row_label_period, highlight_date):

    expected_death_date = birth_date + relativedelta(years=expected_years)

    expected_death_year = expected_death_date.year
    birth_year = birth_date.year

    curr_date = date.today()

    # ensures that the formatting won't break for those who are alive
    # between 9999 and 10000 A.D. and still using this for some reason
    max_year_width = len(str(expected_death_year)) + 1
    max_age_width = len(str(expected_years)) + 1

    fmt_dct = dict(age=expected_years,
                   year=expected_death_year,
                   max_year_width=max_year_width,
                   max_age_width=max_age_width)
    row_label_len = len(row_label_formats[row_label].format(**fmt_dct))

    # Normalize set of dates to highlight (using set for constant time lookup)
    highlight_set = set(date(d.year, 1, 1) + timedelta(weeks=yweek(d))
                        for d in highlight_date)

    for year in range(birth_year, expected_death_year + 1):

        if year == birth_year:  # Print header on first iteration in loop
            click.echo(' ' * row_label_len, nl=False)
            click.echo(header())

        age = year - birth_year

        if age % row_label_period:
            click.echo(' ' * row_label_len, nl=False)
        else:
            fmt_dct = dict(age=age,
                           year=year,
                           max_year_width=max_year_width,
                           max_age_width=max_age_width)
            click.echo(row_label_formats[row_label].format(**fmt_dct), nl=False)

        date_iter = date(year, 1, 1)

        while date_iter.year == year:
            if birth_date < date_iter < curr_date:
                if date_iter in highlight_set:
                    click.secho(FILLED, nl=False, fg='red')
                else:
                    click.secho(FILLED, nl=False, fg='green')
            else:
                click.echo(EMPTY, nl=False)
            click.echo(' ', nl=False)
            date_iter += timedelta(weeks=1)

        click.echo('')


if __name__ == '__main__':
    main()
