from playwright.async_api import async_playwright
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__) # Initialize logger, this will be used to log messages

# Global variables to store browser instance and related objects, for internal use
_playwright: Optional[Any] = None
_browser: Optional[Any] = None
_context: Optional[Any] = None
_page: Optional[Any] = None
_browser_running = False

async def run(url: str, browser_type: str = "chromium") -> bool:
    """
    Launches a browser instance then opens a new page, and navigates to the specified URL.
    If browser is already running, it will navigate to the new URL.
    The browser will remain open until stop() is explicitly called.
    
    Args:
        url (str): The URL to navigate to.
        browser_type (str): The type of browser to launch. Default is "chromium".
        
    Returns:
        bool: True if the page was opened successfully, False otherwise.
    """
    global _playwright, _browser, _context, _page, _browser_running
    
    try:
        # Initialize browser if not already running
        if _browser is None or _playwright is None:
            _playwright = await async_playwright().start()
            browser_launcher = getattr(_playwright, browser_type)
            _browser = await browser_launcher.launch(headless=False)
            _context = await _browser.new_context()
            _page = await _context.new_page()
            _browser_running = True
            logger.info(f"Initialized new {browser_type} browser instance")
        
        # Navigate to URL
        logger.info(f"Navigating to {url}")
        await _page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await _page.wait_for_load_state("networkidle")
        logger.info(f"Successfully loaded {url}")
        return True
        
    except Exception as e:
        logger.error(f"Error in browser operation: {str(e)}")
        return False


async def stop():
    """
    Closes the browser instance and stops playwright.
    """
    global _playwright, _browser, _context, _page
    
    if _page:
        await _page.close()
        _page = None
    
    if _context:
        await _context.close()
        _context = None
    
    if _browser:
        await _browser.close()
        _browser = None
    
    if _playwright:
        await _playwright.stop()
        _playwright = None
    
    logger.info("Browser session closed")   

import asyncio

if __name__ == "__main__":
    async def main():
        success = await run("https://allenyzh.com/portfolio")
        if success:
            logger.info("Page opened successfully")
            await stop()

            # await asyncio.sleep(10) 

    # Run the main function
    asyncio.run(main())
