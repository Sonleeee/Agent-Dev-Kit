"""
tester.py - Deterministic Web UI & E2E Tester
Supports:
1. Connecting to existing Chrome session via CDP (port 9222) or standalone Playwright.
2. Step-by-step automated actions (click, type, wait, scroll).
3. Visual assertions and evidence screenshot generation (Fail-Closed).
"""

import argparse
import asyncio
import os
import sys
import time
from typing import List, Tuple


def get_active_chrome_ws_endpoint():
    """Auto-detects active Chrome WebSocket endpoint from DevToolsActivePort."""
    active_port_file = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\DevToolsActivePort")
    if os.path.exists(active_port_file):
        try:
            with open(active_port_file, "r", encoding="utf-8") as f:
                port = f.readline().strip()
                path = f.readline().strip()
            if port and path:
                return f"ws://127.0.0.1:{port}{path}"
        except Exception:
            pass
    return None


async def get_browser(p, headless: bool = True):
    """Launches system Chrome or Edge to avoid downloading separate chromium binaries."""
    for ch in ["chrome", "msedge", None]:
        try:
            if ch:
                return await p.chromium.launch(channel=ch, headless=headless)
            else:
                return await p.chromium.launch(headless=headless)
        except Exception:
            continue
    raise RuntimeError("No suitable browser executable found (checked chrome, msedge, chromium).")


async def run_scenario(
    cdp_url: str = None,
    url: str = None,
    actions_dsl: str = None,
    screenshot_path: str = None,
    headless: bool = True,
    profile_dir: str = None,
    login_mode: bool = False,
) -> bool:
    from playwright.async_api import async_playwright

    print(f"[TESTER] Starting test execution...")
    start_time = time.time()
    success = True
    error_msg = ""

    async with async_playwright() as p:
        browser = None
        context = None

        if cdp_url:
            print(f"[TESTER] Connecting to CDP: {cdp_url}")
            browser = await p.chromium.connect_over_cdp(cdp_url)
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            # Open dedicated new tab if URL is given, otherwise use active tab
            if url:
                page = await context.new_page()
            else:
                page = context.pages[0] if context.pages else await context.new_page()
        elif profile_dir:
            print(f"[TESTER] Using persistent session profile: {profile_dir} (headless={headless})")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                channel="chrome",
                headless=headless,
            )
            page = context.pages[0] if context.pages else await context.new_page()
        else:
            print(f"[TESTER] Launching standalone browser via system Chrome/Edge (headless={headless})")
            browser = await get_browser(p, headless=headless)
            page = await browser.new_page()

        try:
            if url:
                print(f"[TESTER] Navigating to: {url}")
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)

            if login_mode:
                print("\n[LOGIN MODE] Browser opened! Please log in to your account.")
                print("[LOGIN MODE] Waiting 60 seconds for you to complete sign-in...")
                await asyncio.sleep(60)
                print("[LOGIN MODE] Session saved successfully!")
                return True

            # Parse DSL actions: "action1:arg,action2:arg"
            if actions_dsl:
                steps = [s.strip() for s in actions_dsl.split(",") if s.strip()]
                for idx, step in enumerate(steps, 1):
                    parts = step.split(":", 2)
                    cmd = parts[0].strip().lower()
                    arg1 = parts[1].strip() if len(parts) > 1 else ""
                    arg2 = parts[2].strip() if len(parts) > 2 else ""

                    print(f"  [Step {idx}] {cmd} -> {arg1}" + (f" | {arg2}" if arg2 else ""))

                    if cmd == "click":
                        await page.wait_for_selector(arg1, timeout=10000)
                        await page.click(arg1)
                    elif cmd == "type":
                        await page.wait_for_selector(arg1, timeout=10000)
                        await page.fill(arg1, arg2)
                    elif cmd == "wait":
                        wait_sec = float(arg1) if arg1 else 1.0
                        await asyncio.sleep(wait_sec)
                    elif cmd == "scroll":
                        y = int(arg1) if arg1 else 500
                        await page.evaluate(f"window.scrollBy(0, {y})")
                    elif cmd == "assert_title":
                        title = await page.title()
                        if arg1.lower() not in title.lower():
                            raise AssertionError(f"Expected title containing '{arg1}', got '{title}'")
                        print(f"    [ASSERT PASS] Title contains '{arg1}'")
                    elif cmd == "assert_text":
                        content = await page.content()
                        if arg1.lower() not in content.lower():
                            raise AssertionError(f"Expected text '{arg1}' not found in page content")
                        print(f"    [ASSERT PASS] Page contains text '{arg1}'")
                    elif cmd == "assert_selector":
                        elem = await page.wait_for_selector(arg1, timeout=5000)
                        if not elem:
                            raise AssertionError(f"Selector '{arg1}' not found")
                        print(f"    [ASSERT PASS] Found selector '{arg1}'")
                    else:
                        print(f"    [WARN] Unknown step action: {cmd}")

            # Capture evidence screenshot
            if screenshot_path:
                os.makedirs(os.path.dirname(os.path.abspath(screenshot_path)), exist_ok=True)
                await page.screenshot(path=screenshot_path, full_page=False)
                print(f"[TESTER] Evidence screenshot saved to: {screenshot_path}")

        except Exception as e:
            success = False
            error_msg = str(e)
            print(f"[TESTER FAIL] Error encountered: {error_msg}", file=sys.stderr)
            if screenshot_path:
                fail_shot = screenshot_path.replace(".png", "_fail.png")
                try:
                    await page.screenshot(path=fail_shot)
                    print(f"[TESTER] Saved failure screenshot to: {fail_shot}")
                except Exception:
                    pass
        finally:
            if cdp_url and url and page:
                try:
                    await page.close()
                except Exception:
                    pass
            elif context and profile_dir:
                await context.close()
            elif browser and not cdp_url:
                await browser.close()

    duration = round(time.time() - start_time, 2)
    print(f"[TESTER FINISH] Status: {'PASS' if success else 'FAIL'} in {duration}s")
    return success


