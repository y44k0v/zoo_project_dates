from django import forms


class AnimalSearchForm(forms.Form):
    """
    A form for searching animals by any of their attributes.
    All fields are optional so users can search by one or more criteria.
    """
    name = forms.CharField(
        required=False,
        label="Name contains",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Lion'})
    )
    min_age = forms.IntegerField(
        required=False,
        label="Minimum age",
        min_value=0
    )
    max_age = forms.IntegerField(
        required=False,
        label="Maximum age",
        min_value=0
    )
    min_weight = forms.FloatField(
        required=False,
        label="Minimum weight (kg)",
        min_value=0
    )
    max_weight = forms.FloatField(
        required=False,
        label="Maximum weight (kg)",
        min_value=0
    )
    born_in_captivity = forms.NullBooleanField(
        required=False,
        label="Born in captivity",
        widget=forms.Select(choices=[
            ('', 'Any'),
            ('true', 'Yes'),
            ('false', 'No'),
        ])
    )