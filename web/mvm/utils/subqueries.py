from django.db.models import PositiveIntegerField, Subquery


class SubqueryCount(Subquery):
    # Custom Count function to just perform simple count on any queryset without grouping.
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = PositiveIntegerField()
