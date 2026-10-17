from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('holiday', 'Holiday'),
        ('sick', 'Sick leave'),
        ('remote', 'Remote work'),
        ('other', 'Other / Personal'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, default='holiday')
    start_date = models.DateField(verbose_name='Start date')
    end_date = models.DateField(verbose_name='End date')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, verbose_name='Notes / Reason')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_leave_type_display()} ({self.start_date} to {self.end_date})"

    def clean(self):
        # End date must not be before start date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('End date cannot be before start date.')

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Leave request'
        verbose_name_plural = 'Leave requests'