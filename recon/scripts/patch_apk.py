"""
APK Patcher — pull, decompile, patch cert trust + SSL pinning, rebuild, sign, install.

Usage:
    python patch_apk.py <package_name>

Example:
    python patch_apk.py com.zeptoconsumerapp
    python patch_apk.py com.grofers.customerapp
"""

import os
import re
import shutil
import subprocess
import sys
import glob
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TOOLS_DIR = SCRIPT_DIR.parent / "tools"
APKTOOL_JAR = TOOLS_DIR / "apktool.jar"
KEYSTORE = TOOLS_DIR / "debug.keystore"
KEYSTORE_PASS = "mycart123"
KEY_ALIAS = "mycart"
APKSIGNER = Path(os.environ.get("LOCALAPPDATA", "")) / "Android/Sdk/build-tools/35.0.0/apksigner.bat"
WORK_DIR = SCRIPT_DIR.parent / "patched"

NETWORK_SECURITY_CONFIG = """<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </base-config>
</network-security-config>
"""


def run(cmd, **kwargs):
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        print(f"  STDERR: {result.stderr[:1000]}")
        raise RuntimeError(f"Command failed: {cmd[0]}")
    return result


def pull_apk(package: str, out_dir: Path) -> list[Path]:
    """Pull all APK splits from device."""
    result = run(["adb", "shell", "pm", "path", package])
    paths = [line.replace("package:", "").strip() for line in result.stdout.strip().split("\n")]

    apk_files = []
    for i, device_path in enumerate(paths):
        local_name = out_dir / f"{package}.part{i}.apk"
        run(["adb", "pull", device_path, str(local_name)])
        apk_files.append(local_name)
        print(f"  Pulled: {device_path} -> {local_name.name}")

    return apk_files


def decompile(apk_path: Path, out_dir: Path):
    """Decompile APK with apktool."""
    if out_dir.exists():
        shutil.rmtree(out_dir)
    run(["java", "-jar", str(APKTOOL_JAR), "d", str(apk_path), "-o", str(out_dir), "-f"])


def patch_network_security_config(decompiled_dir: Path):
    """Add/replace network_security_config.xml to trust user certificates."""
    res_xml = decompiled_dir / "res" / "xml"
    res_xml.mkdir(parents=True, exist_ok=True)

    nsc_path = res_xml / "network_security_config.xml"
    nsc_path.write_text(NETWORK_SECURITY_CONFIG, encoding="utf-8")
    print(f"  Wrote: {nsc_path}")

    manifest_path = decompiled_dir / "AndroidManifest.xml"
    manifest = manifest_path.read_text(encoding="utf-8")

    if "networkSecurityConfig" not in manifest:
        manifest = manifest.replace(
            "<application",
            '<application android:networkSecurityConfig="@xml/network_security_config"',
            1,
        )
        manifest_path.write_text(manifest, encoding="utf-8")
        print("  Patched AndroidManifest.xml with networkSecurityConfig attribute")
    else:
        print("  AndroidManifest.xml already has networkSecurityConfig")


def fix_manifest_nulls(decompiled_dir: Path):
    """Fix android:resource='@null' entries that crash on newer Android versions."""
    manifest_path = decompiled_dir / "AndroidManifest.xml"
    manifest = manifest_path.read_text(encoding="utf-8")
    new_manifest = manifest.replace('android:resource="@null"', 'android:value=""')
    if new_manifest != manifest:
        manifest_path.write_text(new_manifest, encoding="utf-8")
        print("  Fixed @null resource references in AndroidManifest.xml")
    else:
        print("  No @null references to fix")


def patch_okhttp_pinning(decompiled_dir: Path):
    """
    Disable OkHttp CertificatePinner by patching smali.
    Handles both named (check) and obfuscated (a, b, etc.) method names
    by matching on the signature (String, List)V and (String, Function0)V
    inside CertificatePinner.smali files.
    """
    pinners_patched = 0
    smali_dirs = sorted(decompiled_dir.glob("smali*"))

    for smali_dir in smali_dirs:
        for pinner_file in smali_dir.rglob("CertificatePinner.smali"):
            content = pinner_file.read_text(encoding="utf-8")
            original = content

            # Pattern 1: check(String, List)V — named or obfuscated
            pattern_list = (
                r"(\.method public (?:final )?\w+\(Ljava/lang/String;Ljava/util/List;\)V)"
                r"(.*?)"
                r"(\.end method)"
            )
            content, c1 = re.subn(
                pattern_list,
                r"\1\n    .registers 3\n    return-void\n\3",
                content,
                flags=re.DOTALL,
            )

            # Pattern 2: check(String, Function0)V — Kotlin lazy variant (obfuscated)
            pattern_fn = (
                r"(\.method public (?:final )?\w+\(Ljava/lang/String;Lkotlin/jvm/functions/Function0;\)V)"
                r"(.*?)"
                r"(\.end method)"
            )
            content, c2 = re.subn(
                pattern_fn,
                r"\1\n    .registers 3\n    return-void\n\3",
                content,
                flags=re.DOTALL,
            )

            total = c1 + c2
            if total > 0:
                pinner_file.write_text(content, encoding="utf-8")
                pinners_patched += total
                print(f"  Patched {total} method(s) in {pinner_file.relative_to(decompiled_dir)}")

    # Scan for other pinning-related classes
    for smali_dir in smali_dirs:
        for smali_file in smali_dir.rglob("*.smali"):
            if "CertificatePinner" in smali_file.name:
                continue
            try:
                content = smali_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            if "SSLPeerUnverifiedException" in content and (
                "pin" in smali_file.name.lower() or "cert" in smali_file.name.lower()
            ):
                print(f"  Found potential pinner: {smali_file.relative_to(decompiled_dir)}")

    if pinners_patched == 0:
        print("  No OkHttp CertificatePinner found (may use different pinning)")
    else:
        print(f"  Patched {pinners_patched} CertificatePinner method(s) total")


