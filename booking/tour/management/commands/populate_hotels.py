from django.core.management.base import BaseCommand
from tour.models import Hotel, Tour

class Command(BaseCommand):
    help = 'Populate database with hotels for all tour destinations'

    def handle(self, *args, **options):
        # Define hotels for different destinations
        hotels_data = {
            'Kathmandu': [
                {'name': 'Kathmandu Grand Hotel', 'price': 8000},
                {'name': 'Hotel Himalaya', 'price': 6500},
                {'name': 'Radisson Blu Hotel', 'price': 12000},
                {'name': 'Yak & Yeti', 'price': 10500},
                {'name': 'Hotel de l\'Annapurna', 'price': 9500},
                {'name': 'Shanker Hotels', 'price': 7800},
                {'name': 'Dwarika\'s Hotel', 'price': 9800},
            ],
            'Pokhara': [
                {'name': 'The Pavilions Himalayas', 'price': 7500},
                {'name': 'Fulbari Resort & Spa', 'price': 8500},
                {'name': 'Pokhara Lakeside Hotel', 'price': 5000},
                {'name': 'Fish Tail Lodge', 'price': 9000},
                {'name': 'Lakeside Eco Resort', 'price': 6000},
                {'name': 'Barahi Jungle Lodge', 'price': 6500},
                {'name': 'New Pokhara Lodge', 'price': 4500},
            ],
            'Everest': [
                {'name': 'Everest Base Camp Lodge', 'price': 3000},
                {'name': 'Sagarmatha Resort', 'price': 4000},
                {'name': 'Namche Lodge', 'price': 3500},
                {'name': 'Khunde Lodge', 'price': 3200},
                {'name': 'Tengboche Lodge', 'price': 3000},
            ],
            'Annapurna': [
                {'name': 'Annapurna Base Camp Lodge', 'price': 2500},
                {'name': 'Mohare Danda Resort', 'price': 3500},
                {'name': 'Tatopani Hot Spring Lodge', 'price': 2000},
                {'name': 'Poon Hill Lodge', 'price': 2200},
                {'name': 'Jomsom Hotel', 'price': 3000},
            ],
            'Mustang': [
                {'name': 'Marpha Guest House', 'price': 1800},
                {'name': 'Kagbeni Lodge', 'price': 2000},
                {'name': 'Jomsom Hill Hotel', 'price': 2500},
                {'name': 'Lo Manthang Palace Hotel', 'price': 2200},
                {'name': 'Tatopani Lodge', 'price': 1500},
            ],
            'Janakpur': [
                {'name': 'Janakpur Grand Hotel', 'price': 3500},
                {'name': 'Ram Navami Hotel', 'price': 3000},
                {'name': 'Janaki Nivas Hotel', 'price': 2800},
                {'name': 'Devi Hotel', 'price': 2500},
            ],
            'Rara': [
                {'name': 'Rara Lake Resort', 'price': 4500},
                {'name': 'Rara National Park Lodge', 'price': 3500},
                {'name': 'Jumla Forest Lodge', 'price': 3000},
            ],
        }

        created_count = 0
        skipped_count = 0

        for destination, hotels in hotels_data.items():
            self.stdout.write(f'\n📍 Adding hotels for {destination}...')
            
            for hotel_data in hotels:
                hotel, created = Hotel.objects.get_or_create(
                    name=hotel_data['name'],
                    defaults={'price_per_day': hotel_data['price']}
                )
                
                if created:
                    self.stdout.write(f'  ✅ Created: {hotel.name} (Rs. {hotel.price_per_day}/day)')
                    created_count += 1
                else:
                    self.stdout.write(f'  ⏭️  Skipped: {hotel.name} (already exists)')
                    skipped_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n✨ Done!\n  Created: {created_count} hotels\n  Skipped: {skipped_count} hotels'))
