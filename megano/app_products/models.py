from uuslug import uuslug
from megano.core.loading import is_model_registered
from .abstract_models import *
from django.urls import reverse
from django.core.cache import cache

__all__ = []

if not is_model_registered("product", "ProductImage"):
    class ProductImage(AbstractImageModel):
        pass


    __all__.append('ProductImage')

if not is_model_registered("product", "Product"):
    class Product(AbstractProductClass):

        def get_name(self):
            cache_key = self.get_name_cache_key()
            name = cache.get(cache_key)

            if not name:
                name = self.name
                cache.set(cache_key, name)

            return name

        def get_name_cache_key(self):
            return "PRODUCT_NAME_%s" % self.pk

        def __str__(self):
            return self.name


    __all__.append("Product")

if not is_model_registered("product", "ProductCommercial"):
    class ProductCommercial(AbstractProductCommercialClass):
        def generate_slug(self):
            self.vendor_code = self.generate_vendor_code()
            return uuslug(self.vendor_code, instance=self)

        def get_product_name(self):
            return self.product.get_name()

        def generate_vendor_code(self):
            return uuslug(
                "mg-%s-%s" % (self.get_product_name(), self.pk) if not self.vendor_code
                else self.vendor_code, instance=self
            )

        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = self.generate_slug()
            return super(AbstractProductCommercialClass, self).save(args, kwargs)

        def get_absolute_url(self):
            return reverse('product', kwargs={
                "product_slug": self.slug
            })


    __all__.append("ProductCommercial")
