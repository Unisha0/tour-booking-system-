from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count
from tour.models import Tourist, Booking


class Command(BaseCommand):
    help = 'Clean up duplicate users and tourists from the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🔍 Scanning for duplicate users...'))
        
        # Find duplicate phone numbers in Tourist model
        duplicate_tourists = Tourist.objects.values('phone').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        deleted_tourists = 0
        deleted_users = 0
        
        for item in duplicate_tourists:
            phone = item['phone']
            tourists = Tourist.objects.filter(phone=phone).order_by('created_at')
            
            self.stdout.write(f'\n📱 Found {item["count"]} tourists with phone: {phone}')
            
            # Keep the oldest one, delete the rest
            tourists_to_delete = tourists[1:]  # Skip the first (oldest) one
            
            for tourist in tourists_to_delete:
                self.stdout.write(f'   ❌ Deleting duplicate tourist: {tourist.name} (ID: {tourist.id})')
                
                # Check if tourist has bookings
                booking_count = Booking.objects.filter(tourist=tourist).count()
                if booking_count > 0:
                    self.stdout.write(self.style.WARNING(
                        f'      ⚠️  This tourist has {booking_count} booking(s). Transferring to main account...'
                    ))
                    # Transfer bookings to the main (first) tourist
                    Booking.objects.filter(tourist=tourist).update(tourist=tourists.first())
                
                # Delete the user account
                user = tourist.user
                tourist.delete()
                
                # Check if user still has other profiles (shouldn't happen, but just in case)
                if not Tourist.objects.filter(user=user).exists():
                    user.delete()
                    deleted_users += 1
                    
                deleted_tourists += 1
        
        # Find duplicate emails
        duplicate_emails = Tourist.objects.exclude(email='').values('email').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        for item in duplicate_emails:
            email = item['email']
            tourists = Tourist.objects.filter(email=email).order_by('created_at')
            
            self.stdout.write(f'\n📧 Found {item["count"]} tourists with email: {email}')
            
            # Keep the oldest one, delete the rest
            tourists_to_delete = tourists[1:]
            
            for tourist in tourists_to_delete:
                self.stdout.write(f'   ❌ Deleting duplicate tourist: {tourist.name} (ID: {tourist.id})')
                
                # Check if tourist has bookings
                booking_count = Booking.objects.filter(tourist=tourist).count()
                if booking_count > 0:
                    self.stdout.write(self.style.WARNING(
                        f'      ⚠️  This tourist has {booking_count} booking(s). Transferring to main account...'
                    ))
                    Booking.objects.filter(tourist=tourist).update(tourist=tourists.first())
                
                # Delete the user account
                user = tourist.user
                tourist.delete()
                
                if not Tourist.objects.filter(user=user).exists():
                    user.delete()
                    deleted_users += 1
                    
                deleted_tourists += 1
        
        # Find users without tourist profiles (orphaned users)
        orphaned_users = User.objects.filter(tourist__isnull=True).exclude(is_staff=True)
        orphaned_count = orphaned_users.count()
        
        if orphaned_count > 0:
            self.stdout.write(f'\n👻 Found {orphaned_count} orphaned user(s) without tourist profile')
            for user in orphaned_users:
                self.stdout.write(f'   ❌ Deleting orphaned user: {user.username}')
                user.delete()
                deleted_users += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        if deleted_tourists > 0 or deleted_users > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Cleanup complete!'))
            self.stdout.write(self.style.SUCCESS(f'   Deleted {deleted_tourists} duplicate tourist(s)'))
            self.stdout.write(self.style.SUCCESS(f'   Deleted {deleted_users} user account(s)'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ No duplicate users found! Database is clean.'))
        
        # Show final stats
        total_tourists = Tourist.objects.count()
        total_users = User.objects.count()
        self.stdout.write(f'\n📊 Current database state:')
        self.stdout.write(f'   Total Tourists: {total_tourists}')
        self.stdout.write(f'   Total Users: {total_users}')
