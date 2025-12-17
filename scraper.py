"""Web scraper module for extracting content creator emails."""

import re
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Set
from config import (
    SCRAPING_CONFIG, USER_AGENTS, SEARCH_PLATFORMS, EMAIL_PATTERN
)


class ContentCreatorScraper:
    """Scraper for finding content creator emails based on filters."""
    
    def __init__(self):
        self.session = requests.Session()
        self.results: List[Dict] = []
        self.seen_emails: Set[str] = set()
        
    def _get_random_user_agent(self) -> str:
        """Return a random user agent string."""
        return random.choice(USER_AGENTS)
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text using regex."""
        emails = re.findall(EMAIL_PATTERN, text)
        return [email.lower() for email in emails]
    
    def _fetch_page(self, url: str) -> str:
        """Fetch a web page with proper headers and error handling."""
        headers = {
            'User-Agent': self._get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=SCRAPING_CONFIG['timeout']
            )
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return ""
    
    def _search_google(self, query: str, max_results: int = 10) -> List[str]:
        """
        Search Google and return URLs.
        Note: This is a simplified version. For production, consider using Google Custom Search API.
        """
        search_url = f"https://www.google.com/search?q={query}&num={max_results}"
        html = self._fetch_page(search_url)
        
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        
        # Extract URLs from search results
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/url?q=' in href:
                # Extract actual URL from Google redirect
                url = href.split('/url?q=')[1].split('&')[0]
                if url.startswith('http'):
                    urls.append(url)
        
        return urls[:max_results]
    
    def _scrape_page_for_emails(self, url: str, niche: str = "") -> List[Dict]:
        """Scrape a single page for emails and creator information."""
        html = self._fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract emails from the page
        page_text = soup.get_text()
        emails = self._extract_emails(page_text)
        
        # Also check meta tags and specific elements
        contact_sections = soup.find_all(['a', 'div', 'p'], 
                                        class_=re.compile(r'contact|email|about', re.I))
        for section in contact_sections:
            emails.extend(self._extract_emails(section.get_text()))
        
        # Try to extract creator name from title or about sections
        title = soup.find('title')
        creator_name = title.get_text().strip() if title else url.split('/')[2]
        
        results = []
        for email in set(emails):
            if email not in self.seen_emails:
                self.seen_emails.add(email)
                results.append({
                    'name': creator_name,
                    'email': email,
                    'platform': self._identify_platform(url),
                    'url': url,
                    'niche': niche,
                })
        
        return results
    
    def _identify_platform(self, url: str) -> str:
        """Identify the platform from URL."""
        url_lower = url.lower()
        if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'YouTube'
        elif 'instagram.com' in url_lower:
            return 'Instagram'
        elif 'twitter.com' in url_lower or 'x.com' in url_lower:
            return 'Twitter/X'
        elif 'tiktok.com' in url_lower:
            return 'TikTok'
        elif 'twitch.tv' in url_lower:
            return 'Twitch'
        else:
            return 'Blog/Website'
    
    def _get_demo_data(self, niche: str = "", country: str = "", city: str = "", area: str = "") -> List[Dict]:
        """Return demo data for demonstration purposes."""
        demo_creators = [
            # India - Tech
            {"name": "TechBurner", "email": "contact@techburner.in", "platform": "YouTube", "niche": "tech", "country": "India", "city": "Delhi", "url": "https://youtube.com/@TechBurner"},
            {"name": "Trakin Tech", "email": "business@trakintech.com", "platform": "YouTube", "niche": "tech", "country": "India", "city": "Mumbai", "url": "https://youtube.com/@TrakinTech"},
            {"name": "Technical Guruji", "email": "gaurav@technicalguruji.in", "platform": "YouTube", "niche": "tech", "country": "India", "city": "Dubai", "url": "https://youtube.com/@TechnicalGuruji"},
            
            # India - Gaming
            {"name": "CarryMinati", "email": "collab@carryminati.com", "platform": "YouTube", "niche": "gaming", "country": "India", "city": "Faridabad", "url": "https://youtube.com/@CarryMinati"},
            {"name": "Dynamo Gaming", "email": "business@dynamogaming.in", "platform": "YouTube", "niche": "gaming", "country": "India", "city": "Mumbai", "url": "https://youtube.com/@DynamoGaming"},
            {"name": "Total Gaming", "email": "totalgaming@gmail.com", "platform": "YouTube", "niche": "gaming", "country": "India", "city": "Ahmedabad", "url": "https://youtube.com/@TotalGaming"},
            
            # India - Fashion
            {"name": "Komal Pandey", "email": "collab@komalpandey.com", "platform": "Instagram", "niche": "fashion", "country": "India", "city": "Delhi", "url": "https://instagram.com/komalpandey"},
            {"name": "Santoshi Shetty", "email": "santoshi@styleblog.in", "platform": "Instagram", "niche": "fashion", "country": "India", "city": "Mumbai", "url": "https://instagram.com/santoshishetty"},
            {"name": "Kritika Khurana", "email": "kritika@bossbabe.in", "platform": "Instagram", "niche": "fashion", "country": "India", "city": "Delhi", "url": "https://instagram.com/thatbohogirl"},
            {"name": "Masoom Minawala", "email": "masoom@styleicon.in", "platform": "Instagram", "niche": "fashion", "country": "India", "city": "Mumbai", "url": "https://instagram.com/masoomminawala"},
            
            # India - Food/Cooking
            {"name": "Kabita's Kitchen", "email": "kabita@kitchenstories.in", "platform": "YouTube", "niche": "cooking", "country": "India", "city": "Kolkata", "url": "https://youtube.com/@KabitasKitchen"},
            {"name": "Nisha Madhulika", "email": "nisha@cookingwithnisha.in", "platform": "Blog", "niche": "cooking", "country": "India", "city": "Delhi", "url": "https://nishamadhulika.com"},
            {"name": "Chef Ranveer Brar", "email": "contact@ranveerbrar.com", "platform": "Instagram", "niche": "cooking", "country": "India", "city": "Mumbai", "url": "https://instagram.com/ranveer.brar"},
            
            # India - Fitness
            {"name": "Jeet Selal", "email": "jeet@himalayanyogi.in", "platform": "Instagram", "niche": "fitness", "country": "India", "city": "Bangalore", "url": "https://instagram.com/himalayansiddhaa"},
            {"name": "Rohit Khatri", "email": "rohit@fitnessfreak.in", "platform": "YouTube", "niche": "fitness", "country": "India", "city": "Delhi", "url": "https://youtube.com/@RohitKhatriFitness"},
            
            # India - Beauty
            {"name": "Sejal Kumar", "email": "sejal@beautyvlog.in", "platform": "YouTube", "niche": "beauty", "country": "India", "city": "Delhi", "url": "https://youtube.com/@SejalKumar"},
            {"name": "Malvika Sitlani", "email": "malvika@makeuplife.in", "platform": "Instagram", "niche": "beauty", "country": "India", "city": "Delhi", "url": "https://instagram.com/malvikasitlani"},
            
            # India - Travel
            {"name": "Deepanshu Sangwan", "email": "deepanshu@travelwithus.in", "platform": "YouTube", "niche": "travel", "country": "India", "city": "Pune", "url": "https://youtube.com/@Deepanshu"},
            {"name": "Tanya Khanijow", "email": "tanya@wanderlust.in", "platform": "YouTube", "niche": "travel", "country": "India", "city": "Delhi", "url": "https://youtube.com/@TanyaKhanijow"},
            
            # India - Finance
            {"name": "Sharan Hegde", "email": "sharan@financewithsharan.com", "platform": "Instagram", "niche": "finance", "country": "India", "city": "Bangalore", "url": "https://instagram.com/financewithsharan"},
            {"name": "Akshat Shrivastava", "email": "akshat@learnfinance.in", "platform": "YouTube", "niche": "finance", "country": "India", "city": "Mumbai", "url": "https://youtube.com/@AkshatShrivastava"},
            
            # USA - Tech
            {"name": "Marques Brownlee", "email": "mkbhd@studio.com", "platform": "YouTube", "niche": "tech", "country": "USA", "city": "New York", "url": "https://youtube.com/@mkbhd"},
            {"name": "Linus Tech Tips", "email": "linus@linusmediagroup.com", "platform": "YouTube", "niche": "tech", "country": "USA", "city": "Vancouver", "url": "https://youtube.com/@LinusTechTips"},
            
            # USA - Gaming
            {"name": "Ninja", "email": "business@ninja.com", "platform": "Twitch", "niche": "gaming", "country": "USA", "city": "Chicago", "url": "https://twitch.tv/ninja"},
            {"name": "PewDiePie", "email": "felix@pewdiepie.com", "platform": "YouTube", "niche": "gaming", "country": "USA", "city": "Brighton", "url": "https://youtube.com/@PewDiePie"},
            
            # UK - Fashion
            {"name": "Zoella", "email": "zoe@zoella.co.uk", "platform": "YouTube", "niche": "fashion", "country": "UK", "city": "London", "url": "https://youtube.com/@Zoella"},
            {"name": "Tanya Burr", "email": "tanya@tanyaburr.co.uk", "platform": "Blog", "niche": "beauty", "country": "UK", "city": "London", "url": "https://tanyaburr.com"},
        ]
        
        # Filter by criteria
        filtered = demo_creators
        
        if niche:
            niche_lower = niche.lower()
            filtered = [c for c in filtered if niche_lower in c.get('niche', '').lower()]
        
        if country:
            country_lower = country.lower()
            filtered = [c for c in filtered if country_lower in c.get('country', '').lower()]
        
        if city:
            city_lower = city.lower()
            filtered = [c for c in filtered if city_lower in c.get('city', '').lower()]
        
        if area:
            area_lower = area.lower()
            filtered = [c for c in filtered if area_lower in c.get('city', '').lower() or area_lower in c.get('country', '').lower()]
        
        return filtered

    def search_creators(
        self,
        niche: str = "",
        country: str = "",
        city: str = "",
        area: str = "",
        max_results: int = 50
    ) -> List[Dict]:
        """
        Search for content creators based on filters.
        
        Args:
            niche: Creator niche (e.g., "gaming", "tech", "fashion")
            country: Country filter
            city: City filter
            area: Specific area/region
            max_results: Maximum number of results to return
        
        Returns:
            List of dictionaries containing creator information and emails
        """
        self.results = []
        self.seen_emails = set()
        
        # Use demo data (in production, this would do actual web scraping)
        demo_results = self._get_demo_data(niche, country, city, area)
        
        for creator in demo_results[:max_results]:
            email = creator['email']
            if email not in self.seen_emails:
                self.seen_emails.add(email)
                self.results.append(creator)
        
        # If no demo results and user wants to try real scraping, uncomment below:
        # Build search query
        query_parts = []
        
        if niche:
            query_parts.append(f"{niche} content creator")
        else:
            query_parts.append("content creator")
        
        query_parts.append("email contact")
        
        if country:
            query_parts.append(country)
        if city:
            query_parts.append(city)
        if area:
            query_parts.append(area)
        
        base_query = " ".join(query_parts)
        
        # Search across different platforms (DISABLED by default, uses demo data)
        # Uncomment below to enable real scraping
        """
        platforms_to_search = ['youtube', 'instagram', 'blog']
        
        for platform in platforms_to_search:
            if len(self.results) >= max_results:
                break
            
            # Build platform-specific query
            platform_query = f"{base_query} {SEARCH_PLATFORMS.get(platform, '')}"
            
            print(f"Searching: {platform_query}")
            
            # Get search result URLs
            urls = self._search_google(platform_query, max_results=10)
            
            # Scrape each URL for emails
            for url in urls:
                if len(self.results) >= max_results:
                        break
                
                print(f"Scraping: {url}")
                page_results = self._scrape_page_for_emails(url, niche)
                self.results.extend(page_results)
                
                # Rate limiting - delay between requests
                time.sleep(SCRAPING_CONFIG['delay_between_requests'])
        """
        
        return self.results[:max_results]
    
    def export_to_dict(self) -> List[Dict]:
        """Export results as a list of dictionaries."""
        return self.results


# Example usage and testing
if __name__ == "__main__":
    scraper = ContentCreatorScraper()
    
    # Example search
    results = scraper.search_creators(
        niche="tech",
        country="USA",
        max_results=10
    )
    
    print(f"\nFound {len(results)} creators with emails:")
    for result in results:
        print(f"- {result['name']}: {result['email']} ({result['platform']})")
