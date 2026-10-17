from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'condition', 'quantity', 'description', 'image']
        labels = {
            'name': 'Όνομα Εξοπλισμού',
            'category': 'Κατηγορία',
            'condition': 'Κατάσταση',
            'quantity': 'Διαθέσιμη Ποσότητα',
            'description': 'Περιγραφή / Σημειώσεις',
            'image': 'Φωτογραφία',
        }