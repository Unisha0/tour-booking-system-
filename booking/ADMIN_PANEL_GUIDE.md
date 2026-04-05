# 🛡️ Custom Admin Panel - SajiloYatra

## Overview
A fully custom admin dashboard for managing your tour booking system, completely separate from Django's default admin panel.

## Admin Login Credentials

**Default Admin Account:**
- **Email:** `admin@gmail.com`
- **Password:** `admin123`

## Access URLs

- **Admin Login:** `http://127.0.0.1:8000/admin-panel/login/`
- **Admin Signup:** `http://127.0.0.1:8000/admin-panel/signup/`
- **Admin Dashboard:** `http://127.0.0.1:8000/admin-panel/dashboard/`

## Features

### 🎯 Main Dashboard (`/admin-panel/dashboard/`)
- Overview statistics
  - Total Bookings
  - Confirmed/Pending/Cancelled Bookings
  - Total Tourists
  - Total Tours & Active Tours
  - Revenue tracking
- Recent bookings table
- Popular tours list

### 📅 Bookings Management (`/admin-panel/bookings/`)
- View all bookings
- Filter by status (Pending/Confirmed/Cancelled)
- Search by tourist name, email, or tour
- View detailed booking information
- Cancel bookings
- See payment status

### 👥 Tourists Management (`/admin-panel/tourists/`)
- View all registered tourists
- Search by name, email, or phone
- View individual tourist profiles
- See booking history for each tourist

### 🗺️ Tours Management (`/admin-panel/tours/`)
- View all tour packages
- Filter active/inactive tours
- Search tours
- View booking statistics per tour

### 📈 Reports & Analytics (`/admin-panel/reports/`)
- Monthly comparison (current vs last month)
- Revenue analytics
- Top destinations by bookings
- Booking status distribution

## Admin vs User Interface

### Admin Panel Features:
- **URL Prefix:** `/admin-panel/`
- **Authentication:** Separate admin authentication (AdminUser model)
- **Design:** Matches user interface style with admin-specific colors
- **Navigation:** Easy access to all management features
- **Permissions:** Only AdminUser accounts can access

### User Interface:
- **URL:** Regular site URLs (/, /dashboard/, /bookings/)
- **Authentication:** Tourist/User authentication
- **Design:** Customer-facing design
- **Features:** Browse tours, make bookings, view own bookings

## Creating New Admin Accounts

### Option 1: Via Signup Page
1. Go to `http://127.0.0.1:8000/admin-panel/signup/`
2. Fill in the form:
   - Full Name
   - Email
   - Password
   - Confirm Password
3. Click "Create Admin Account"

### Option 2: Via Management Command
```bash
python manage.py create_admin
```

## Database Structure

### AdminUser Model
```python
class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Navigation Flow

```
Admin Login → Dashboard
                ↓
    ┌──────────┴───────────┐
    ↓           ↓          ↓
Bookings   Tourists    Tours    Reports
    ↓           ↓          ↓        ↓
  Details    Profile   Stats   Analytics
```

## Security Features

1. **Separate Authentication:** Admin and user accounts are completely separate
2. **Access Control:** Only AdminUser accounts can access admin panel
3. **Secure Login:** Password hashing via Django authentication
4. **Permission Checks:** Each admin view checks for admin privileges

## Common Adminoperations

### View a booking:
1. Go to Bookings List
2. Click "View" on any booking
3. See complete details including tourist info, tour details, payment status

### Cancel a booking:
1. Go to Bookings List or Booking Detail
2. Click "Cancel" button
3. Confirm cancellation
4. Booking status changes to "Cancelled"

### View tourist information:
1. Go to Tourists List
2. Click on a tourist
3. See profile and complete booking history

### Check analytics:
1. Go to Reports
2. View monthly comparisons
3. See top destinations
4. Check booking status distribution

## Testing the Admin Panel

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Access admin login:**
   Navigate to `http://127.0.0.1:8000/admin-panel/login/`

3. **Login with:**
   - Email: `admin@gmail.com`
   - Password: `admin123`

4. **Explore the dashboard:**
   - View statistics
   - Manage bookings
   - Check tourist information
   - View reports

## Customization

### Adding New Admin Features
All admin views are in `tour/admin_views.py`
All admin templates are in `tour/templates/tour/admin/`
All admin URLs are in `tour/urls.py` under the `# Admin URLs` section

### Styling
The admin panel uses the same CSS variables as the user interface:
- `--primary`: #1E6B9E
- `--success`: #27AE60
- `--danger`: #E74C3C
- `--warning`: #F39C12

## File Structure

```
tour/
├── admin_views.py          # All admin view logic
├── forms.py                # AdminLoginForm, AdminSignupForm
├── models.py               # AdminUser model
├── urls.py                 # Admin URL patterns
└── templates/
    └── tour/
        └── admin/
            ├── base.html              # Admin base template
            ├── dashboard.html         # Main dashboard
            ├── login.html             # Admin login
            ├── signup.html            # Admin signup
            ├── bookings_list.html     # All bookings
            ├── booking_detail.html    # Booking details
            ├── cancel_booking.html    # Cancel confirmation
            ├── tourists_list.html     # All tourists
            ├── tourist_detail.html    # Tourist profile
            ├── tours_list.html        # All tours
            └── reports.html           # Analytics
```

## Troubleshooting

### Cannot login to admin panel
- Make sure you're using `/admin-panel/login/` not `/admin/`
- Use email (not username) to login
- Default credentials: `admin@gmail.com` / `admin123`

### Admin dashboard shows empty data
- Create some bookings via the user interface first
- Add tour packages via Django admin or shell

### Permission denied errors
- Make sure you're logged in as an AdminUser
- Regular Tourist accounts cannot access admin panel

## Next Steps

You can now:
1. ✅ Login to the admin panel
2. ✅ View all bookings and manage them
3. ✅ See tourist information
4. ✅ Monitor tour performance
5. ✅ Generate reports and analytics
6. ✅ Create additional admin accounts

The admin panel is fully functional and ready to use! 🎉
