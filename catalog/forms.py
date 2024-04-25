from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product, Version, Category


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ('is_active', 'is_published'):
                field.widget.attrs['class'] = 'form-control'


class CategoryForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class PokemonForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        words_to_delete = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in words_to_delete:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'вы ввели недопустимое слово в наименовании: {word}')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        words_to_delete = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in words_to_delete:
            if word in cleaned_data:
                raise forms.ValidationError(f'вы ввели недопустимое слово в описании: {word}')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    active_count = 0

    class Meta:
        model = Version
        fields = "__all__"

    def clean_second_active_version(self):
        cleaned_data = self.cleaned_data['is_active']
        if cleaned_data:
            VersionForm.active_count += 1
        if VersionForm.active_count > 1:
            VersionForm.active_count = 0
            raise ValidationError('Возможна лишь одна активная версия. Пожалуйста, активируйте только 1 версию.')
        return cleaned_data


class ModeratorPokemonForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published', )
