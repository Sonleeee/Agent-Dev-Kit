"""
harvest.py - Deterministic Web Harvester for Deep Research
Supports:
1. Direct scraping with Playwright or Crawl4AI.
2. Attaching to an already-open Chrome browser via CDP (port 9222).
3. Extracting clean Markdown / text with zero HTML clutter.
"""

import argparse
import asyncio
import os
import re
import sys
from typing import Optional


def html_to_clean_markdown(html_content: str, title: str = "") -> str:
    """Basic deterministic HTML-to-Markdown cleaner without heavy 3rd-party dependencies."""
    # Strip script, style, svg, noscript, nav, footer, header
    cleaned = re.sub(
        r"<(script|style|svg|noscript|nav|footer|header)[^>]*>.*?</\1>",
        "",
        html_content,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # Strip inline tags but keep content
    cleaned = re.sub(r"<(span|div|section|article|main)[^>]*>", "\n", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"</(span|div|section|article|main)>", "\n", cleaned, flags=re.IGNORECASE)

    # Convert headers
    for i in range(6, 0, -1):
        cleaned = re.sub(
            rf"<h{i}[^>]*>(.*?)</h{i}>",
            lambda m: f"\n\n{'#' * i} {m.group(1).strip()}\n\n",
            cleaned,
            flags=re.DOTALL | re.IGNORECASE,
        )

    # Convert paragraphs and line breaks
    cleaned = re.sub(r"<br\s*/?>", "\n", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<p[^>]*>(.*?)</p>", lambda m: f"\n\n{m.group(1).strip()}\n\n", cleaned, flags=re.DOTALL | re.IGNORECASE)

    # Convert list items
    cleaned = re.sub(r"<li[^>]*>(.*?)</li>", lambda m: f"\n- {m.group(1).strip()}", cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"</?(ul|ol)[^>]*>", "\n", cleaned, flags=re.IGNORECASE)

    # Convert links: <a href="url">text</a> -> [text](url)
    cleaned = re.sub(
        r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        lambda m: f"[{m.group(2).strip()}]({m.group(1)})" if m.group(2).strip() else "",
        cleaned,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Convert code blocks
    cleaned = re.sub(
        r"<pre[^>]*><code[^>]*>(.*?)</code></pre>",
        lambda m: f"\n```\n{m.group(1).strip()}\n```\n",
        cleaned,
        flags=re.DOTALL | re.IGNORECASE,
    )
    cleaned = re.sub(r"<code[^>]*>(.*?)</code>", lambda m: f"`{m.group(1).strip()}`", cleaned, flags=re.DOTALL | re.IGNORECASE)

    # Strip remaining HTML tags
    cleaned = re.sub(r"<[^>]+>", "", cleaned)

    # Decode HTML entities
    cleaned = (
        cleaned.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&nbsp;", " ")
    )

    # Collapse excess whitespace
    lines = [line.strip() for line in cleaned.splitlines()]
    non_empty_lines = []
    blank = False
    for line in lines:
        if line:
            non_empty_lines.append(line)
            blank = False
        elif not blank:
            non_empty_lines.append("")
            blank = True

    body = "\n".join(non_empty_lines).strip()
    if title:
        return f"# {title.strip()}\n\n{body}\n"
    return body


def get_active_chrome_ws_endpoint() -> Optional[str]:
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


async def scrape_via_cdp(cdp_url: str, url: Optional[str] = None, selector: Optional[str] = None) -> tuple[str, str]:
    """Attaches to existing running Chrome instance via CDP without disrupting active user tabs."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()

        # Always open a separate tab for URL scraping and close it when done
        if url:
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                title = await page.title()
                if selector:
                    element = await page.query_selector(selector)
                    html = await element.inner_html() if element else await page.content()
                else:
                    html = await page.content()
                return title, html
            finally:
                await page.close()
        else:
            # If no URL given, inspect the current active tab non-destructively
            page = context.pages[0] if context.pages else await context.new_page()
            title = await page.title()
            if selector:
                element = await page.query_selector(selector)
                html = await element.inner_html() if element else await page.content()
            else:
                html = await page.content()
            return title, html


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


async def scrape_with_profile(url: str, profile_dir: str, headless: bool = True, selector: Optional[str] = None) -> tuple[str, str]:
    """Scrapes using a persistent user profile (keeps logins/cookies)."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            channel="chrome",
            headless=headless,
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        title = await page.title()
        if selector:
            element = await page.query_selector(selector)
            html = await element.inner_html() if element else await page.content()
        else:
            html = await page.content()
        await context.close()
        return title, html


async def scrape_standalone(url: str, headless: bool = True, selector: Optional[str] = None) -> tuple[str, str]:
    """Runs a standalone browser session to scrape target URL without disturbing the user."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await get_browser(p, headless=headless)
        page = await browser.new_page()
        response = await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        final_url = page.url
        title = await page.title()

        # Check if redirected to login wall
        if any(w in final_url.lower() for w in ["/login", "auth", "signin", "accounts.google.com"]) and not any(w in url.lower() for w in ["/login", "auth", "signin"]):
            print(f"[AUTH DETECTED] Page redirected to login wall: {final_url}", file=sys.stderr)

        if selector:
            element = await page.query_selector(selector)
            html = await element.inner_html() if element else await page.content()
        else:
            html = await page.content()
        await browser.close()
        return title, html


async def main():
    default_profile = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\AI_Session")
    parser = argparse.ArgumentParser(description="Web Harvester for Deep Research")
    parser.add_argument("--url", help="Target URL to scrape", default=None)
    parser.add_argument("--cdp-url", help="Connect to running browser via CDP (e.g. http://localhost:9222)", default=None)
    parser.add_argument("--session", action="store_true", help="Use active user Chrome session (may trigger security prompt on chrome://inspect)")
    parser.add_argument("--profile", help=f"Persistent profile path to keep logins (default: {default_profile})", default=None)
    parser.add_argument("--selector", help="Specific CSS selector to extract", default=None)
    parser.add_argument("--format", choices=["markdown", "raw_html"], default="markdown", help="Output format")
    parser.add_argument("--out", help="Output file path (default: stdout)", default=None)
    parser.add_argument("--headless", action="store_true", default=True, help="Run headless if standalone")

    args = parser.parse_args()

    # Only connect to user session if explicitly requested via --session or --cdp-url
    cdp_target = None
    if args.cdp_url:
        cdp_target = args.cdp_url
    elif args.session:
        cdp_target = get_active_chrome_ws_endpoint()
        if not cdp_target:
            print("[WARN] --session requested but active Chrome with remote debugging was not found. Falling back to standalone.", file=sys.stderr)

    if not args.url and not cdp_target:
        print("Error: Either --url, --session, or --cdp-url must be provided.", file=sys.stderr)
        sys.exit(1)

    if cdp_target:
        print(f"[HARVEST] Mode: CDP attached ({cdp_target})")
    elif args.profile:
        print(f"[HARVEST] Mode: Persistent profile ({args.profile})")
    else:
        print(f"[HARVEST] Mode: Standalone browser")

    if args.url:
        print(f"[HARVEST] Target URL: {args.url}")

    if cdp_target:
        title, html = await scrape_via_cdp(cdp_target, args.url, args.selector)
    elif args.profile:
        title, html = await scrape_with_profile(args.url, args.profile, args.headless, args.selector)
    else:
        title, html = await scrape_standalone(args.url, args.headless, args.selector)

    if args.format == "markdown":
        output_content = html_to_clean_markdown(html, title=title)
    else:
        output_content = html

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"[HARVEST] Saved {len(output_content)} chars to {args.out}")
    else:
        print("\n--- OUTPUT ---\n")
        print(output_content[:2000] + ("\n... [truncated]" if len(output_content) > 2000 else ""))


if __name__ == "__main__":
    asyncio.run(main())