def patch_trustmanager_checks(decompiled_dir: Path):
    """
    Find and neuter custom TrustManager implementations that reject user certs.
    """
    patched = 0
    smali_dirs = sorted(decompiled_dir.glob("smali*"))

    for smali_dir in smali_dirs:
        for smali_file in smali_dir.rglob("*.smali"):
            try:
                content = smali_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            if "Ljavax/net/ssl/X509TrustManager;" not in content:
                continue

            # Patch checkServerTrusted to return void
            pattern = (
                r"(\.method public (?:final )?checkServerTrusted\(\[Ljava/security/cert/X509Certificate;Ljava/lang/String;\)V)"
                r"(.*?)"
                r"(\.end method)"
            )
            new_content, count = re.subn(
                pattern,
                r"\1\n    .registers 3\n    return-void\n\3",
                content,
                flags=re.DOTALL,
            )
            if count > 0:
                smali_file.write_text(new_content, encoding="utf-8")
                patched += count
                print(f"  Patched checkServerTrusted in {smali_file.relative_to(decompiled_dir)}")

    print(f"  Patched {patched} custom TrustManager(s)")


def rebuild(decompiled_dir: Path, out_apk: Path):
    """Rebuild APK from decompiled directory."""
    run(["java", "-jar", str(APKTOOL_JAR), "b", str(decompiled_dir), "-o", str(out_apk)])
    print(f"  Built: {out_apk}")


def sign_apk(apk_path: Path):
    """Sign APK with debug keystore using apksigner."""
    if APKSIGNER.exists():
        run([
            str(APKSIGNER), "sign",
            "--ks", str(KEYSTORE),
            "--ks-key-alias", KEY_ALIAS,
            "--ks-pass", f"pass:{KEYSTORE_PASS}",
            "--key-pass", f"pass:{KEYSTORE_PASS}",
            str(apk_path),
        ])
    else:
        # Fallback to jarsigner
        run([
            "jarsigner",
            "-keystore", str(KEYSTORE),
            "-storepass", KEYSTORE_PASS,
            "-keypass", KEYSTORE_PASS,
            str(apk_path),
            KEY_ALIAS,
        ])
    print(f"  Signed: {apk_path}")


def install_apk(apk_path: Path):
    """Install APK on device (uninstall first to avoid signature mismatch)."""
    run(["adb", "install", "-r", "-d", str(apk_path)])
    print(f"  Installed: {apk_path.name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python patch_apk.py <package_name>")
        print("Example: python patch_apk.py com.zeptoconsumerapp")
        sys.exit(1)

    package = sys.argv[1]
    pkg_work_dir = WORK_DIR / package
    pkg_work_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  APK Patcher — {package}")
    print(f"{'='*60}\n")

    # Step 1: Pull APK from device
    print("[1/7] Pulling APK from device...")
    apk_files = pull_apk(package, pkg_work_dir)
    base_apk = apk_files[0]  # First one is the base APK

    # Step 2: Decompile
    print("\n[2/7] Decompiling with apktool...")
    decompiled_dir = pkg_work_dir / "decompiled"
    decompile(base_apk, decompiled_dir)

    # Step 3: Patch network security config
    print("\n[3/8] Patching network_security_config.xml...")
    patch_network_security_config(decompiled_dir)

    # Step 4: Fix manifest issues
    print("\n[4/8] Fixing manifest @null references...")
    fix_manifest_nulls(decompiled_dir)

    # Step 5: Patch OkHttp certificate pinning
    print("\n[5/8] Patching OkHttp CertificatePinner...")
    patch_okhttp_pinning(decompiled_dir)

    # Step 6: Patch custom TrustManagers
    print("\n[6/8] Patching custom TrustManagers...")
    patch_trustmanager_checks(decompiled_dir)

    # Step 7: Rebuild
    print("\n[7/8] Rebuilding APK...")
    patched_apk = pkg_work_dir / f"{package}-patched.apk"
    rebuild(decompiled_dir, patched_apk)

    # Step 8: Sign all APKs (patched base + original splits)
    print("\n[8/8] Signing all APKs...")
    sign_apk(patched_apk)
    split_apks = [f for f in apk_files[1:] if f.exists()]
    for split in split_apks:
        sign_apk(split)

    print(f"\n{'='*60}")
    print(f"  Patched APK ready: {patched_apk}")
    print(f"{'='*60}\n")

    # Install instructions
    print("To install:")
    print(f"  adb uninstall {package}")
    all_apks = [str(patched_apk)] + [str(s) for s in split_apks]
    print(f"  adb install-multiple {' '.join(all_apks)}")


if __name__ == "__main__":
    main()
