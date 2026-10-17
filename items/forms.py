from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'condition', 'quantity', 'description', 'image']
        labels = {
            'name': 'Equipment name',
            'category': 'Category',
            'condition': 'Condition',
            'quantity': 'Available quantity',
            'description': 'Description / Notes',
            'image': 'Photo',
        }