from django import forms
from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm
from mainapp.models import ProductCategories, Product


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategories
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
                continue
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_name(self):
        data = self.cleaned_data['name']
        if not data:
            raise forms.ValidationError("Нельзя создать категорию без имени!")

        return data


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
                continue
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-select'
                continue
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_name(self):
        data = self.cleaned_data['name']
        if not data:
            raise forms.ValidationError("Нельзя создать продукт без имени!")

        return data

    def clean_category(self):
        data = self.cleaned_data['category']
        if not data:
            raise forms.ValidationError("Нельзя создать продукт без категории!")

        return data
