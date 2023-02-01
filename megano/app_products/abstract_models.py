from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractImageModel(models.Model):
    image = models.ImageField(_("image"), upload_to="products")
    product = models.ForeignKey(
        'product.Product', verbose_name=_("product_image"), on_delete=models.CASCADE, related_name='images',
    )

    @property
    def url(self):
        return f'{settings.MEDIA_URL}{self.image.name}'

    class Meta:
        abstract = True
        verbose_name = _("image")
        verbose_name_plural = _("images")
        app_label = "product"


class AbstractProductClass(models.Model):
    name = models.CharField(_("name"), max_length=255, db_index=True, unique=True)
    description = models.TextField(_("description"), blank=True)
    short_description = models.CharField("short description", max_length=255, blank=True)
    categories = models.ManyToManyField("catalog.Category", related_name="products")
    data = models.JSONField(
        _("the product specifications"), name="specifications",
    )

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
    product = models.OneToOneField(
        'product.Product', verbose_name=_('Product'), on_delete=models.CASCADE, related_name="commercial"
    )

    is_active = models.BooleanField(
        _("is active"),
        default=True,
        db_index=True,
        help_text="Show if product is active and available to search."
    )

    highlights = models.ManyToManyField(
        "catalog.CategoryCommercial", related_name="products", blank=True
    )

    class Meta:
        abstract = True
        verbose_name = _("Product commercial info")
        verbose_name_plural = _("Products commercial info")
        ordering = ['price']
        app_label = "product"
