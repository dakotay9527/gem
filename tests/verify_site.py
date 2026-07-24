import hashlib
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APK_NAME = "photo-curator-android-1.0.0.apk"
APK_SHA256 = "45cecf8a0eff0941af60edee0f6bf8f44db891200c3aae917fd5cc380b4e6f48"
APK_URL = f"https://dakotay9527.github.io/gem/downloads/{APK_NAME}"
QR_PATH = ROOT / "assets" / "android-download-qr.png"
APP_STORE_URL = "https://apps.apple.com/app/id6788588179"
IOS_VERSION = "v1.1"
APP_ASSETS = {
    "app-icon.png": (256, 256),
    "confirm-results.jpg": (1000, 1400),
    "range-score.jpg": (1000, 1400),
    "analysis-progress.jpg": (1000, 1400),
    "card-review.jpg": (1000, 1400),
    "android-range.png": (700, 1400),
}


class DownloadLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.apk_download_links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if (
            tag == "a"
            and "download" in values
            and values.get("href", "").endswith(".apk")
        ):
            self.apk_download_links.append(values)


class SiteReleaseTests(unittest.TestCase):
    def test_real_app_assets_are_published(self):
        import cv2

        asset_dir = ROOT / "assets" / "app"
        for name, (minimum_width, minimum_height) in APP_ASSETS.items():
            path = asset_dir / name
            self.assertTrue(path.is_file(), name)
            image = cv2.imread(str(path))
            self.assertIsNotNone(image, name)
            height, width = image.shape[:2]
            self.assertGreaterEqual(width, minimum_width, name)
            self.assertGreaterEqual(height, minimum_height, name)

    def test_signed_apk_and_checksum_are_published(self):
        apk = ROOT / "downloads" / APK_NAME
        checksum = apk.with_suffix(apk.suffix + ".sha256")

        self.assertTrue(apk.is_file())
        self.assertEqual(hashlib.sha256(apk.read_bytes()).hexdigest(), APK_SHA256)
        self.assertEqual(checksum.read_text().strip(), f"{APK_SHA256}  {APK_NAME}")

    def test_page_exposes_android_release_contract(self):
        html = (ROOT / "index.html").read_text()
        parser = DownloadLinkParser()
        parser.feed(html)

        self.assertEqual(len(parser.apk_download_links), 1)
        self.assertEqual(parser.apk_download_links[0]["href"], f"downloads/{APK_NAME}")
        self.assertIn('class="platform-downloads"', html)
        self.assertIn(
            'class="platform-download android-download" href="#android-download"',
            html,
        )
        self.assertIn(
            f'class="platform-download ios-download" href="{APP_STORE_URL}"',
            html,
        )
        self.assertIn('class="qr-download-panel" id="android-download"', html)
        self.assertIn('class="qr-download-panel"', html)
        self.assertIn('src="assets/android-download-qr.png"', html)
        self.assertIn(f'href="{APK_URL}"', html)
        self.assertIn(f'href="{APP_STORE_URL}"', html)
        self.assertIn("App Store 下载", html)
        self.assertIn("iPhone / iPad", html)
        self.assertIn(IOS_VERSION, html)
        self.assertIn("iOS 17+", html)
        self.assertNotIn("App Store 敬请期待", html)
        self.assertLess(
            html.index('class="section support"'),
            html.index('class="section install"'),
        )
        self.assertLess(
            html.index('class="section install"'),
            html.index('class="section policy"'),
        )
        self.assertEqual(html.count('class="section install"'), 1)
        for text in ("Android 10–16", "v1.0.0", "38 MB", APK_SHA256, "安卓安装说明"):
            self.assertIn(text, html)
        self.assertNotIn('href="#"', html)

    def test_page_uses_real_app_imagery_instead_of_mock_phone_ui(self):
        html = (ROOT / "index.html").read_text()

        for name in APP_ASSETS:
            self.assertIn(f"assets/app/{name}", html)
        for fragment in (
            'class="app-brand"',
            'class="hero-device-showcase"',
            'id="experience"',
            'class="device-gallery"',
            'class="device-shot',
        ):
            self.assertIn(fragment, html)
        for obsolete_fragment in (
            "phone-stage",
            "phone-screen",
            "mock-photo",
            "photo-wall",
            "tile tile-",
        ):
            self.assertNotIn(obsolete_fragment, html)
        self.assertGreaterEqual(html.count('class="device-shot'), 5)
        self.assertIn('fetchpriority="high"', html)
        self.assertGreaterEqual(html.count('loading="lazy"'), 4)

    def test_qr_code_points_to_official_apk(self):
        import cv2

        self.assertTrue(QR_PATH.is_file())
        image = cv2.imread(str(QR_PATH))
        decoded, points, _ = cv2.QRCodeDetector().detectAndDecode(image)

        self.assertIsNotNone(points)
        self.assertEqual(decoded, APK_URL)

    def test_mobile_hash_and_download_styles_exist(self):
        css = (ROOT / "styles.css").read_text()

        for selector in (
            ".android-download",
            ".download-label > span",
            ".checksum",
            ".install-guide",
            ".qr-download-panel",
            ".platform-downloads",
            ".platform-download",
            ".ios-download",
            ".ios-icon",
        ):
            self.assertIn(selector, css)
        self.assertIn("overflow-wrap: anywhere", css)
        self.assertIn("scroll-margin-top", css)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr))", css)

    def test_styles_match_the_app_design_system(self):
        css = (ROOT / "styles.css").read_text().lower()

        for token in (
            "--cream: #fff6e8",
            "--paper: #fffdf7",
            "--deep-ink: #2b2621",
            "--coral: #f36f45",
            "--mint: #8bd6c5",
            "--gold: #f8c96b",
            "--rose: #e66a70",
        ):
            self.assertIn(token, css)
        for selector in (
            ".app-brand",
            ".hero-device-showcase",
            ".privacy-promises",
            ".device-gallery",
            ".device-card",
        ):
            self.assertIn(selector, css)
        for obsolete_selector in (
            ".phone-stage",
            ".phone-screen",
            ".mock-photo",
            ".photo-wall",
            ".tile",
        ):
            self.assertNotIn(obsolete_selector, css)
        self.assertIn("scroll-snap-type: x mandatory", css)


if __name__ == "__main__":
    unittest.main()
