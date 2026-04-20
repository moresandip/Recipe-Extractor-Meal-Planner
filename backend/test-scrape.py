#!/usr/bin/env python3
"""Test script to check if scraping and LLM are working"""
import sys
sys.path.insert(0, 'c:\\Users\\mores\\OneDrive\\Desktop\\Recipe Extractor & Meal Planner\\backend')

print("="*50)
print("TESTING SCRAPER & LLM")
print("="*50)

# Test 1: Check imports
print("\n1. Testing imports...")
try:
    from app.services.scraper import scraper
    print("   ✓ Scraper imported")
except Exception as e:
    print(f"   ✗ Scraper import failed: {e}")
    sys.exit(1)

try:
    from app.services.llm_service import llm_service
    print("   ✓ LLM Service imported")
except Exception as e:
    print(f"   ✗ LLM import failed: {e}")
    sys.exit(1)

# Test 2: Scrape a URL
print("\n2. Testing scraper...")
test_url = "https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/"
print(f"   URL: {test_url}")

result = scraper.scrape_url(test_url)
if result["success"]:
    print(f"   ✓ Scraping successful")
    print(f"   Title: {result.get('title', 'N/A')}")
    print(f"   Text length: {len(result.get('text_content', ''))}")
else:
    print(f"   ✗ Scraping failed: {result.get('error')}")
    sys.exit(1)

# Test 3: Test LLM
print("\n3. Testing LLM...")
text = result["text_content"][:5000]  # First 5000 chars
llm_result = llm_service.extract_recipe(text)

if llm_result["success"]:
    print(f"   ✓ LLM extraction successful")
    data = llm_result["data"]
    print(f"   Recipe: {data.get('title', 'N/A')}")
    print(f"   Cuisine: {data.get('cuisine', 'N/A')}")
else:
    print(f"   ✗ LLM failed: {llm_result.get('error')}")

print("\n" + "="*50)
print("TEST COMPLETE")
print("="*50)

input("\nPress Enter to exit...")
