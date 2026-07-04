# Blinkit API Documentation

> Discovered via HTTP Toolkit traffic capture on 2026-07-04.

## Package Name
`com.grofers.customerapp` (version 18.7.0, build 80180070)

## Base URL
`https://api2.grofers.com`

## CDN
`https://cdn.grofers.com`

## Architecture
**Server-driven UI (SDUI)**: Most endpoints return full layout instructions (widgets, styling,
actions) rather than raw data. Product information is embedded inside widget tracking metadata
and cart action payloads. Our adapter must parse these nested structures.

---

## Required Headers

Every authenticated request needs these headers:

```
auth_key: 45bff2b1437ff764d5e5b9b292f9771428e18fc40b7f3b7303d196ea84ab4341
app_client: consumer_android
app_version: 80180070
version_code: 80180070
version_name: 18.7.0
host_app: blinkit
access_token: <from verify OTP response>
session_uuid: <uuid4, generated per session>
device_id: <device identifier>
lat: <latitude>
lon: <longitude>
accept: application/json
content-type: application/json; charset=UTF-8
user-agent: com.grofers.customerapp/280180070 (Linux; U; Android 16; en_US; <device>; Build/<build>; Cronet/149.0.7827.102)
```

### Optional/Diagnostic Headers
```
screen_density: 1080px
screen_density_num: 2.8125
cpu-level: AVERAGE
memory-level: EXCELLENT
storage-level: EXCELLENT
network-level: AVERAGE
battery-level: HIGH
rn_bundle_version: 1009002001
app_api_version: 36
x-app-theme: default
x-app-appearance: LIGHT
```

### Notes
- `auth_key` appears to be a static app-level key (not per-user)
- `access_token` format: `v2::<uuid>` (e.g. `v2::2720178c-7553-48bc-a71b-34cdc42326d5`)
- Location is sent as lat/lon headers on every request, plus `cur_lat`/`cur_lon` for GPS position
- `session_uuid` is a random UUID4 generated per app session

---

## Authentication

### 1. Request OTP

```
POST /v2/accounts/
Content-Type: application/x-www-form-urlencoded
```

**Request Body** (form-encoded, NOT JSON):
```
country_code=91&otp_mode=SMS&user_phone=9560494827&build_variant=release
```

| Field | Type | Description |
|-------|------|-------------|
| country_code | int | Country dial code (91 for India) |
| otp_mode | string | `SMS` or potentially `WHATSAPP` |
| user_phone | string | 10-digit phone number |
| build_variant | string | Always `release` |

**Response** (200):
```json
{
  "login": true,
  "action": "login",
  "sms_sent": true,
  "message_id": "<uuid>",
  "success": true,
  "message": "We have sent a verification code to you via SMS"
}
```

### 2. Verify OTP

```
POST /v2/accounts/verify/phone/code/
Content-Type: application/x-www-form-urlencoded
```

**Request Body** (form-encoded):
```
country_code=91&otp_mode=SMS&user_phone=9560494827&adv_id=-NA-&verify_code=5542&notification_permission_enabled=false
```

| Field | Type | Description |
|-------|------|-------------|
| country_code | int | Same as request OTP |
| otp_mode | string | Same as request OTP |
| user_phone | string | Same phone number |
| adv_id | string | Advertising ID (`-NA-` if unavailable) |
| verify_code | string | OTP digits |
| notification_permission_enabled | bool | Push notification permission status |

**Response** (200):
```json
{
  "access_token": "v2::2720178c-7553-48bc-a71b-34cdc42326d5",
  "message": "Login Successful",
  "success": true,
  "user": {
    "date_now": 1783171641,
    "id": 67150010,
    "phone": "9560494827",
    "verified": true
  }
}
```

The `access_token` is used in the `access_token` header for all subsequent requests.

---

## Search

### Auto Suggest (Type-ahead)

```
POST /v1/actions/auto_suggest
Content-Type: application/json
```

**Request Body**:
```json
{
  "q": "milk",
  "search_string": "milk",
  "search_type": "type_to_search"
}
```

**Response**: SDUI layout with suggestion snippets. Each suggestion contains:
- `title.text`: Display text with markdown formatting (e.g. `<medium-400|{color.text.grey|Milk}>`)
- `click_action.update_search_api_params.api_params`: The actual search call to make
- `entity_type`: `keyterm`, `composite_keyword`, etc.
- `entity_name`: Clean suggestion text (e.g. "milk", "cow milk", "full cream milk")
- `image.url`: Suggestion thumbnail

### Search Products

```
POST /v1/layout/search?q=milk&search_type=type_to_search&should_send_session_context=true
Content-Type: application/json
```

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| q | string | Search query |
| search_type | string | `type_to_search` (live), `auto_suggest` (from suggestion tap) |
| should_send_session_context | bool | Include session tracking |

**Request Body**:
```json
{
  "search_string": "milk",
  "search_type": "type_to_search"
}
```

**Response**: Large SDUI response (~500KB) containing:

1. **Filter pills** (`pill_container_snippet`) — Quantity, Brand, Fat Profile, Milk Source, Price, etc.
2. **Product cards** (`product_card_type_unbounded_v3`) — The actual search results

#### Extracting Product Data

Product data lives in **two places** per product card:

