from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.cache import cache


class AbstractProductClass(models.Model):
    name = models.CharField(_("name"), max_length=255, db_index=True, unique=True)
    description = models.TextField(_("description"), blank=True)
    short_description = models.CharField("short description", max_length=255, blank=True)
    category = models.ManyToManyField("catalog.Category", related_name="products")
    image = models.ImageField(_("image"), upload_to="products")

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

    class Meta:
        abstract = True
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']
        app_label = "product"


class AbstractProductCommercialClass(models.Model):
    vendor_code = models.CharField(_("vendor code"), db_index=True, unique=True, max_length=512)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    count = models.IntegerField(verbose_name=_("left in stock"))
    product = models.OneToOneField('product.Product', verbose_name=_('Product'), on_delete=models.CASCADE)

    is_active = models.BooleanField(
        _("is active"),
        default=True,
        db_index=True,
        help_text="Show if product is active and available to search."
    )

    slug = models.SlugField(_("slug"), db_index=True, unique=True)

    category = models.ManyToManyField(
        "catalog.CategoryCommercial", related_name="products",
    )

    def generate_slug(self):
        self.vendor_code = self.generate_vendor_code()
        return slugify(self.vendor_code)

    def get_product_name(self):
        return self.product.get_name()

    def generate_vendor_code(self):
        return "MG-%s-%s" % (self.get_product_name(), self.pk) if not self.vendor_code else self.vendor_code

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        return super(AbstractProductCommercialClass, self).save(args, kwargs)

    def get_absolute_url(self):
        return reverse('product', kwargs={
            "product_slug": self.slug
        })

    class Meta:
        abstract = True
        verbose_name = _("Product commercial info")
        verbose_name_plural = _("Products commercial info")
        ordering = ['price']
        app_label = "product"
