from django.db import models


class ProductQuerySet(models.QuerySet):
    def price_in_range(self, **kwargs):
        price_from = kwargs['price_from']
        price_to = kwargs['price_to']

        return self.filter(commercial__price__range=[price_from, price_to])

    def name_filter(self, **kwargs):
        name = kwargs['name']
        return self.filter(name__istartswith=name) | \
            self.filter(name__iendswith=name) | \
            self.filter(name__contains=name)

    def in_stock(self):
        return self.filter(commercial__count__gt=0)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model)

    def get_names(self, **kwargs):
        return self.get_queryset().name_filter(**kwargs)

    def price_range(self, **kwargs):
        return self.get_queryset().price_in_range(**kwargs)

    def in_stock(self, **kwargs):
        return self.get_queryset().in_stock()

    def catalog_filter(self, params: dict):
        queryset = None

        for key, value in params.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if not queryset:
                    queryset = attr(**value)
                else:
                    queryset.intersection(attr(**value))

        return queryset


class ProductCommercialQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductCommercialManager(models.Manager):
    def get_queryset(self):
        return ProductCommercialQuerySet(self.model)

    def active(self):
        return self.get_queryset().active()
