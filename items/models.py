from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('microcontrollers', 'Microcontrollers (Arduino, ESP32)'),
        ('electronics', 'Electronics & Sensors'),
        ('cnc_tools', 'CNC Tools & Parts'),
        ('hardware', 'Hardware (GPU, Server Parts)'),
        ('geospatial', 'Field / GIS Equipment'),
        ('other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New / Sealed'),
        ('good', 'Good condition'),
        ('fair', 'Worn but working'),
        ('poor', 'Needs repair / For parts'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_items')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (x{self.quantity}) - {self.owner.username}"

    class Meta:
        ordering = ['-created_at']


class ItemRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned')
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requester.username} requests {self.item.name}"