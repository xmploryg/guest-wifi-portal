#!/usr/bin/env python3
"""
UniFi Guest Network Setup for "Go Noles"
Run this from a machine with access to UDM Pro (192.168.1.1)
Uses legacy UniFi API (working endpoints discovered)
"""

import json
import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== CONFIG ==========
UDM_HOST = "192.168.1.1"           # UDM Pro IP
SITE = "default"                   # Usually "default"
SSID_NAME = "Go Noles"
SSID_PASSWORD = "FirstYearDown"
VLAN_ID = 20                       # Guest VLAN (must exist in UniFi)
PORTAL_URL = "https://portal.phoenixlab.me"  # Your Cloudflare Pages URL

# Read API token from environment (set in .env)
API_TOKEN = os.environ.get("UNIFI_API_TOKEN", "")

# ========== AUTH ==========
session = requests.Session()
session.verify = False

def login():
    """Authenticate with UDM Pro using API token"""
    if not API_TOKEN:
        print("❌ UNIFI_API_TOKEN not set in environment")
        return False
    
    session.headers.update({"X-API-KEY": API_TOKEN})
    print("✅ Using API token from environment")
    return True

def get_existing_wlan():
    """Check if WLAN already exists using legacy API"""
    url = f"https://{UDM_HOST}/proxy/network/api/s/{SITE}/list/wlanconf"
    resp = session.get(url)
    if resp.status_code == 200:
        for wlan in resp.json().get("data", []):
            if wlan.get("name") == SSID_NAME:
                return wlan
    return None

def create_guest_wlan():
    """Create the guest WLAN using legacy API"""
    url = f"https://{UDM_HOST}/proxy/network/api/s/{SITE}/rest/wlanconf"
    
    payload = {
        "name": SSID_NAME,
        "enabled": True,
        "security": "wpapsk",
        "wpapsk": SSID_PASSWORD,
        "wpapsk_type": "wpa2",
        "vlan": VLAN_ID,
        "is_guest": True,
        "guest_portal_enabled": True,
        "guest_portal_type": "external",
        "guest_portal_url": PORTAL_URL,
        "guest_portal_https_redirection": True,
        "hide_ssid": False,
        "band": "all",  # 2.4 + 5 GHz
        "channel": "auto",
        "tx_power": "auto",
        "min_rssi": -85,
        "multicast_enhance_enabled": True,
        "uapsd_enabled": False,
        "group_rekey_interval": 3600,
        "radius_enabled": False,
    }
    
    resp = session.post(url, json=payload)
    if resp.status_code in (200, 201):
        print(f"✅ Created WLAN '{SSID_NAME}' on VLAN {VLAN_ID}")
        print(f"   Password: {SSID_PASSWORD}")
        print(f"   External Portal: {PORTAL_URL}")
        return resp.json()
    print(f"❌ Failed to create WLAN: {resp.status_code} {resp.text}")
    return None

def update_guest_portal(wlan_id):
    """Update existing WLAN to use external portal using legacy API"""
    url = f"https://{UDM_HOST}/proxy/network/api/s/{SITE}/rest/wlanconf/{wlan_id}"
    payload = {
        "guest_portal_enabled": True,
        "guest_portal_type": "external",
        "guest_portal_url": PORTAL_URL,
        "guest_portal_https_redirection": True,
    }
    resp = session.put(url, json=payload)
    if resp.status_code == 200:
        print(f"✅ Updated WLAN to use external portal: {PORTAL_URL}")
        return True
    print(f"❌ Failed to update portal: {resp.status_code} {resp.text}")
    return False

def main():
    print("=" * 50)
    print("UniFi Guest Network Setup: Go Noles")
    print("=" * 50)
    
    if not login():
        return
    
    # Check existing
    existing = get_existing_wlan()
    if existing:
        print(f"ℹ️  WLAN '{SSID_NAME}' already exists (ID: {existing['_id']})")
        update_guest_portal(existing['_id'])
    else:
        create_guest_wlan()
    
    print("\n📋 Next Steps:")
    print("1. Ensure VLAN 20 exists in UniFi → Settings → Networks")
    print("2. Assign VLAN 20 to the guest SSID in WiFi settings")
    print("3. Deploy Cloudflare Pages from /opt/data/guest-wifi")
    print("4. Update PORTAL_URL in this script if domain differs")
    print("5. Test: Connect to 'Go Noles' / 'FirstYearDown'")

if __name__ == "__main__":
    main()