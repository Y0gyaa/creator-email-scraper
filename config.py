"""Configuration settings for the content creator email scraper."""

import os

# Scraping settings
SCRAPING_CONFIG = {
    'delay_between_requests': 2,  # seconds
    'timeout': 10,  # seconds
    'max_results': 100,
    'max_retries': 3,
}

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# Platform-specific search URLs (examples - will use Google search primarily)
SEARCH_PLATFORMS = {
    'youtube': 'site:youtube.com',
    'instagram': 'site:instagram.com',
    'twitter': 'site:twitter.com OR site:x.com',
    'tiktok': 'site:tiktok.com',
    'blog': 'blog OR blogger',
}

# Email regex pattern
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Flask settings
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
}

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)
