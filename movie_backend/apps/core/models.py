from django.db import models


class ContactMessage(models.Model):
    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100, blank=True)
    email = models.EmailField('Email Address')
    phone = models.CharField('Phone Number', max_length=30, blank=True)
    subject = models.CharField('Subject', max_length=255, blank=True)
    message = models.TextField('Message Content')
    is_read = models.BooleanField('Is Read', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.first_name} ({self.email}) - {self.subject or 'No subject'}"
