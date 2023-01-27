from django import forms
from django.utils.translation import gettext_lazy as _
from megano.core.loading import get_model

Category = get_model('catalog', 'Category')


class GlobalSettingsForm(forms.Form):
    delivery_prices_difference = forms.DecimalField(
        max_digits=7, decimal_places=2,
        required=False,
        help_text=_("Value that specify the difference in price between"
                    " basic delivery and express delivery"),
    )

    BOOLEAN_OPTIONS = (
        ("Y", _("Yes")),
        ("N", _("No")),
    )

    is_payment_available = forms.ChoiceField(
        label=_("Is payment available"), choices=BOOLEAN_OPTIONS, required=False,
        help_text=_("Choose 'Yes' if payment is available at the current moment on the site."
                    "Otherwise, the user will not be able to pay."),
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(),
        required=False, label=_("Available categories"),
        help_text=_("Select the categories that available on the site for viewing."),
    )

    min_price_to_free_delivery = forms.DecimalField(
        max_digits=6, decimal_places=2, label=_("Minimal order price"),
        help_text=_("Minimal total price for getting free delivery"),
    )

    basic_delivery_price = forms.DecimalField(
        max_digits=6, decimal_places=2, label=_("Basic delivery price"),
        help_text=_("This price will be payed by the customer if his order price "
                    "will be less than value of 'Minimal order price'"),
    )

    PROMOTIONS_CHOICES = (
        ("L", _("Limited edition")),
        ("H", _("Hot offers")),
    )

    # Будет тоже самое, что и с categories, пока просто ещё не созданы модели.
    promotions = forms.MultipleChoiceField(
        choices=PROMOTIONS_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text=_("Select the promotions that available on the site."),

    )

    reviews = forms.ChoiceField(
        required=False,
        choices=BOOLEAN_OPTIONS,
        label=_("Is reviews adding is available"),
        help_text=_("Choose 'Yes' if an adding reviews is available at the current moment on the site."
                    "Otherwise, the user will not be able to add review to the product."),

    )
