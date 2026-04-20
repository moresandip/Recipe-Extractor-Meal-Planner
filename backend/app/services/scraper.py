import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

class RecipeScraper:
    def __init__(self):
        # Real browser headers to avoid blocking
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_url(self, url: str) -> Dict[str, Any]:
        """Scrape recipe content from URL"""
        try:
            import cloudscraper
            import json
            
            scraper_client = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'desktop': True
                }
            )
            
            # Use extra headers for better resilience
            logger.info(f"Scraping URL: {url}")
            response = scraper_client.get(url, timeout=30)
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code == 404:
                return {
                    "success": False,
                    "url": url,
                    "error": f"The recipe page was not found (404). Please verify the URL: {url}"
                }
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            text_content = self._extract_text(soup)
            logger.info(f"Extracted text length: {len(text_content) if text_content else 0}")
            
            if not text_content or len(text_content.strip()) < 100:
                # Try fallback with requests
                logger.warning("Cloudscraper failed, trying fallback with requests...")
                return self._fallback_scrape(url)
            
            # Try to extract structured data if available
            structured_data = self._extract_structured_data(soup)
            
            return {
                "success": True,
                "url": url,
                "title": self._extract_title(soup),
                "html": str(soup),
                "text_content": text_content,
                "structured_data": structured_data
            }
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else "Unknown"
            return {
                "success": False,
                "url": url,
                "error": f"Website returned an error ({status_code}). Site might be blocking automated access."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "url": url,
                "error": f"Failed to connect to the website: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Scraping error: {str(e)}")
            return {
                "success": False,
                "url": url,
                "error": f"Scraping logic error: {str(e)}"
            }
    
    def _fallback_scrape(self, url: str) -> Dict[str, Any]:
        """Fallback scraping using requests session"""
        try:
            logger.info(f"Trying fallback scrape with session...")
            
            # First visit the main site to get cookies
            try:
                from urllib.parse import urlparse
                parsed = urlparse(url)
                base_url = f"{parsed.scheme}://{parsed.netloc}"
                self.session.get(base_url, timeout=10)
            except:
                pass
            
            # Now try the actual URL
            response = self.session.get(url, timeout=30, allow_redirects=True)
            logger.info(f"Fallback response status: {response.status_code}")
            
            if response.status_code == 404:
                return {
                    "success": False,
                    "url": url,
                    "error": f"Page not found (404). The recipe may have been removed or URL is incorrect."
                }
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = self._extract_text(soup)
            
            if not text_content or len(text_content.strip()) < 100:
                return {
                    "success": False,
                    "url": url,
                    "error": f"Website returned empty content. Status: {response.status_code}. Site might be blocking scrapers."
                }
            
            structured_data = self._extract_structured_data(soup)
            
            return {
                "success": True,
                "url": url,
                "title": self._extract_title(soup),
                "html": str(soup),
                "text_content": text_content,
                "structured_data": structured_data
            }
        except Exception as e:
            logger.error(f"Fallback scraping failed: {str(e)}")
            return {
                "success": False,
                "url": url,
                "error": f"Failed to scrape website: {str(e)}. The website may be blocking automated access."
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return "Unknown Recipe"
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract readable text content from the page"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:15000]  # Limit to avoid token limits
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract JSON-LD structured data if available"""
        structured_data = {}
        
        # Look for JSON-LD scripts
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                import json
                data = json.loads(script.string)
                
                # Check if it's a recipe
                if isinstance(data, dict):
                    if data.get('@type') == 'Recipe' or 'Recipe' in str(data.get('@type', '')):
                        structured_data = data
                        break
                    elif isinstance(data.get('@graph'), list):
                        for item in data['@graph']:
                            if item.get('@type') == 'Recipe':
                                structured_data = item
                                break
                elif isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Recipe':
                            structured_data = item
                            break
                            
            except (json.JSONDecodeError, AttributeError):
                continue
        
        return structured_data


scraper = RecipeScraper()
