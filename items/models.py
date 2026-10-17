from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('microcontrollers', 'Μικροελεγκτές (Arduino, ESP32 κλπ)'),
        ('electronics', 'Ηλεκτρονικά & Αισθητήρες'),
        ('cnc_tools', 'Εργαλεία & Ανταλλακτικά CNC'),
        ('hardware', 'Hardware (GPU, Server Parts)'),
        ('geospatial', 'Εξοπλισμός Πεδίου / GIS'),
        ('other', 'Άλλο'),
    ]

    CONDITION_CHOICES = [
        ('new', 'Καινούριο / Σφραγισμένο'),
        ('good', 'Σε καλή κατάσταση'),
        ('fair', 'Φθαρμένο αλλά λειτουργικό'),
        ('poor', 'Χρειάζεται επισκευή / Για ανταλλακτικά'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_items')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)  # Αντί για is_available
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (x{self.quantity}) - {self.owner.username}"

    class Meta:
        ordering = ['-created_at']


class ItemRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Εκκρεμεί'),
        ('approved', 'Εγκρίθηκε'),
        ('rejected', 'Απορρίφθηκε'),
        ('returned', 'Επεστράφη')
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ο/Η {self.requester.username} ζητάει το: {self.item.name}"