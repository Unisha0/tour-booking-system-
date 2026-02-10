# 🚀 Quick Start Guide - Sajilo Yatra

## ⚡ Live Server
```
🌐 http://127.0.0.1:8001/
```

---

## 🗺️ Page Routes

| Page | URL | Login? |
|------|-----|--------|
| Home | `/` | ❌ No |
| Browse Tours | `/tours/` | ❌ No |
| About | `/about/` | ❌ No |
| Contact | `/contact/` | ❌ No |
| Dashboard | `/dashboard/` | ✅ Yes |
| Book Tour | `/book/1/` | ✅ Yes |
| Payment | `/payment/1/` | ✅ Yes |
| My Bookings | `/bookings/` | ✅ Yes |

---

## 👤 Test Account

**Phone Number:** `9841234567`  
**Password:** `password123`

Or sign up at: `/signup/`

---

## ✨ What to Try

### 1. As Guest (No Login)
- [ ] Go to home page `/`
- [ ] See hero video
- [ ] Browse tours at `/tours/`
- [ ] Try to book → See login modal
- [ ] Read about at `/about/`
- [ ] Check contact at `/contact/`
- [ ] Fill contact form

### 2. As User (After Signup/Login)
- [ ] Login with phone + password
- [ ] See dashboard with all 7 tours
- [ ] Search for tour by name
- [ ] Click tour details (modal)
- [ ] Book a tour
- [ ] Customize: days, persons, hotel
- [ ] Choose payment method
- [ ] Simulate payment (80% success)
- [ ] View confirmation
- [ ] Check My Bookings

---

## 🎨 Colors to Spot

- 🟠 **Orange:** Buttons, accents (#FF6B35)
- 🔵 **Blue:** Headers, nav (#004E89)
- 🟢 **Teal:** Highlights (#1B998B)
- ⚪ **White:** Background, text
- ⬛ **Dark:** Text, shadows

---

## 📱 Responsive Test

**On Desktop:**
- 3-column tour grid
- Full navigation
- Horizontal layout

**On Tablet (resize browser):**
- 2-column grid
- Still responsive
- Touch-friendly buttons

**On Mobile:**
- 1-column layout
- Stacked navigation
- Full-width buttons

---

## 🔍 Features to Check

✅ Smooth hover effects on cards  
✅ Search bar works (try "Everest")  
✅ Modal popups appear  
✅ Forms validate  
✅ Buttons have hover states  
✅ Gradients smooth  
✅ Navigation sticky at top  
✅ Login prompt on booking  
✅ Payment simulation works  
✅ Responsive layout shifts  

---

## 🐛 Troubleshooting

**Page shows error?**
```bash
cd /Users/U/Desktop/BOOKING/minorproject-sajiloyatra/booking
./venv/bin/python manage.py check
```

**Server down?**
```bash
./venv/bin/python manage.py runserver 8001
```

**Template not loading?**
```bash
./venv/bin/python manage.py collectstatic --noinput
```

---

## 📊 Database Test Data

**Hotels:** 36 across 7 destinations  
**Tours:** 7 major destinations  
**Add-ons:** Multiple (guides, permits, etc.)  
**Test User:** Phone number as username  

---

## 🎯 Success Criteria

✅ Home page loads with video  
✅ Can browse tours without login  
✅ Search bar filters tours  
✅ Login/signup working  
✅ Can book and pay  
✅ Mobile responsive  
✅ Buttons have animations  
✅ Payment simulation works  
✅ All colors visible  

---

## 📚 Documentation Files

- `FRONTEND_COMPLETE.md` - Full frontend guide
- `FRONTEND_DOCUMENTATION.md` - Design details
- `DESIGN_GUIDE.md` - Visual guide
- `GETTING_STARTED.md` - How to use
- `SYSTEM_STATUS.md` - Feature checklist
- `HOTELS_DATABASE.md` - Hotel info

---

## 🎉 Status

**✅ Server Running**  
**✅ All Pages Working**  
**✅ Responsive Design**  
**✅ Modern Theme Applied**  
**✅ Ready to Test**

---

Visit: **http://127.0.0.1:8001/**

Enjoy! 🏔️✈️
