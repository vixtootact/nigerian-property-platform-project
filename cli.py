import argparse
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from properties.models import Property
from accounts.models import CustomUser
from applications.models import Application


def generate_report():
    print("\n" + "="*55)
    print("   NAIJAHHOMES - PROPERTY STATISTICS REPORT")
    print("="*55)

    total_properties   = Property.objects.count()
    total_users        = CustomUser.objects.count()
    total_applications = Application.objects.count()
    total_landlords    = CustomUser.objects.filter(role='landlord').count()
    total_tenants      = CustomUser.objects.filter(role='tenant').count()

    print(f"\n📊 PLATFORM OVERVIEW")
    print(f"   Total Properties   : {total_properties}")
    print(f"   Total Users        : {total_users}")
    print(f"   Total Landlords    : {total_landlords}")
    print(f"   Total Tenants      : {total_tenants}")
    print(f"   Total Applications : {total_applications}")

    print(f"\n🏠 PROPERTIES BY STATUS")
    for status in ['available', 'rented', 'unavailable']:
        count = Property.objects.filter(status=status).count()
        bar   = '█' * count
        print(f"   {status.capitalize():15} : {bar} ({count})")

    print(f"\n📍 PROPERTIES BY STATE")
    from django.db.models import Count
    by_state = Property.objects.values('state').annotate(count=Count('id')).order_by('-count')
    for item in by_state:
        bar = '█' * item['count']
        print(f"   {item['state']:20} : {bar} ({item['count']})")

    print(f"\n🏡 PROPERTIES BY TYPE")
    by_type = Property.objects.values('property_type').annotate(count=Count('id')).order_by('-count')
    for item in by_type:
        bar = '█' * item['count']
        print(f"   {item['property_type']:20} : {bar} ({item['count']})")

    print(f"\n💰 PRICE ANALYSIS")
    from django.db.models import Avg, Min, Max
    price_stats = Property.objects.aggregate(
        avg_price = Avg('price'),
        min_price = Min('price'),
        max_price = Max('price')
    )
    print(f"   Average Price : ₦{price_stats['avg_price']:,.0f}")
    print(f"   Lowest Price  : ₦{price_stats['min_price']:,.0f}")
    print(f"   Highest Price : ₦{price_stats['max_price']:,.0f}")

    print(f"\n📋 APPLICATIONS BY STATUS")
    for status in ['pending', 'approved', 'rejected']:
        count = Application.objects.filter(status=status).count()
        print(f"   {status.capitalize():15} : {count}")

    print("\n" + "="*55)
    print("   Report generated successfully")
    print("="*55 + "\n")


def generate_charts():
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from django.db.models import Count, Avg
    except ImportError:
        print("Matplotlib not installed. Run: pip install matplotlib")
        return

    print("\nGenerating charts...")

    os.makedirs('charts', exist_ok=True)

    by_state = list(
        Property.objects.values('state')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    states = [item['state'] for item in by_state]
    counts = [item['count'] for item in by_state]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(states, counts, color='#1a6b3c', edgecolor='white', linewidth=0.5)

    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(count),
            ha='center', va='bottom',
            fontweight='bold', fontsize=11
        )

    plt.title('Number of Properties by State', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('State', fontsize=12)
    plt.ylabel('Number of Properties', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('charts/properties_by_state.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: charts/properties_by_state.png")

    by_type = list(
        Property.objects.values('property_type')
        .annotate(count=Count('id'))
    )

    types  = [item['property_type'].capitalize() for item in by_type]
    counts = [item['count'] for item in by_type]

    colors = ['#1a6b3c', '#f0a500', '#2d9b5e', '#e74c3c', '#3498db', '#9b59b6']

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        counts,
        labels=types,
        colors=colors[:len(types)],
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.85
    )

    for autotext in autotexts:
        autotext.set_fontweight('bold')

    plt.title('Property Type Distribution', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('charts/property_types.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: charts/property_types.png")

    avg_prices = list(
        Property.objects.values('state')
        .annotate(avg_price=Avg('price'))
        .order_by('-avg_price')
    )

    states     = [item['state'] for item in avg_prices]
    avg_values = [item['avg_price'] / 1_000_000 for item in avg_prices]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(states, avg_values, color='#f0a500', edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, avg_values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f'₦{val:.1f}M',
            ha='center', va='bottom',
            fontweight='bold', fontsize=9
        )

    plt.title('Average Annual Rent by State', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('State', fontsize=12)
    plt.ylabel('Average Price (₦ Millions)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('charts/avg_price_by_state.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: charts/avg_price_by_state.png")

    print("\nAll 3 charts generated successfully in the charts/ folder.")


def export_csv():
    import csv
    from datetime import datetime

    filename = f"data/properties_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    properties = Property.objects.all()

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow([
            'ID', 'Title', 'Type', 'Location', 'State',
            'LGA', 'Price (NGN)', 'Bedrooms', 'Bathrooms',
            'Status', 'Date Listed'
        ])

        for p in properties:
            writer.writerow([
                p.id, p.title, p.property_type, p.location,
                p.state, p.lga, p.price, p.bedrooms,
                p.bathrooms, p.status, p.created_at.strftime('%Y-%m-%d')
            ])

    print(f"\nExported {properties.count()} properties to: {filename}\n")


def backup_database():
    import shutil
    from datetime import datetime

    source = 'database/property_platform.db'
    backup = f"database/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

    if not os.path.exists(source):
        print("Database file not found.")
        return

    shutil.copy2(source, backup)
    print(f"\nDatabase backed up to: {backup}\n")


def seed_database():
    from seed import seed
    seed()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='NaijaHomes Property Platform - CLI Tool',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('--report',  action='store_true', help='Generate a statistics report')
    parser.add_argument('--charts',  action='store_true', help='Generate Matplotlib charts')
    parser.add_argument('--export',  action='store_true', help='Export properties to CSV')
    parser.add_argument('--backup',  action='store_true', help='Backup the database')
    parser.add_argument('--seed',    action='store_true', help='Load sample data into database')
    parser.add_argument('--all',     action='store_true', help='Run all of the above')

    args = parser.parse_args()

    if args.report or args.all:
        generate_report()

    if args.charts or args.all:
        generate_charts()

    if args.export or args.all:
        export_csv()

    if args.backup or args.all:
        backup_database()

    if args.seed:
        seed_database()

    if not any(vars(args).values()):
        parser.print_help()