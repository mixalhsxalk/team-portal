from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from items.models import Item, ItemRequest
from timeoff.models import LeaveRequest

PASSWORD = 'demo1234'

ITEMS = {
    'alice': [
        ('ESP32 DevKit V1', 'microcontrollers', 'new', 6, 'WiFi + BLE boards, USB-C.'),
        ('Raspberry Pi 4 (4GB)', 'hardware', 'good', 2, 'With case and power supply.'),
    ],
    'bob': [
        ('Arduino Uno R3', 'microcontrollers', 'good', 4, 'Classic starter board.'),
        ('Digital Multimeter', 'electronics', 'fair', 1, 'Auto-range, works fine.'),
        ('DHT22 Sensor Pack', 'electronics', 'new', 10, 'Temperature & humidity sensors.'),
    ],
    'carol': [
        ('GPS RTK Receiver', 'geospatial', 'good', 1, 'Centimeter-level positioning kit.'),
        ('End Mill Set 3mm', 'cnc_tools', 'new', 3, 'Carbide, 2-flute.'),
        ('Soldering Station', 'other', 'poor', 1, 'Needs a new tip.'),
    ],
}


class Command(BaseCommand):
    help = 'Fills the database with demo users, items, requests and leaves.'

    def handle(self, *args, **options):
        today = timezone.localdate()
        users = {}
        for name in ['demo', 'alice', 'bob', 'carol', 'dave']:
            user, created = User.objects.get_or_create(username=name)
            if created:
                user.set_password(PASSWORD)
                user.is_staff = user.is_superuser = (name == 'demo')
                user.save()
            users[name] = user

        if Item.objects.exists():
            self.stdout.write('Demo data already present, skipping items/leaves.')
            return

        for owner, rows in ITEMS.items():
            for name, cat, cond, qty, desc in rows:
                Item.objects.create(owner=users[owner], name=name, category=cat,
                                    condition=cond, quantity=qty, description=desc)
        Item.objects.create(owner=users['demo'], name='Oscilloscope 100MHz', category='electronics',
                            condition='good', quantity=1, description='2-channel, with probes.')
        Item.objects.create(owner=users['demo'], name='Laser Rangefinder', category='geospatial',
                            condition='new', quantity=2, description='Field measurements up to 100m.')

        scope = Item.objects.get(name='Oscilloscope 100MHz')
        ranger = Item.objects.get(name='Laser Rangefinder')
        ItemRequest.objects.create(item=scope, requester=users['bob'])
        ItemRequest.objects.create(item=ranger, requester=users['carol'], status='approved')
        ranger.quantity -= 1
        ranger.save()
        ItemRequest.objects.create(item=Item.objects.get(name='ESP32 DevKit V1'), requester=users['demo'])
        ItemRequest.objects.create(item=Item.objects.get(name='Arduino Uno R3'), requester=users['demo'],
                                   status='approved')

        d = lambda days: today + timedelta(days=days)
        for user, kind, start, end, status in [
            ('alice', 'holiday', d(-1), d(3), 'approved'),
            ('bob', 'remote', d(0), d(0), 'approved'),
            ('carol', 'holiday', d(7), d(12), 'approved'),
            ('dave', 'sick', d(2), d(3), 'approved'),
            ('demo', 'holiday', d(14), d(18), 'approved'),
            ('demo', 'remote', d(5), d(5), 'pending'),
        ]:
            LeaveRequest.objects.create(user=users[user], leave_type=kind,
                                        start_date=start, end_date=end, status=status)

        self.stdout.write(self.style.SUCCESS(f"Demo data created. Log in as 'demo' / '{PASSWORD}'."))
