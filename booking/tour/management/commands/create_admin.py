from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tour.models import AdminUser


class Command(BaseCommand):
    help = 'Create default admin account'

    def handle(self, *args, **options):
        email = 'admin@gmail.com'
        password = 'admin123'
        username = email
        full_name = 'System Administrator'

        # Check if admin already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('Admin account already exists!'))
            return

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        # Create AdminUser
        AdminUser.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            is_super_admin=True
        )

        self.stdout.write(self.style.SUCCESS(f'✅ Admin account created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
        self.stdout.write(self.style.SUCCESS(f'Login at: /admin-panel/login/'))
