from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, get_language
from django.utils import timezone
from django.core.cache import cache
from django.core.validators import MinValueValidator, MaxValueValidator
from uuslug import uuslug

__all__ = ["AbstractCategory", "AbstractCommercialCategory"]


class AbstractCategory(models.Model):
    name = models.CharField(_("name"), max_length=255, db_index=True, unique=True)
    image = models.ImageField(_("image"), upload_to='categories', blank=True)
    slug = models.SlugField(_("slug"), max_length=255, db_index=True)
    is_public = models.BooleanField(
        _("is public"),
        default=True,
        db_index=True,
        help_text=_(
            "Show this category in search results and catalog listings.")
    )

    def get_url_cache_key(self):
        current_locale = get_language()
        cache_key = 'CATEGORY_URL_%s_%s' % (current_locale, self.pk)
        return cache_key

    def get_slug(self):
        cache_key = self.get_url_cache_key()
        slug = cache.get(cache_key)

        if not slug:
            slug = self.slug
            cache.set(cache_key, slug)

        return slug

    def generate_slug(self):
        return uuslug(self.name, instance=self)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
        app_label = "catalog"

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'category-slug': self.slug})


class AbstractCommercialCategory(models.Model):
    name = models.CharField(_("name"), max_length=255, db_index=True)
    description = models.TextField(_("description"), blank=True)
    is_active = models.BooleanField(
        _("is active"),
        db_index=True,
        default=True,
        help_text="Show if the commercial category is available."
    )

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _("Category")
        verbose_name_plural = _("Categories commercial info")
        ordering = ['name']
        app_label = "catalog"