**A. `tracking.widget_meta`** (analytics/tracking payload — has ALL clean data):
```json
{
  "product_id": 176,
  "name": "Amul Taaza Homogenised Toned Milk",
  "brand": "Amul",
  "price": 77,
  "mrp": 77,
  "currency": "INR",
  "primary_unit_of_measure": "1 ltr",
  "secondary_unit_of_measure": "",
  "rating": 4.72,
  "inventory": 20,
  "inventory_limit": 20,
  "state": "available",
  "merchant_id": 31661,
  "merchant_type": "express",
  "eta_identifier": "express",
  "ptype": "Milk",
  "product_position": "10",
  "widget_name": "Product",
  "widget_type": "product_card_type_unbounded_v3",
  "promo_identifers": [
    "OFFER_TYPE_PROMO_25209695",
    "OFFER_TYPE_PROMO_25209559",
    "OFFER_TYPE_PROMO_25209288"
  ]
}
```

**B. `cta_data.stepper.increment_actions.default[0].add_to_cart.cart_item`** (cart payload):
```json
{
  "product_id": 522807,
  "merchant_id": 31661,
  "product_name": "Amul Buffalo A2 Milk",
  "quantity": 1,
  "unavailable_quantity": 0,
  "price": 40,
  "mrp": 40,
  "unit": "500 ml",
  "inventory": 1,
  "image_url": "https://cdn.grofers.com/da/cms-assets/cms/product/<uuid>.png",
  "group_id": 2057146,
  "merchant_type": "express",
  "eta_identifier": "express",
  "brand": "",
  "product_full_name": "Amul Buffalo A2 Milk",
  "display_name": "Amul Buffalo A2 Milk"
}
```

**C. Additional display fields** on the product card widget:
- `accessibility_info.text`: Human-readable summary (e.g. "Country Delight 25 g High Protein Chocolate Milk is available for ₹119")
- `display_name.text`: Product name
- `pricing_info.price.text`: Display price (e.g. "₹40")
- `media_container.items[].image.url`: Product images
- `product_state`: `"available"` or absent
- `identity.id`: Product ID as string

#### Adapter Strategy
For our adapter, parse `tracking.widget_meta` from each `product_card_type_unbounded_v3` widget.
It has the cleanest data: product_id, name, brand, price, mrp, unit, rating, inventory, state.

---

## Product Detail

```
POST /v1/layout/product/{product_id}?identity={product_id}&merchant_id={merchant_id}&...
```

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| identity | int | Product ID |
| merchant_id | int | Merchant/store ID |
| product_id | int | Same as identity |
| product_index | int | Position in search results |
| npr_flag | string | `PRODUCT_RECOMMENDATION` |
| previous_page | string | `search` |
| should_send_cart_items_data | bool | Include cart state |

**Response**: Full PDP layout (~219KB SDUI). Contains:
- Image carousel with all product photos
- Key highlights (shelf life, biological source, processing type)
- Pricing info
- Variant selector (compressed/encoded)
- Related products

---

## Other Endpoints

### Ping (Health Check)
```
GET /api/v1/ping
```
Returns 200 if API is alive.

### App Config
```
GET /api/v1/config/primary?consumer_app_android_version=80180070&fetch_nearest_addresses=true&prev_lat=28.477&prev_lon=77.502
```
Returns store configuration, nearest addresses, delivery slot info.

### Login Config
```
POST /v1/login/config
```
Returns OTP configuration per country (SMS/WhatsApp availability).

### Feed (Home Page)
```
POST /v1/layout/feed
POST /v1/layout/feed?fetch_config_state=APP_LAUNCH_WITH_GPS_SUCCESS
```
Home page SDUI layout with banners, categories, deals.

### Empty Search (Search Page Landing)
```
POST /v1/layout/empty_search
```
Returns trending searches, recent searches, popular categories.

---

## Image URLs

Base pattern: `https://cdn.grofers.com/da/cms-assets/cms/product/<filename>.png`

With Cloudflare image resizing:
```
https://cdn.grofers.com/cdn-cgi/image/f=avif,fit=crop,q=50,metadata=none,w=360,h=318,dpr=1.0,background=%23F8F9FC/da/cms-assets/cms/product/<filename>.png
```

Resize parameters:
- `f`: Format (avif, webp)
- `fit`: crop, scale-down
- `q`: Quality (50)
- `w`, `h`: Dimensions
- `dpr`: Device pixel ratio
- `background`: Hex bg color (URL-encoded #)

---

## Key Implementation Notes

1. **No request signing/HMAC** — API relies on `auth_key` (static) + `access_token` (per-user)
2. **REST, not GraphQL** — All endpoints are REST POST/GET
3. **Location via headers** — `lat`/`lon` headers on every request determine store/pricing
4. **Server-driven UI** — Responses contain full layout, not just data. Must deep-parse widget trees
5. **Form-encoded auth** — OTP endpoints use `application/x-www-form-urlencoded`, NOT JSON
6. **Cloudflare CDN** — Behind Cloudflare with `__cf_bm` cookies, WAF, and Brotli compression
7. **OkHttp 5.0.0-alpha.14** — App uses OkHttp with Cronet transport
8. **Token format** — `v2::<uuid>`, no expiry observed yet (may be long-lived)
9. **Merchant context** — Products are tied to a `merchant_id` (store), determined by location
