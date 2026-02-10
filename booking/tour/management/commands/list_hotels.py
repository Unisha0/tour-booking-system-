from tour.models import Hotel

print("\n" + "="*70)
print("🏨 HOTELS IN DATABASE - COMPLETE LISTING")
print("="*70 + "\n")

# Get all hotels
all_hotels = Hotel.objects.all().order_by('name')

if all_hotels.exists():
    print(f"Total Hotels: {all_hotels.count()}\n")
    
    # Define location keywords
    locations = {
        '🏔️ KATHMANDU': ['Kathmandu', 'Himalaya', 'Radisson', 'Yak & Yeti', 'Annapurna', 'Shanker', 'Dwarika'],
        '🌄 POKHARA': ['Pokhara', 'Pavilions', 'Fulbari', 'Fish Tail', 'Lakeside', 'Barahi', 'New Pokhara'],
        '⛰️ EVEREST BASE CAMP': ['Everest', 'Sagarmatha', 'Namche', 'Khunde', 'Tengboche'],
        '🏔️ ANNAPURNA': ['Annapurna', 'Mohare', 'Poon Hill', 'Jomsom', 'Tatopani'],
        '🗻 MUSTANG': ['Marpha', 'Kagbeni', 'Lo Manthang'],
        '🕉️ JANAKPUR': ['Janakpur', 'Ram Navami', 'Janaki', 'Devi'],
        '🏞️ RARA': ['Rara', 'Jumla'],
    }
    
    for location_name, keywords in locations.items():
        location_hotels = []
        for keyword in keywords:
            location_hotels.extend(all_hotels.filter(name__icontains=keyword).distinct())
        
        if location_hotels:
            print(f"{location_name}")
            print("-" * 70)
            for i, hotel in enumerate(location_hotels, 1):
                print(f"  {i}. {hotel.name:<50} Rs. {hotel.price_per_day:>6}/night")
            print()
    
    print("="*70)
    print("\n✅ All hotels are ready for booking!\n")
else:
    print("❌ No hotels found in database!")
