/*
 * Universal Android SSL Pinning Bypass
 * Works with: OkHttp CertificatePinner, TrustManagerImpl, Conscrypt, network_security_config
 *
 * Usage: frida -U -f <package_name> -l ssl_pinning_bypass.js --no-pause
 *
 * Blinkit:  frida -U -f com.grofers.customerapp -l ssl_pinning_bypass.js --no-pause
 * Zepto:    frida -U -f com.zeptoconsumerapp -l ssl_pinning_bypass.js --no-pause
 */

Java.perform(function () {
    console.log("[*] SSL Pinning Bypass loaded");

    // --- OkHttp3 CertificatePinner ---
    try {
        var CertificatePinner = Java.use("okhttp3.CertificatePinner");
        CertificatePinner.check.overload("java.lang.String", "java.util.List").implementation = function (hostname, peerCertificates) {
            console.log("[+] OkHttp3 CertificatePinner.check bypassed for: " + hostname);
        };
    } catch (e) {
        console.log("[-] OkHttp3 CertificatePinner not found");
    }

    // --- TrustManagerImpl (Android system) ---
    try {
        var TrustManagerImpl = Java.use("com.android.org.conscrypt.TrustManagerImpl");
        TrustManagerImpl.verifyChain.implementation = function (untrustedChain, trustAnchorChain, host, clientAuth, ocspData, tlsSctData) {
            console.log("[+] TrustManagerImpl.verifyChain bypassed for: " + host);
            return untrustedChain;
        };
    } catch (e) {
        console.log("[-] TrustManagerImpl not found");
    }

    // --- Conscrypt (newer Android) ---
    try {
        var ConscryptPlatform = Java.use("org.conscrypt.Platform");
        ConscryptPlatform.checkServerTrusted.overload("javax.net.ssl.X509TrustManager", "[Ljava.security.cert.X509Certificate;", "java.lang.String", "org.conscrypt.AbstractConscryptSocket").implementation = function (tm, chain, authType, socket) {
            console.log("[+] Conscrypt Platform.checkServerTrusted bypassed");
        };
    } catch (e) {
        console.log("[-] Conscrypt Platform not found");
    }

    // --- Custom X509TrustManager implementations ---
    try {
        var X509TrustManager = Java.use("javax.net.ssl.X509TrustManager");
        var SSLContext = Java.use("javax.net.ssl.SSLContext");

        var TrustManager = Java.registerClass({
            name: "com.mycart.BypassTrustManager",
            implements: [X509TrustManager],
            methods: {
                checkClientTrusted: function (chain, authType) {},
                checkServerTrusted: function (chain, authType) {},
                getAcceptedIssuers: function () {
                    return [];
                },
            },
        });

        var TrustManagers = [TrustManager.$new()];
        var sslContext = SSLContext.getInstance("TLS");
        sslContext.init(null, TrustManagers, null);
        console.log("[+] Custom TrustManager installed");
    } catch (e) {
        console.log("[-] Custom TrustManager setup failed: " + e);
    }

    console.log("[*] SSL Pinning Bypass complete");
});
