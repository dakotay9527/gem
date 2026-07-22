import hashlib
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APK_NAME = "photo-curator-android-1.0.0.apk"
APK_SHA256 = "45cecf8a0eff0941af60edee0f6bf8f44db891200c3aae917fd5cc380b4e6f48"


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
        for text in ("Android 10–16", "v1.0.0", "38 MB", APK_SHA256, "安卓安装说明"):
            self.assertIn(text, html)
        self.assertNotIn('href="#"', html)

    def test_mobile_hash_and_download_styles_exist(self):
        css = (ROOT / "styles.css").read_text()

        for selector in (".android-download", ".download-meta", ".checksum", ".install-guide"):
            self.assertIn(selector, css)
        self.assertIn("overflow-wrap: anywhere", css)


if __name__ == "__main__":
    unittest.main()
