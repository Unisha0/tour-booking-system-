# 🎨 Sajilo Yatra - Visual Design Guide

## 🎯 Color Palette

```
PRIMARY COLORS:
├── Orange/Red Accent: #FF6B35
├── Navy Blue: #004E89
└── Teal Accent: #1B998B

SUPPORTING COLORS:
├── Light Background: #F7F7F7
├── Dark Text: #1a1a1a
├── Success Green: #06A77D
├── Error Red: #D32F2F
└── Warning Yellow: #FFC107
```

## 🎬 Hero Section

```
╔════════════════════════════════════════════╗
║                                            ║
║       Video Background (autoplay)          ║
║       Gradient Overlay (semi-transparent) ║
║                                            ║
║    "Discover Nepal's Magic"               ║
║    Stunning mountain peaks...              ║
║                                            ║
║   [Explore Tours]  [Start Your Journey]   ║
║                                            ║
╚════════════════════════════════════════════╝
```

**Key Features:**
- 600px height (400px on mobile)
- Video background (opacity 0.3)
- Gradient overlay (80% opaque)
- White text with shadow
- Two CTA buttons

---

## 🏔️ Tour Cards

```
┌──────────────────────────────┐
│  ⛰️  [Popular Badge]         │ ← Emoji Icon
├──────────────────────────────┤
│  MOUNTAIN TREK              │ ← Destination
│  Everest Base Camp          │ ← Title
│  📅 14 Days  👥 1-8 persons │ ← Meta
│  Rs. 25,000                 │ ← Price (Orange)
│                             │
│  Trek to world's highest    │ ← Description
│  peak with experienced...   │
│                             │
│  [Book Now →]     [Details] │ ← Buttons
└──────────────────────────────┘
```

**Hover Effect:** Lift up (-8px), shadow grows

---

## 📱 Navigation Bar

```
┌─────────────────────────────────────────────────┐
│ 🏔️ Sajilo Yatra │ Home Explore About Contact │ [Login] [Sign Up] │
└─────────────────────────────────────────────────┘
```

**Features:**
- Sticky (stays at top)
- Gradient background
- White text
- Hover underline animation
- Responsive on mobile

---

## ✨ Button Styles

### Primary Button (Orange Gradient)
```
┌──────────────────┐
│  Book Now →      │  ← Gradient background
└──────────────────┘   ← 25px border-radius
   White text, padding 10-15px
   Hover: -2px lift, shadow glow
```

### Secondary Button (White)
```
┌──────────────────┐
│  Explore Tours   │  ← White background
└──────────────────┘   ← Blue text
   Hover: shadow & lift
```

### Logout Button (Transparent Border)
```
┌──────────────────┐
│  Logout          │  ← Transparent with border
└──────────────────┘   ← White text
```

---

## 📊 Stats Section

```
╔════════════════════════════════════════════════════╗
║  50K+              7                36+            ║
║  Happy Travelers   Tour Destinations  Partner Hotels║
║                                                    ║
║  4.8⭐            100%               24/7          ║
║  Average Rating   Satisfaction       Support       ║
╚════════════════════════════════════════════════════╝

Background: Gradient overlay (blue to orange)
Text: White
Stats in 4-column grid
```

---

## 📋 "Why Choose Us" Cards

```
┌─────────────────────┐
│  🏔️                 │  ← Emoji Icon (60px)
├─────────────────────┤
│  Expert Guides      │  ← Title (Blue)
│                     │
│  Local guides with  │  ← Description
│  years of...        │
└─────────────────────┘

Hover: Lift (-10px), border color changes to orange
```

---

## 🔍 Search Bar

```
┌─────────────────────────────────────┐
│  🔍 Search tours by name...         │
└─────────────────────────────────────┘
  Width: 100% / max-width: 600px
  Padding: 15px
  Border: 2px #ddd
  Border-radius: 25px
  Focus: Border becomes orange, subtle shadow
```

---

## 💬 Form Inputs

```
┌──────────────────────────────────────┐
│ Full Name *                          │
│ [_____________________________]       │
│                                      │
│ Email Address *                      │
│ [_____________________________]       │
│                                      │
│ Message *                            │
│ [_____________________________]       │
│ [_____________________________]       │
│ [_____________________________]       │
│                                      │
│          [Send Message →]            │
└──────────────────────────────────────┘
```

