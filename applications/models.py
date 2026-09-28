from django.db import models
from properties.models import Property


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    tenant_id  = models.IntegerField()
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message    = models.TextField(blank=True, default='')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'applications'

    def __str__(self):
        return f"Application {self.id} - Tenant {self.tenant_id} for {self.property.title}"

    def to_dict(self):
        return {
            'id':                self.id,
            'property_id':       self.property.id,
            'property_title':    self.property.title,
            'property_location': self.property.location,
            'property_state':    self.property.state,
            'property_price':    self.property.price,
            'property_type':     self.property.property_type,
            'property_status':   self.property.status,
            'tenant_id':         self.tenant_id,
            'status':            self.status,
            'message':           self.message,
            'applied_at':        str(self.applied_at),
        }