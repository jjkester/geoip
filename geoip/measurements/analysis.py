from copy import copy
from django.db.models import Avg, Q
from django.utils.translation import ugettext as _
import pygal
from pygal.style import DefaultStyle
from geoip.databases.models import Database


class DataSetAnalysis(object):
    """
    Class for analyzing data sets.
    """
    def __init__(self, dataset):
        """
        :param dataset: The data set to analyze.
        """
        self.object = dataset
        self.databases = Database.objects.filter(measurements__dataset=self.object).distinct()

        self.chart_style = DefaultStyle()
        self.chart_style.background = '#FFFFFF'
        self.chart_options = dict(
            print_values=True,
            style=self.chart_style,
            legend_at_bottom=True,
        )

    def averages(self):
        """Measurement averages for the whole data set."""
        aggregates = self.object.measurements.all()\
            .aggregate(
                accuracy_ipv4=Avg('ipv4_distance'),
                accuracy_ipv6=Avg('ipv6_distance'),
                accuracy_difference=Avg('mutual_distance'),
            )
        return aggregates

    def database_averages(self):
        """Measurement averages per database."""
        data = []

        for database in self.databases:
            aggregates = self.object.measurements.filter(database=database).exclude(ipv4_distance=None)\
                .aggregate(
                    accuracy_ipv4=Avg('ipv4_distance'),
                    accuracy_ipv6=Avg('ipv6_distance'),
                    accuracy_difference=Avg('mutual_distance'),
                )

            data.append(dict(
                database=database,
                **aggregates
            ))

        return data

    def database_counts(self):
        """Measurement counts per database."""
        data = []

        for database in self.databases:
            data.append(dict(
                database=database,
                all=self.object.measurements.filter(database=database).count(),
                complete=self.object.measurements.filter(database=database).exclude(ipv4_location=None).exclude(ipv6_location=None).count(),
                incomplete=self.object.measurements.filter(database=database).filter(Q(ipv4_location=None) | Q(ipv6_location=None)).count(),
                only_v6=self.object.measurements.filter(database=database).exclude(ipv6_location=None).filter(ipv4_location=None).count(),
                only_v4=self.object.measurements.filter(database=database).exclude(ipv4_location=None).filter(ipv6_location=None).count(),
                none=self.object.measurements.filter(database=database).filter(ipv4_location=None, ipv6_location=None).count(),
            ))

        return data

    def database_accuracies(self, points):
        """Accuracy of measured databases for the given distance points (in kms)"""
        data = []

        query_v4 = lambda d, p: self.object.measurements.exclude(ipv4_distance=None).filter(database=d, ipv4_distance__lte=p).count()
        query_v6 = lambda d, p: self.object.measurements.exclude(ipv6_distance=None).filter(database=d, ipv6_distance__lte=p).count()

        for database in self.databases:
            data.append(dict(
                database=database,
                points=points,
                ipv4=list(map(lambda point: query_v4(database, point), points)),
                ipv6=list(map(lambda point: query_v6(database, point), points)),
                total=self.object.measurements.filter(database=database).count(),
            ))
        return data

    def database_averages_chart(self, for_embed=True):
        data = self.database_averages()

        chart = pygal.Bar(legend_at_bottom_columns=3, value_formatter=lambda x: '%.1f km' % x, **self.chart_options)
        chart.x_labels = [row['database'].name for row in data]

        chart.add(_("Average IPv4 deviation"), [row['accuracy_ipv4'] for row in data])
        chart.add(_("Average IPv6 deviation"), [row['accuracy_ipv6'] for row in data])
        chart.add(_("Average mutual deviation"), [row['accuracy_difference'] for row in data])

        return chart.render(disable_xml_declaration=for_embed)

    def database_counts_chart(self, for_embed=True):
        data = self.database_counts()

        chart = pygal.Bar(legend_at_bottom_columns=3, range=(0, max([max(row['only_v4'], row['only_v6'], row['none']) for row in data])), **self.chart_options)
        chart.x_labels = [row['database'].name for row in data]

        # chart.add(_("Complete"), [row['complete'] for row in data])
        chart.add(_("Only IPv4"), [row['only_v4'] for row in data])
        chart.add(_("Only IPv6"), [row['only_v6'] for row in data])
        chart.add(_("None"), [row['none'] for row in data])

        return chart.render(disable_xml_declaration=for_embed)

    def database_accuracies_chart(self, for_embed=True):
        points = range(0, 1001, 10)

        data = self.database_accuracies(points)

        chart_options = copy(self.chart_options)
        chart_options['print_values'] = False
        chart = pygal.XY(legend_at_bottom_columns=2, range=(0, 100), xrange=(0, 1000), **chart_options)
        chart.x_labels = map(lambda x: '%d km' % x, range(0, 1001, 100))
        chart.y_labels = map(lambda x: '%d%%' % x, range(0, 101, 10))

        for row in data:
            # chart.add('%s IPv4' % row['database'].name, row['ipv4'])
            # chart.add('%s IPv6' % row['database'].name, row['ipv6'])
            chart.add('%s IPv4' % row['database'].name, list(zip(points, map(lambda x: (x / row['total']) * 100, row['ipv4']))))
            chart.add('%s IPv6' % row['database'].name, list(zip(points, map(lambda x: (x / row['total']) * 100, row['ipv6']))))

        return chart.render(disable_xml_declaration=for_embed)

    def database_accuracies_large_chart(self, for_embed=True):
        points = range(6000, 20001, 10)

        data = self.database_accuracies(points)

        chart_options = copy(self.chart_options)
        chart_options['print_values'] = False
        chart_options['width'] = 1600
        chart_options['height'] = 600
        chart = pygal.XY(legend_at_bottom_columns=3, range=(85, 100), xrange=(6000, 20000), **chart_options)
        chart.x_labels = map(lambda x: '%d km' % x, range(6000, 20001, 1000))
        chart.y_labels = map(lambda x: '%d%%' % x, range(85, 101, 1))

        for row in data:
            # chart.add('%s IPv4' % row['database'].name, row['ipv4'])
            # chart.add('%s IPv6' % row['database'].name, row['ipv6'])
            chart.add('%s IPv4' % row['database'].name, list(zip(points, map(lambda x: (x / row['total']) * 100, row['ipv4']))), show_dots=False)
            chart.add('%s IPv6' % row['database'].name, list(zip(points, map(lambda x: (x / row['total']) * 100, row['ipv6']))), show_dots=False)

        return chart.render(disable_xml_declaration=for_embed)
