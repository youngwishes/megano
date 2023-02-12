from django.db import models


class ProductQuerySet(models.QuerySet):

    def price_range(self, **kwargs):
        price_from = kwargs['price_from']
        price_to = kwargs['price_to']

        if price_to and price_from:
            return self.filter(commercial__price__range=[price_from, price_to])

        return self

    def get_names(self, **kwargs):
        name = kwargs['name']
        queryset = self.filter(name__istartswith=name) | self.filter(name__iendswith=name)

        if len(name) > 2:
            queryset = queryset | self.filter(name__icontains=name)

        return queryset

    def in_stock(self, **kwargs):
        return self.filter(commercial__count__gt=0)

    def catalog_filter(self, params: dict):
        queryset = None

        for key, value in params.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if queryset is None:
                    queryset = attr(**value)
                else:
                    queryset = queryset & attr(**value)

        return queryset


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model)


class ProductCommercialQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductCommercialManager(models.Manager):
    def get_queryset(self):
        return ProductCommercialQuerySet(self.model)

    def active(self):
        return self.get_queryset().active()
