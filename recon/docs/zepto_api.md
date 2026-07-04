# Zepto API Documentation

> Pending traffic capture. APK has been patched and re-signed with SSL pinning bypass.
> Awaiting user test to verify the patched APK works with HTTP Toolkit.

## Package Name
`com.zeptoconsumerapp`

## APK Patching Notes
- OkHttp CertificatePinner methods are **obfuscated**: `check` → `a`, `lazyCerts` → `b`
- Patched signatures:
  - `a(Ljava/lang/String;Ljava/util/List;)V` → `return-void`
  - `b(Ljava/lang/String;Lkotlin/jvm/functions/Function0;)V` → `return-void`
- Also patched custom X509TrustManager.checkServerTrusted
- All split APKs re-signed with same debug keystore

## Known Domains
- `zeptonow.com`
- `zepto.co`

## Base URL
<!-- TODO: fill after traffic capture -->

## Authentication

### Request OTP
<!-- TODO -->

### Verify OTP
<!-- TODO -->

### Auth Token Format
<!-- TODO -->

## Headers
<!-- TODO: document required headers -->

## Endpoints

### Search
<!-- TODO -->

### Product Details
<!-- TODO -->

### Categories
<!-- TODO -->

### Cart
<!-- TODO -->

### Addresses
<!-- TODO -->

## Notes
- Is it REST or GraphQL?
- How is location communicated?
- Does the API use request signing (HMAC)?