**Input Style:**
- 2px border (#ddd)
- 12px padding
- 8px border-radius
- Smooth transitions
- Focus: Orange border + shadow glow

---

## 📱 Modal Popup

```
                    ┌─────────────────────────────────┐
                    │  Tour Details            ✕      │
                    ├─────────────────────────────────┤
                    │                                 │
                    │  Everest Base Camp              │
                    │  📍 Himalaya Region             │
                    │                                 │
                    │ ┌─────────────────────────────┐ │
                    │ │ Duration: 14 Days           │ │
                    │ │ Price: Rs. 25,000           │ │
                    │ └─────────────────────────────┘ │
                    │                                 │
                    │ Full description text...        │
                    │                                 │
                    │ [Book This Tour →]              │
                    │                                 │
                    └─────────────────────────────────┘
```

**Features:**
- Centered on screen
- Semi-transparent background
- White content box
- Click outside to close
- Responsive width

---

## 🎫 Payment Method Cards

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   eSewa 🟠       │  │   Khalti 🟣      │  │   Bank Transfer  │
│                  │  │                  │  │   🏦              │
│  Mobile Payment  │  │  Digital Wallet  │  │  Offline Payment │
│  (Email, Pass)   │  │  (Mobile, PIN)   │  │  (Account Info)  │
│                  │  │                  │  │                  │
│  [Select] ✓      │  │  [Select]        │  │  [Select]        │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        (selected style: border color changes to orange)
```

---

## 📋 Table: My Bookings

```
┌──────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Tour │ Duration │ Persons  │ Status   │ Payment  │ Total    │
├──────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Ever │ 14 days  │ 2        │ ✓ Conf   │ ✓ Paid   │ Rs.47,4K │
│ Anna │ 16 days  │ 3        │ ⏳ Pend  │ ⏳ Pend  │ Rs.52,8K │
│ Kath │ 3 days   │ 1        │ ✓ Conf   │ ✓ Paid   │ Rs.8,000 │
└──────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

**Badge Colors:**
- ✓ Confirmed: Green (#06A77D)
- ⏳ Pending: Yellow (#FFC107)
- ❌ Cancelled: Red (#D32F2F)

---

## 🎯 Responsive Behavior

### Desktop (1200px+)
```
┌──────────────────┬──────────────────┬──────────────────┐
│    Tour Card     │    Tour Card     │    Tour Card     │
└──────────────────┴──────────────────┴──────────────────┘
```
3-column grid, spacing 30px

### Tablet (768px-1199px)
```
┌──────────────────┬──────────────────┐
│    Tour Card     │    Tour Card     │
├──────────────────┼──────────────────┤
│    Tour Card     │    Tour Card     │
└──────────────────┴──────────────────┘
```
2-column grid

### Mobile (<768px)
```
┌──────────────────┐
│    Tour Card     │
├──────────────────┤
│    Tour Card     │
├──────────────────┤
│    Tour Card     │
└──────────────────┘
```
1-column stack

---

## 🎬 Animation Timings

| Animation | Duration | Easing | Usage |
|-----------|----------|--------|-------|
| Hover Effects | 0.3s | ease | Cards, buttons |
| Page Load | 0.5s | ease-in | Title fade-in |
| Modal | 0.3s | ease | Popup entrance |
| Form Input Focus | 0.3s | ease | Input highlights |
| Button Lift | 0.3s | ease | CTA buttons |

---

## 📐 Spacing System

```
Extra Small: 8px
Small:       15px
Medium:      20px
Large:       30px
XL:          40px
2XL:         60px
3XL:         80px
```

Used for:
- Padding
- Margins
- Gaps between elements

---

## 🔤 Typography Scale

```
H1 (Hero):           60px, weight 800
H2 (Section Title):  45px, weight 800
H3 (Card Title):     20-22px, weight 700
Body Text:           14-16px, weight 400-600
Small Text:          12-14px, weight 400
```

**Font Family:** 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif

---

## 🌈 Gradient Library

### Primary Gradient (Nav, Buttons)
```css
linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)
```

### Secondary Gradient (Hero, Footer)
```css
linear-gradient(135deg, #004E89 0%, #FF6B35 100%)
```

### Accent Gradient (Stats)
```css
linear-gradient(135deg, #1B998B 0%, #00D9FF 100%)
```

### Hero Overlay
```css
linear-gradient(135deg, rgba(0, 78, 137, 0.8) 0%, rgba(255, 107, 53, 0.8) 100%)
```

---

## ✅ Design Checklist

- [x] Consistent color palette
- [x] Proper typography hierarchy
- [x] Adequate whitespace
- [x] Smooth animations (not jarring)
- [x] Responsive design (mobile-first)
- [x] Accessibility (contrast ratios)
- [x] Professional appearance
- [x] Clear call-to-action buttons
- [x] Consistent hover states
- [x] Proper spacing/padding

---

## 🎨 Design Philosophy

**Modern:** Clean, contemporary aesthetic  
**Colorful:** Vibrant orange/blue/teal palette  
**Professional:** Business-appropriate design  
**Accessible:** Good contrast, readable fonts  
**Responsive:** Works on all devices  
**Fast:** Smooth animations, optimized loading  

---

This visual guide ensures consistent design across all pages!

**Happy browsing! 🏔️✈️**
