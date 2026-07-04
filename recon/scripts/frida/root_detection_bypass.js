/*
 * Basic Root Detection Bypass for Android
 * Hooks common root-checking methods and returns false.
 *
 * Usage: frida -U -f <package_name> -l root_detection_bypass.js --no-pause
 */

Java.perform(function () {
    console.log("[*] Root Detection Bypass loaded");

    // --- RootBeer library (commonly used) ---
    try {
        var RootBeer = Java.use("com.scottyab.rootbeer.RootBeer");
        RootBeer.isRooted.implementation = function () {
            console.log("[+] RootBeer.isRooted() bypassed");
            return false;
        };
        RootBeer.isRootedWithoutBusyBoxCheck.implementation = function () {
            console.log("[+] RootBeer.isRootedWithoutBusyBoxCheck() bypassed");
            return false;
        };
    } catch (e) {
        console.log("[-] RootBeer not found");
    }

    // --- Common file-based root checks ---
    try {
        var File = Java.use("java.io.File");
        var originalExists = File.exists;
        File.exists.implementation = function () {
            var path = this.getAbsolutePath();
            var rootPaths = ["/system/app/Superuser.apk", "/system/xbin/su", "/system/bin/su", "/sbin/su", "/data/local/xbin/su", "/data/local/bin/su", "/data/local/su", "/su/bin/su"];
            if (rootPaths.indexOf(path) >= 0) {
                console.log("[+] File.exists bypassed for: " + path);
                return false;
            }
            return originalExists.call(this);
        };
    } catch (e) {
        console.log("[-] File.exists hook failed: " + e);
    }

    // --- Runtime.exec su check ---
    try {
        var Runtime = Java.use("java.lang.Runtime");
        var originalExec = Runtime.exec.overload("java.lang.String");
        Runtime.exec.overload("java.lang.String").implementation = function (cmd) {
            if (cmd === "su" || cmd.indexOf("/su") >= 0) {
                console.log("[+] Runtime.exec bypassed for: " + cmd);
                throw Java.use("java.io.IOException").$new("Permission denied");
            }
            return originalExec.call(this, cmd);
        };
    } catch (e) {
        console.log("[-] Runtime.exec hook failed: " + e);
    }

    // --- Build.TAGS check ---
    try {
        var Build = Java.use("android.os.Build");
        Build.TAGS.value = "release-keys";
        console.log("[+] Build.TAGS set to release-keys");
    } catch (e) {
        console.log("[-] Build.TAGS override failed: " + e);
    }

    console.log("[*] Root Detection Bypass complete");
});
