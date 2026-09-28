from django.db import models


class Property(models.Model):
    TYPE_CHOICES = [
        ('apartment',    'Apartment'),
        ('duplex',       'Duplex'),
        ('bungalow',     'Bungalow'),
        ('self-contain', 'Self Contain'),
        ('room',         'Room'),
        ('mansion',      'Mansion'),
    ]

    STATUS_CHOICES = [
        ('available',   'Available'),
        ('rented',      'Rented'),
        ('unavailable', 'Unavailable'),
    ]

    title         = models.CharField(max_length=200)
    description   = models.TextField(blank=True, default='')
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location      = models.CharField(max_length=200)
    state         = models.CharField(max_length=100)
    lga           = models.CharField(max_length=100, blank=True, default='')
    price         = models.FloatField()
    bedrooms      = models.IntegerField(default=0)
    bathrooms     = models.IntegerField(default=0)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    landlord_id   = models.IntegerField()
    image_url     = models.TextField(blank=True, default='')
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'properties'

    def __str__(self):
        return f"{self.title} - {self.location}, {self.state}"

    def to_dict(self):
        return {
            'id':            self.id,
            'title':         self.title,
            'description':   self.description,
            'property_type': self.property_type,
            'location':      self.location,
            'state':         self.state,
            'lga':           self.lga,
            'price':         self.price,
            'bedrooms':      self.bedrooms,
            'bathrooms':     self.bathrooms,
            'status':        self.status,
            'landlord_id':   self.landlord_id,
            'image_url':     self.image_url,
            'created_at':    str(self.created_at),
        }