def main():
    default_profile = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\AI_Session")
    parser = argparse.ArgumentParser(description="Web UI & E2E Tester")
    parser.add_argument("--url", help="Target URL", default=None)
    parser.add_argument("--session", action="store_true", help="Use active user Chrome session")
    parser.add_argument("--cdp-url", help="CDP connection endpoint", default=None)
    parser.add_argument("--profile", help=f"Persistent profile path (default: {default_profile})", default=None)
    parser.add_argument("--login", action="store_true", help="Open visible browser to log in and save session")
    parser.add_argument("--steps", help="Comma-separated DSL steps, e.g. 'wait:1,assert_title:Google'", default=None)
    parser.add_argument("--screenshot", help="Path to save evidence screenshot", default=None)
    parser.add_argument("--headed", action="store_true", default=False, help="Run with visible browser window (default: headless)")

    args = parser.parse_args()

    cdp_target = None
    if args.cdp_url:
        cdp_target = args.cdp_url
    elif args.session:
        cdp_target = get_active_chrome_ws_endpoint()

    if not args.url and not cdp_target and not args.login:
        print("Error: Either --url, --session, --cdp-url, or --login must be provided.", file=sys.stderr)
        sys.exit(1)

    profile_to_use = args.profile
    if args.login and not profile_to_use:
        profile_to_use = default_profile

    is_headless = False if (args.login or args.headed) else True

    result = asyncio.run(
        run_scenario(
            cdp_url=cdp_target,
            url=args.url or ("https://www.youtube.com" if args.login else None),
            actions_dsl=args.steps,
            screenshot_path=args.screenshot,
            headless=is_headless,
            profile_dir=profile_to_use,
            login_mode=args.login,
        )
    )

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
