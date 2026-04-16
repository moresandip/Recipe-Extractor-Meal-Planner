import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import re


class RecipeScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    
    def scrape_url(self, url: str) -> Dict[str, Any]:
        """Scrape recipe content from URL"""
        try:
            import cloudscraper
            scraper_client = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'desktop': True
                }
            )
            response = scraper_client.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            text_content = self._extract_text(soup)
            
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
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "url": url,
                "error": f"Failed to fetch URL: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": f"Scraping error: {str(e)}"
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
