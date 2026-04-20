import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import logging
import time

logger = logging.getLogger(__name__)

class SmartRecipeScraper:
    """Enhanced scraper with multiple fallback strategies"""
    
    def __init__(self):
        self.session = requests.Session()
        # Rotate user agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
    
    def scrape_url(self, url: str) -> Dict[str, Any]:
        """Try multiple strategies to scrape the URL"""
        
        strategies = [
            self._try_cloudscraper,
            self._try_requests_session,
            self._try_requests_direct,
            self._try_with_delay
        ]
        
        for i, strategy in enumerate(strategies):
            try:
                logger.info(f"Trying strategy {i+1}/{len(strategies)}: {strategy.__name__}")
                result = strategy(url)
                if result["success"]:
                    logger.info(f"Strategy {i+1} succeeded!")
                    return result
                else:
                    logger.warning(f"Strategy {i+1} failed: {result.get('error')}")
            except Exception as e:
                logger.error(f"Strategy {i+1} error: {str(e)}")
                continue
        
        # All strategies failed
        return {
            "success": False,
            "url": url,
            "error": f"All scraping strategies failed for {url}. The website is actively blocking automated access. Try these recipe sites instead: SimplyRecipes.com, FoodNetwork.com, BonAppetit.com, or Tasty.co"
        }
    
    def _try_cloudscraper(self, url: str) -> Dict[str, Any]:
        """Try with cloudscraper"""
        import cloudscraper
        
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        response = scraper.get(url, timeout=30)
        return self._process_response(response, url)
    
    def _try_requests_session(self, url: str) -> Dict[str, Any]:
        """Try with session and headers"""
        headers = {
            "User-Agent": self.user_agents[0],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        
        # First visit homepage to get cookies
        from urllib.parse import urlparse
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        try:
            self.session.get(base, headers=headers, timeout=10)
        except:
            pass
        
        response = self.session.get(url, headers=headers, timeout=30)
        return self._process_response(response, url)
    
    def _try_requests_direct(self, url: str) -> Dict[str, Any]:
        """Try direct request with different user agent"""
        headers = {
            "User-Agent": self.user_agents[1],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        return self._process_response(response, url)
    
    def _try_with_delay(self, url: str) -> Dict[str, Any]:
        """Try with delay to avoid rate limiting"""
        time.sleep(2)  # Wait 2 seconds
        
        headers = {
            "User-Agent": self.user_agents[2],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        return self._process_response(response, url)
    
    def _process_response(self, response, url: str) -> Dict[str, Any]:
        """Process HTTP response"""
        if response.status_code == 404:
            return {
                "success": False,
                "url": url,
                "error": "Page not found (404). Please check the URL."
            }
        
        if response.status_code == 403:
            return {
                "success": False,
                "url": url,
                "error": "Access forbidden (403). Website is blocking scrapers."
            }
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = self._extract_text(soup)
        
        if not text_content or len(text_content.strip()) < 50:
            return {
                "success": False,
                "url": url,
                "error": "Could not extract content from page."
            }
        
        return {
            "success": True,
            "url": url,
            "title": self._extract_title(soup),
            "text_content": text_content,
            "structured_data": self._extract_structured_data(soup)
        }
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract readable text from soup"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title = soup.find('title')
        if title:
            return title.get_text(strip=True)
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        return "Unknown Recipe"
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> Dict:
        """Extract JSON-LD structured data"""
        import json
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Recipe':
                            return item
                elif data.get('@type') == 'Recipe':
                    return data
            except:
                continue
        return None

# Global instance
smart_scraper = SmartRecipeScraper()
