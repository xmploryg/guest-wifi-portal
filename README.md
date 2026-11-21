# FirstYearDown Guest WiFi Setup

Complete package for a themed guest network with FSU branding + baby photo.

## 📁 Files Created

```
/opt/data/guest-wifi/
├── index.html           # Landing page (deploy to Cloudflare Pages)
├── _redirects           # Cloudflare Pages routing
├── wifi-qr-print.png    # Print-ready 4×6" QR card @ 300 DPI
├── wifi-qr-web.png      # Web-optimized QR (400×400)
├── generate_qr.py       # QR generator script
├── setup_unifi.py       # UniFi configuration script
└── README.md            # This file
```

## 🎨 Landing Page Features

- **FSU colors**: Garnet (#CE1126) + Gold (#FFD700) + Dark Blue (#002147)
- **Dual logos**: FSU logo + baby photo placeholder (circular, gold borders)
- **Auto-detects internet**: Shows "You're Connected!" when online
- **Captive portal friendly**: Works with iOS/Android/macOS detection
- **External portal redirect**: `/connect` → UniFi guest login
- **Responsive**: Mobile-first, works on all devices

## 📱 QR Code

**WiFi Config**: `WIFI:T:WPA;S:FirstYearDown;P:FirstYearDown;;`

- **Print version**: `wifi-qr-print.png` — 4×6 inch, 300 DPI, ready for photo print
- **Web version**: `wifi-qr-web.png` — 400×400, for embedding in page

**To customize baby photo**: Replace the `.baby-photo .placeholder` div in `index.html` with:
```html
<img src="baby.jpg" alt="Baby" style="width:100%;height:100%;object-fit:cover;">
```
Add `baby.jpg` to the same folder before deploying.

---

## ☁️ Deploy to Cloudflare Pages

### Option A: Via Dashboard (Easiest)
1. Go to https://dash.cloudflare.com → Pages → Create a project
2. Connect GitHub repo (push this folder first) **OR** Direct Upload
3. **Build settings**:
   - Build command: (none / leave empty)
   - Build output directory: `/` (root)
   - Root directory: `/guest-wifi`
4. **Custom domain**: `portal.phoenixlab.me` (or your preferred subdomain)
5. Deploy!

### Option B: Via Wrangler CLI
```bash
cd /opt/data/guest-wifi
npm install -g wrangler
wrangler pages deploy . --project-name=firstyeardown --branch=main
# Then add custom domain in dashboard
```

### Required: HTTPS
Cloudflare Pages provides automatic HTTPS — **required** for captive portal detection on iOS/macOS.

---

## 🔧 UniFi Configuration

### Prerequisites
1. **VLAN 20** exists in UniFi → Settings → Networks → Create New Network
   - Name: "Guest"
   - VLAN ID: 20
   - Gateway: 192.168.20.1/24
   - DHCP: Enabled
   - **Block LAN access**: Enable (isolates guests)

### Run Setup Script
```bash
cd /opt/data/guest-wifi
# Edit setup_unifi.py with your credentials:
# - UDM_HOST, UDM_USER, UDM_PASS  OR  API_TOKEN
# - PORTAL_URL = "https://portal.phoenixlab.me"
python3 setup_unifi.py
```

### Manual Setup (Alternative)
1. UniFi Network App → Settings → WiFi → Create New WiFi
2. **Name**: `FirstYearDown`
3. **Security**: WPA2-PSK
4. **Password**: `FirstYearDown`
5. **VLAN**: 20 (Guest)
6. **Guest Policy**: Enable → **External Portal**
7. **Portal URL**: `https://portal.phoenixlab.me`
8. **HTTPS Redirection**: Enable
9. Save → Apply to APs

---

## 🖨️ Print the QR Card

**File**: `/opt/data/guest-wifi/wifi-qr-print.png`

- **Size**: 4×6 inch @ 300 DPI
- **Print on**: 4×6 photo paper (glossy/matte) or cardstock
- **Places to put**: Fridge, guest room, kitchen, entryway

**QR Code contains**: Network name + password — phones auto-join when scanned.

---

## ✅ Testing Checklist

| Test | Expected |
|------|----------|
| iPhone connects to "FirstYearDown" | Captive portal opens → shows landing page |
| Android connects | Notification → tap → opens landing page |
| macOS connects | Popup → opens landing page |
| Click "Connect to WiFi" | Redirects to UniFi auth → grants access |
| After auth, revisit page | Shows "You're Connected!" success state |
| QR code scan | Auto-joins network (no typing) |

---

## 🔗 Integration with Your Stack

| Component | Your Setup |
|-----------|------------|
| Domain | `phoenixlab.me` (Cloudflare) |
| Tunnel | Already configured for phoenixlab cluster |
| DNS | Add CNAME `portal` → `firstyeardown.pages.dev` |
| Access | Cloudflare Access not needed (public portal) |

---

## 🎯 Quick Start

```bash
# 1. Add baby photo
cp your-baby-photo.jpg /opt/data/guest-wifi/baby.jpg
# Edit index.html to use <img src="baby.jpg" ...>

# 2. Deploy to Cloudflare Pages
# (via dashboard or wrangler)

# 3. Configure UniFi
# Edit setup_unifi.py with credentials, then:
python3 /opt/data/guest-wifi/setup_unifi.py

# 4. Print QR card
# Send /opt/data/guest-wifi/wifi-qr-print.png to printer

# 5. Test with phone
```

---

## 📞 Need Help?

- **Landing page changes**: Edit `index.html` → redeploy
- **UniFi issues**: Check UDM Pro logs, ensure VLAN 20 exists
- **Portal not loading**: Verify HTTPS, check Cloudflare Pages build logs
- **QR not scanning**: Ensure print quality, test with multiple phones