# Sajilo Yatra - Tour Booking System with Payment Integration

A complete Django-based tour booking platform with integrated payment system supporting demo payment gateways (eSewa, Khalti, and Bank Transfer).

## 🚀 Features

### Core Features
- **User Authentication**: Sign up, login, and profile management
- **Tour Browsing**: View available tours with detailed information
- **Booking System**: Book tours with customizable options (days, persons, hotel, add-ons)
- **Payment Integration**: 
  - eSewa Payment Simulation
  - Khalti Payment Simulation
  - Bank Transfer Details
  - Realistic processing animation
- **Booking Management**: Track all your bookings with payment status
- **Admin Dashboard**: Manage tours, bookings, and payments

### Payment Features
- Step-by-step payment process
- Realistic payment form simulation
- Progress indicators
- Real-time processing animation
- Automatic payment success/failure simulation (80% success rate)
- Payment status tracking

## 📋 System Requirements

- Python 3.14+
- Django 6.0.2
- SQLite3 (default)
- Django REST Framework
- django-allauth
- Pillow (for image handling)
- python-dotenv

## 🔧 Installation

### 1. Navigate to Project Directory
```bash
cd /Users/U/Desktop/BOOKING/minorproject-sajiloyatra/booking
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver 8001
```

Server will be available at: **http://127.0.0.1:8001/**

## 📁 Project Structure

```
booking/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── booking/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── tour/
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── api_views.py         # REST API endpoints
│   ├── auth_views.py        # Authentication API
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin configuration
│   ├── migrations/          # Database migrations
│   ├── templates/tour/      # HTML templates
│   └── static/tour/         # CSS, JS, images
├── media/                   # Uploaded files
└── venv/                    # Virtual environment
```

## 🔐 User Authentication

### Sign Up
- **URL**: `/signup/`
- Create account with name, email, and phone number
- Phone number used as username

### Login
- **URL**: `/login/`
- Login with phone number or email
- Automatic redirect to profile completion if needed

### API Authentication
```bash
# Get Token
POST /api/login/
{
  "email": "user@example.com",
  "password": "password123"
}

# Response
{
  "token": "abc123xyz...",
  "user_id": 1,
  "email": "user@example.com",
  "username": "tourist1"
}

# Use token in requests
curl -H "Authorization: Token abc123xyz..." \
  http://127.0.0.1:8001/api/bookings/
```

## 🎫 Booking Flow

### Step 1: Browse Tours
- **URL**: `/dashboard/`
- View all available tours with images and details
- See base price and duration

### Step 2: Book a Tour
- **URL**: `/book/<tour_id>/`
- Select number of days and persons
- Choose optional hotel and add-ons
- Click "Book" → Redirected to payment gateway

### Step 3: Select Payment Method
- **URL**: `/payment/<booking_id>/`
- Choose payment method:
  - eSewa
  - Khalti
  - Bank Transfer
- Review booking summary
- Click "Proceed to Payment"

### Step 4: Complete Payment
- **URL**: `/payment/<booking_id>/process/`
- Realistic payment form based on chosen method
- Enter payment details (demo mode)
- System processes payment (3-5 seconds)
- Auto success/failure (80% success rate)

### Step 5: Confirm Booking
- If payment successful → Booking confirmed
- View booking in "My Bookings"
- If payment failed → Return to payment gateway to retry

## 💳 Payment Methods

### eSewa
- Email-based account
- Shows eSewa branded card
- Simulates eSewa login process

### Khalti
- Mobile number based
- Shows Khalti branded card
- Simulates PIN verification

### Bank Transfer
- Shows bank details
- Reference ID entry
- Manual payment confirmation

## 📊 Admin Dashboard

### Access
- **URL**: `/admin/`
- Username: Your superuser username
- Password: Your superuser password

### Manage
- **Tours**: Add, edit, delete tour packages
- **Bookings**: View all bookings and their status
- **Payments**: Track payment transactions
- **Hotels**: Manage available hotels
- **Add-ons**: Manage tour add-ons (hiking, city tour, etc.)
- **Tourists**: Manage user profiles

## 🔌 API Endpoints

### Authentication
- `POST /api/login/` - Get auth token
- `POST /api/logout/` - Revoke token

### Tours
- `GET /api/tours/` - List all active tours

### Bookings
- `POST /api/bookings/create/` - Create new booking
- `GET /api/bookings/` - Get user's bookings
- `GET /api/bookings/<id>/` - Get booking details

### Payments
- `POST /api/bookings/<id>/initiate-payment/` - Start payment
- `POST /api/bookings/<id>/process-payment/` - Process payment

## 🗄️ Database Models

### Tourist
- User profile extension
- Phone, DOB, email
- Created/updated timestamps

### Tour
- Tour package details
- Price, destination, duration
- Active/inactive status
- Get price dynamically based on persons

### Booking
- Links tourist and tour
- Booking status (pending/confirmed/cancelled)
- Hotel and add-ons selection
- Computed total price with discounts

### Payment
- Links to booking
- Payment method (eSewa/Khalti/Offline)
- Payment status (pending/completed/failed)
- Transaction ID tracking

### Hotel
- Hotel name and daily rate

### Addon
- Optional add-ons (hiking, city tour, etc.)
- Fixed prices

## 💰 Price Calculation

```python
Total Price = (Base Price × Days × Persons × Discount) 
              + (Hotel Price × Days) 
              + Sum(Add-on Prices)

Discounts:
- 1 person: No discount
- 2 persons: 1.8x multiplier
- 3+ persons: 0.85x multiplier

Duration Discounts:
- 2 days: 10% off
- 3+ days: 15% off
```

## ⚙️ Settings Configuration

### Important Settings in `booking/settings.py`

```python
# Debug mode (set to False in production)
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8001',
    'http://localhost:8001',
]
```

## 📝 Environment Variables

Create `.env` file in `booking/` directory:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## 🧪 Testing the Payment System

1. **Create an account**
   - Go to `/signup/`
   - Fill in details (use test phone number)

2. **Login**
   - Use your phone number and password

3. **Book a tour**
   - Go to `/dashboard/`
   - Click on any tour
   - Fill booking details
   - Click "Book"

4. **Process payment**
   - Select payment method
   - Enter demo credentials (any values work)
   - Payment automatically processes
   - System simulates success/failure

5. **View bookings**
   - Go to `/bookings/`
   - See booking and payment status
   - Retry payment if failed

## 🐛 Troubleshooting

### CSRF Token Error
- Ensure `{% csrf_token %}` is in POST forms
- Check CSRF_TRUSTED_ORIGINS in settings

### Template Not Found
- Verify template file exists in correct directory
- Check `TEMPLATES` setting in settings.py

### Payment Gateway Errors
- Ensure Payment model is created (run migrations)
- Check database has payment entries

### Import Errors
- Install all requirements: `pip install -r requirements.txt`
- Ensure virtual environment is activated

## 📈 Future Enhancements

- [ ] Real eSewa integration
- [ ] Real Khalti integration
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Invoice generation
- [ ] Itinerary management
- [ ] Reviews and ratings
- [ ] Travel insurance options
- [ ] Group booking discounts
- [ ] Multi-language support

## 📞 Support

For issues or questions, check:
1. Django logs in terminal
2. Database entries in admin panel
3. Browser console for JavaScript errors
4. Network tab for API requests

## 📄 License

This project is for educational purposes.

---

**Happy Booking! 🎫✈️🏔️**
