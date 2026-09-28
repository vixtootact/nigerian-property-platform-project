import os
import sys
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from accounts.models import CustomUser
from properties.models import Property


def seed():
    print("Starting database seed...")

    if not CustomUser.objects.filter(email='landlord@demo.com').exists():
        landlord = CustomUser.objects.create_user(
            username   = 'landlord@demo.com',
            email      = 'landlord@demo.com',
            password   = 'password123',
            first_name = 'Demo',
            last_name  = 'Landlord',
            phone      = '08012345678',
            role       = 'landlord'
        )
        print(f"Created demo landlord with ID: {landlord.id}")
    else:
        landlord = CustomUser.objects.get(email='landlord@demo.com')
        print("Demo landlord already exists.")

    if not CustomUser.objects.filter(email='tenant@demo.com').exists():
        tenant = CustomUser.objects.create_user(
            username   = 'tenant@demo.com',
            email      = 'tenant@demo.com',
            password   = 'password123',
            first_name = 'Demo',
            last_name  = 'Tenant',
            phone      = '08087654321',
            role       = 'tenant'
        )
        print(f"Created demo tenant with ID: {tenant.id}")
    else:
        print("Demo tenant already exists.")

    json_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_properties.json')

    with open(json_path, 'r') as f:
        properties = json.load(f)

    print(f"\nFound {len(properties)} properties in JSON file.")

    inserted = 0

    for prop in properties:
        if Property.objects.filter(title=prop['title']).exists():
            print(f"  Skipping (already exists): {prop['title']}")
            continue

        Property.objects.create(
            title         = prop['title'],
            description   = prop['description'],
            property_type = prop['property_type'],
            location      = prop['location'],
            state         = prop['state'],
            lga           = prop['lga'],
            price         = prop['price'],
            bedrooms      = prop['bedrooms'],
            bathrooms     = prop['bathrooms'],
            status        = prop['status'],
            landlord_id   = landlord.id
        )
        inserted += 1
        print(f"  Added: {prop['title']}")

    print(f"\nDone! {inserted} properties added.")
    print("\nDemo Accounts:")
    print("  Landlord: landlord@demo.com / password123")
    print("  Tenant:   tenant@demo.com   / password123")


if __name__ == '__main__':
    seed()