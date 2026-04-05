# 🔒 ONE BOOKING AT A TIME POLICY

## Overview
The system now enforces a **strict one-booking-at-a-time policy** to prevent users from making multiple simultaneous bookings.

## ✅ What's Been Implemented

### 1. **Database Cleanup**
- Created management command to clean duplicate users
- Removed 13 orphaned user accounts without tourist profiles
- Database is now clean and optimized

### 2. **Validation Rules**

#### Frontend Validation:
- Dashboard shows warning banner if user has active booking
- "Book Now" buttons are **disabled** for users with active bookings
- Clear messaging: "🔒 Booking Locked"
- Link to view current booking directly from warning banner

#### Backend Validation (Views):
- `book_tour` view checks for active bookings before allowing new bookings
- Redirects to "My Bookings" page with warning message
- Prevents direct URL access attempts

#### API Validation:
- `create_booking` API endpoint validates active bookings
- Returns HTTP 400 error with details about existing booking
- Includes existing booking ID and tour name in error response

### 3. **Model Methods**
Added helper methods to `Tourist` model:
```python
def has_active_booking(self):
    """Check if tourist has any active (pending or confirmed) booking"""
    return self.booking_set.filter(status__in=['pending', 'confirmed']).exists()

def get_active_booking(self):
    """Get the active booking if exists"""
    return self.booking_set.filter(status__in=['pending', 'confirmed']).first()
```

## 📋 Active Booking Definition

A booking is considered **"active"** if its status is:
- ✅ **Pending** (awaiting payment)
- ✅ **Confirmed** (payment completed)

A booking is **NOT active** if:
- ❌ **Cancelled**

## 🎯 User Flow

### Scenario 1: User WITHOUT Active Booking
1. User logs in
2. Views dashboard with all tours
3. Clicks "Book Now" on any tour
4. Proceeds to booking form
5. Completes booking and payment
6. Now has 1 active booking

### Scenario 2: User WITH Active Booking
1. User logs in
2. Dashboard shows **warning banner**:
   ```
   ⚠️ ACTIVE BOOKING: You have an active booking for [Tour Name]. 
   Please complete or cancel it before making a new booking. View Booking →
   ```
3. All "Book Now" buttons show "🔒 Booking Locked" (disabled)
4. If user tries to access booking URL directly:
   - Redirected to "My Bookings" page
   - Warning message displayed

### Scenario 3: Completing Current Booking
1. User views "My Bookings"
2. Either:
   - Completes payment for pending booking → Status becomes "Confirmed"
   - Cancels booking → Status becomes "Cancelled"
3. Once cancelled or completed, can make new booking

## 🔧 Management Commands

### Clean Up Duplicate Users
```bash
python manage.py cleanup_users
```

**What it does:**
- Finds duplicate tourists by phone number
- Finds duplicate tourists by email
- Transfers bookings from duplicates to main account
- Deletes duplicate tourist profiles
- Removes orphaned user accounts (users without tourist profile)
- Provides detailed summary of cleanup

**Example Output:**
```
🔍 Scanning for duplicate users...

👻 Found 13 orphaned user(s) without tourist profile
   ❌ Deleting orphaned user: username1
   ❌ Deleting orphaned user: username2
   ...

==================================================
✅ Cleanup complete!
   Deleted 0 duplicate tourist(s)
   Deleted 13 user account(s)

📊 Current database state:
   Total Tourists: 12
   Total Users: 13
```

## 🛡️ Security & Validation Layers

### Layer 1: Frontend (UI)
- Visual indicators (disabled buttons)
- Warning banners
- Prevents accidental attempts

### Layer 2: Backend Views
- Python validation in views
- Checks before form processing
- User-friendly error messages

### Layer 3: API
- REST API validation
- Structured error responses
- Client-side app support

## 📱 API Response Examples

### Success (No Active Booking):
```json
{
  "id": 123,
  "tourist": {...},
  "tour": {...},
  "status": "pending",
  ...
}
```

### Error (Has Active Booking):
```json
{
  "error": "You already have an active booking. Please complete or cancel it before making a new booking.",
  "existing_booking_id": 122,
  "existing_tour": "Pokhara Tour Package"
}
```

## 🎨 UI/UX Features

### Warning Banner (Dashboard):
- **Background:** Yellow warning color (#FFF3CD)
- **Border:** Orange left border (#F39C12)
- **Icon:** ⚠️
- **Message:** Clear explanation with link to bookings
- **Action:** Direct link to "My Bookings" page

### Disabled Button:
- **Background:** Gray (#E0E0E0)
- **Text Color:** Dark gray (#757575)
- **Cursor:** not-allowed
- **Icon:** 🔒
- **Text:** "Booking Locked"
- **Tooltip:** "You already have an active booking"

## 🧪 Testing the Feature

### Test Case 1: First Booking
1. Login as new user
2. Should see all "Book Now" buttons enabled
3. Book a tour successfully
4. Verify booking is pending/confirmed

### Test Case 2: Second Booking Attempt
1. Login as user with active booking
2. Should see warning banner at top
3. All "Book Now" buttons should be disabled
4. Try accessing `/book/<tour_id>/` directly
5. Should redirect to My Bookings with warning message

### Test Case 3: After Cancellation
1. Go to My Bookings
2. Cancel the active booking
3. Return to dashboard
4. Warning banner should disappear
5. "Book Now" buttons should be enabled again

### Test Case 4: API Request
```bash
# Should fail if user has active booking
curl -X POST http://localhost:8000/api/bookings/create/ \
  -H "Authorization: Token <user-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tour": 1,
    "days": 3,
    "persons": 2
  }'
```

## 📂 Files Modified

### Backend:
- `tour/models.py` - Added helper methods to Tourist model
- `tour/views.py` - Added validation in book_tour view
- `tour/api_views.py` - Added validation in create_booking API
- `tour/management/commands/cleanup_users.py` - New cleanup command

### Frontend:
- `tour/templates/tour/dashboard.html` - Warning banner + disabled buttons

## 🚀 Benefits

1. **Prevents Overbooking:** Users can't accidentally book multiple tours
2. **Better UX:** Clear messaging about current booking status
3. **Data Integrity:** Clean database without duplicates
4. **Simplified Management:** One active booking easier to track
5. **Payment Flow:** Ensures payment completion before new bookings
6. **Admin Clarity:** Easier to manage one booking per user

## 💡 Future Enhancements

Potential improvements for future versions:
- Allow multiple bookings for different dates
- Queue system for future bookings
- Booking history with rebooking option
- Admin override for special cases
- Booking expiration after X hours of pending status

## 🆘 Troubleshooting

### Issue: Can't make any bookings
**Solution:** Check if you have an active booking. Go to "My Bookings" and complete or cancel it.

### Issue: Button still disabled after cancellation
**Solution:** Refresh the page. The dashboard checks booking status on page load.

### Issue: Duplicate users still exist
**Solution:** Run `python manage.py cleanup_users` to clean the database.

---

**Implementation Date:** April 5, 2026  
**Status:** ✅ Fully Implemented & Tested
