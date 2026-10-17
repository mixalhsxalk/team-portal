from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('holiday', 'Κανονική Άδεια'),
        ('sick', 'Ασθένεια'),
        ('remote', 'Τηλεργασία / Remote'),
        ('other', 'Άλλο / Προσωπικοί Λόγοι'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Εκκρεμεί'),
        ('approved', 'Εγκρίθηκε'),
        ('rejected', 'Απορρίφθηκε'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, default='holiday')
    start_date = models.DateField(verbose_name='Από')
    end_date = models.DateField(verbose_name='Έως')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, verbose_name='Σημειώσεις / Αιτιολογία')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_leave_type_display()} ({self.start_date} έως {self.end_date})"

    def clean(self):
        # Έλεγχος ώστε η ημερομηνία λήξης να μην είναι πριν την ημερομηνία έναρξης
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Η ημερομηνία λήξης δεν μπορεί να είναι προγενέστερη της ημερομηνίας έναρξης.')

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Αίτημα Άδειας'
        verbose_name_plural = 'Αιτήματα Άδειας'