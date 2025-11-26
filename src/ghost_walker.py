from playwright.sync_api import sync_playwright
import os
import time

class GhostWalker:
    def __init__(self):
        self.headless = True
        if not os.path.exists("intel/screenshots"):
            os.makedirs("intel/screenshots", exist_ok=True)

    def scan_url(self, url, wait_time=5):
        report = {}
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=self.headless,
                    args=['--disable-blink-features=AutomationControlled']
                )
                
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                
                page = context.new_page()
                
                print(f"[GhostWalker] Infiltrating: {url}")
                page.goto(url, wait_until='networkidle', timeout=60000)
                
                time.sleep(wait_time)
                
                title = page.title()
                content = page.content() # Full HTML
                text = page.inner_text('body')
                
                timestamp = int(time.time())
                safe_name = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).rstrip()[:30]
                screenshot_path = f"intel/screenshots/{timestamp}_{safe_name}.png"
                
                page.screenshot(path=screenshot_path, full_page=True)
                
                report = {
                    "status": "SUCCESS",
                    "title": title,
                    "screenshot_path": screenshot_path,
                    "text_preview": text[:2000],
                    "url": url
                }
                
                browser.close()
                return report

        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e),
                "url": url
            }


