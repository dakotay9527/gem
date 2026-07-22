# Gem Android Download Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the signed 相册拾光 Android v1.0.0 APK from the official GitHub Pages website with trustworthy download metadata and installation guidance.

**Architecture:** Keep the existing dependency-free static site. Store the signed APK and checksum under `downloads/`, link them with relative URLs from `index.html`, and use a Python standard-library regression test to verify content, artifacts, and hashes before publication.

**Tech Stack:** HTML5, CSS3, Python 3 `unittest`, GitHub Pages

## Global Constraints

- Android download must remain under `https://dakotay9527.github.io/gem/`; do not link to GitHub Release or an app store.
- Release version is `v1.0.0`, target support text is `Android 10–16`, and displayed size is `38 MB`.
- APK SHA-256 must be `45cecf8a0eff0941af60edee0f6bf8f44db891200c3aae917fd5cc380b4e6f48`.
- Preserve the current single-page design and dependency-free hosting model.
- iOS remains unavailable and must not expose a placeholder `href="#"` download link.

---

### Task 1: Add Static Download Contract Tests

**Files:**
- Create: `tests/verify_site.py`

**Interfaces:**
- Consumes: repository root containing `index.html`, `styles.css`, and `downloads/`.
- Produces: `python3 -m unittest tests/verify_site.py` as the release gate.

- [ ] **Step 1: Write the failing test**

```python
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
        self.download_links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and "download" in values:
            self.download_links.append(values)


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
        self.assertEqual(len(parser.download_links), 1)
        self.assertEqual(parser.download_links[0]["href"], f"downloads/{APK_NAME}")
        for text in ("Android 10–16", "v1.0.0", "38 MB", APK_SHA256, "安卓安装说明"):
            self.assertIn(text, html)
        self.assertNotIn('href="#"', html)

    def test_mobile_hash_and_download_styles_exist(self):
        css = (ROOT / "styles.css").read_text()
        for selector in (".android-download", ".download-meta", ".checksum", ".install-guide"):
            self.assertIn(selector, css)
        self.assertIn("overflow-wrap: anywhere", css)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/verify_site.py -v`

Expected: FAIL because `downloads/photo-curator-android-1.0.0.apk` and the Android page contract do not exist.

- [ ] **Step 3: Commit the failing release contract**

```bash
git add tests/verify_site.py
git commit -m "test: define Android website release contract"
```

### Task 2: Add Signed Release Artifacts

**Files:**
- Create: `downloads/photo-curator-android-1.0.0.apk`
- Create: `downloads/photo-curator-android-1.0.0.apk.sha256`

**Interfaces:**
- Consumes: verified signed release artifacts from `PhotoCuratorAndroid/release/`.
- Produces: immutable same-origin website files referenced by `index.html`.

- [ ] **Step 1: Copy the signed APK and checksum file**

Run:

```bash
mkdir -p downloads
cp /Users/dakota/Documents/dex/.worktrees/photo-curator-android/PhotoCuratorAndroid/release/photo-curator-android-1.0.0.apk downloads/
cp /Users/dakota/Documents/dex/.worktrees/photo-curator-android/PhotoCuratorAndroid/release/photo-curator-android-1.0.0.apk.sha256 downloads/
```

- [ ] **Step 2: Verify byte identity and checksum**

Run: `shasum -a 256 downloads/photo-curator-android-1.0.0.apk && cmp -s downloads/photo-curator-android-1.0.0.apk /Users/dakota/Documents/dex/.worktrees/photo-curator-android/PhotoCuratorAndroid/release/photo-curator-android-1.0.0.apk`

Expected: hash `45cecf8a0eff0941af60edee0f6bf8f44db891200c3aae917fd5cc380b4e6f48` and exit status 0.

### Task 3: Implement Download and Installation UI

**Files:**
- Modify: `index.html`
- Modify: `styles.css`

**Interfaces:**
- Consumes: `downloads/photo-curator-android-1.0.0.apk` and checksum.
- Produces: one `<a download>` link to the APK, visible release metadata, installation instructions, and platform-neutral privacy wording.

- [ ] **Step 1: Replace the placeholder hero action**

Add a single same-origin download link:

```html
<a class="android-download" href="downloads/photo-curator-android-1.0.0.apk" download>
  <span class="android-icon" aria-hidden="true"></span>
  <span><small>官网下载</small><strong>Android 版</strong></span>
</a>
<div class="download-copy">
  <span class="download-meta">Android 10–16 · v1.0.0 · 38 MB</span>
  <span class="ios-note">iPhone / iPad 版本：App Store 敬请期待</span>
</div>
```

- [ ] **Step 2: Add installation and checksum content**

Add an `id="install"` section with three explicit steps and render the full SHA-256 inside `<code class="checksum">` plus a relative checksum download link.

- [ ] **Step 3: Make privacy wording platform-neutral**

Replace iOS-only export wording with Android system picker and iOS share/document picker wording without changing the no-upload and no-tracking claims.

- [ ] **Step 4: Add responsive styles**

Add focused styles for `.android-download`, `.android-icon`, `.download-copy`, `.download-meta`, `.ios-note`, `.install-guide`, and `.checksum`; at `max-width: 640px`, keep the button full width and allow the checksum to wrap.

- [ ] **Step 5: Run the release contract and verify green**

Run: `python3 -m unittest tests/verify_site.py -v`

Expected: 3 tests PASS.

- [ ] **Step 6: Commit the website implementation and artifacts**

```bash
git add index.html styles.css downloads/
git commit -m "feat: publish Android download on official website"
```

### Task 4: Verify Locally and Publish

**Files:**
- Modify only if verification exposes a defect: `index.html`, `styles.css`, or `tests/verify_site.py`.

**Interfaces:**
- Consumes: completed branch and its test gate.
- Produces: published GitHub Pages site and verified live APK.

- [ ] **Step 1: Run all static tests and artifact checks**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
git diff --check
shasum -a 256 downloads/photo-curator-android-1.0.0.apk
```

Expected: 3 tests PASS, no diff errors, expected SHA-256.

- [ ] **Step 2: Serve and probe the complete site locally**

Run `python3 -m http.server 8765`, then request `/`, `/styles.css`, the APK, and checksum file. Expect HTTP 200 and APK content length equal to the local file size.

- [ ] **Step 3: Inspect desktop and mobile layouts**

Open the local URL at normal desktop size and a 390 px viewport. Confirm the download call-to-action and install guide are visible, keyboard-focusable, and do not create horizontal scrolling.

- [ ] **Step 4: Push the branch and fast-forward main**

Push `codex/gem-android-download`, then update `main` only after the branch verification is green.

- [ ] **Step 5: Verify the published site**

Request the official page and APK URL until GitHub Pages serves the new commit. Expect HTTP 200 for both, then download the live APK and verify the expected SHA-256.
