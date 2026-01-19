"""
Auto Scraper Module
Automatically extracts news articles without manual CSS selectors
Supports RSS feeds and AI-powered content extraction
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from typing import List, Dict, Optional
import logging
import feedparser
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoScraper:
    """Automatically scrapes articles using RSS feeds or AI extraction"""

    def __init__(self, sources: List[Dict]):
        self.sources = sources
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_all_sources(self, hours_ago: int = 24) -> List[Dict]:
        """
        Scrape articles from all configured sources

        Args:
            hours_ago: Only include articles from the last N hours

        Returns:
            List of article dictionaries
        """
        all_articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours_ago)

        for source in self.sources:
            logger.info(f"Scraping {source['name']}...")
            try:
                # Try RSS first if available
                if 'rss_url' in source:
                    articles = self._scrape_rss(source, cutoff_time)
                else:
                    # Try to auto-discover RSS or use intelligent extraction
                    articles = self._auto_scrape(source, cutoff_time)

                all_articles.extend(articles)
                logger.info(f"Found {len(articles)} articles from {source['name']}")
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {str(e)}")

        return all_articles

    def _scrape_rss(self, source: Dict, cutoff_time: datetime) -> List[Dict]:
        """Scrape articles from RSS feed"""
        try:
            logger.debug(f"Fetching RSS feed: {source['rss_url']}")

            # Fetch RSS using requests first (better SSL handling and timeout support)
            try:
                response = requests.get(source['rss_url'], headers=self.headers, timeout=10)
                response.raise_for_status()
                feed = feedparser.parse(response.content)
            except requests.RequestException as e:
                logger.error(f"Failed to fetch RSS feed: {str(e)}")
                # Fallback to feedparser's built-in fetching
                logger.debug("Trying feedparser's built-in fetching...")
                feed = feedparser.parse(source['rss_url'])

            # Debug: Show feed status
            if hasattr(feed, 'status'):
                logger.debug(f"RSS HTTP Status: {feed.status}")

            total_entries = len(feed.entries)
            logger.debug(f"Total entries in feed: {total_entries}")

            if total_entries == 0:
                logger.warning(f"No entries found in RSS feed for {source['name']}")
                return []

            articles = []
            filtered_count = 0

            for entry in feed.entries:
                # Parse publication date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])

                # Check if recent enough
                if pub_date and pub_date < cutoff_time:
                    filtered_count += 1
                    continue

                # If no date, include it (assume it's recent)
                if not pub_date:
                    logger.debug(f"No date found for article: {entry.get('title', 'NO TITLE')[:50]}... - including it anyway")

                # Extract article data
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'source': source['name'],
                    'date': entry.get('published', entry.get('updated', '')),
                    'description': self._clean_html(entry.get('summary', entry.get('description', ''))),
                    'scraped_at': datetime.now().isoformat()
                }

                if article['title']:
                    articles.append(article)

            logger.debug(f"Filtered out {filtered_count} old articles (older than cutoff)")
            logger.debug(f"Kept {len(articles)} recent articles")

            if filtered_count > 0 and len(articles) == 0:
                logger.warning(f"All {total_entries} articles from {source['name']} were older than {cutoff_time}")
                logger.warning(f"Try increasing --hours parameter (currently filtering last 24 hours)")

            return articles

        except Exception as e:
            logger.error(f"RSS parsing failed for {source['name']}: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
            return []

    def _auto_scrape(self, source: Dict, cutoff_time: datetime) -> List[Dict]:
        """
        Automatically scrape using intelligent extraction
        First tries to find RSS, then falls back to HTML parsing
        """
        # Try to discover RSS feed first
        rss_url = self._discover_rss(source['url'])
        if rss_url:
            logger.info(f"Auto-discovered RSS feed: {rss_url}")
            source['rss_url'] = rss_url
            return self._scrape_rss(source, cutoff_time)

        # Fall back to intelligent HTML parsing
        return self._scrape_html_intelligent(source, cutoff_time)

    def _discover_rss(self, url: str) -> Optional[str]:
        """Try to auto-discover RSS feeds from a website"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            # Look for RSS link tags
            rss_link = soup.find('link', type='application/rss+xml')
            if rss_link and rss_link.get('href'):
                return urljoin(url, rss_link['href'])

            atom_link = soup.find('link', type='application/atom+xml')
            if atom_link and atom_link.get('href'):
                return urljoin(url, atom_link['href'])

            # Common RSS URL patterns to try
            from urllib.parse import urlparse
            base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

            common_patterns = [
                f"{url}/rss",
                f"{url}/feed",
                f"{url}/rss.xml",
                f"{url}/feed.xml",
                f"{base_url}/rss",
                f"{base_url}/feed",
            ]

            for pattern in common_patterns:
                try:
                    test_response = requests.head(pattern, headers=self.headers, timeout=5)
                    if test_response.status_code == 200:
                        return pattern
                except:
                    continue

            return None

        except Exception as e:
            logger.debug(f"RSS discovery failed: {str(e)}")
            return None

    def _scrape_html_intelligent(self, source: Dict, cutoff_time: datetime) -> List[Dict]:
        """
        Intelligent HTML scraping without manual selectors
        Uses common patterns and heuristics
        """
        try:
            response = requests.get(source['url'], headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            articles = []

            # Try common article patterns
            article_selectors = [
                'article',
                '[class*="article"]',
                '[class*="story"]',
                '[class*="post"]',
                '[class*="card"]',
                '[class*="item"]'
            ]

            article_elements = []
            for selector in article_selectors:
                elements = soup.select(selector)
                if elements:
                    article_elements = elements
                    break

            for element in article_elements[:30]:  # Limit to first 30
                try:
                    article = self._extract_article_intelligent(element, source['name'], source['url'])
                    if article and article['title']:
                        articles.append(article)
                except Exception as e:
                    logger.debug(f"Error extracting article: {str(e)}")
                    continue

            return articles

        except requests.RequestException as e:
            logger.error(f"Request failed for {source['url']}: {str(e)}")
            return []

    def _extract_article_intelligent(self, element, source_name: str, base_url: str) -> Optional[Dict]:
        """Extract article data using intelligent patterns"""

        # Find title - try multiple patterns
        title = None
        title_selectors = ['h1', 'h2', 'h3', '[class*="title"]', '[class*="headline"]']
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                if title and len(title) > 10:  # Reasonable title length
                    break

        if not title:
            return None

        # Find link
        link = None
        link_elem = element.find('a', href=True)
        if link_elem:
            link = link_elem['href']
            if link and not link.startswith('http'):
                link = urljoin(base_url, link)

        # Find date
        date_str = None
        time_elem = element.find('time')
        if time_elem:
            date_str = time_elem.get('datetime') or time_elem.get_text(strip=True)

        # Find description
        description = ""
        desc_selectors = ['p', '[class*="description"]', '[class*="summary"]', '[class*="excerpt"]']
        for selector in desc_selectors:
            desc_elem = element.select_one(selector)
            if desc_elem:
                description = desc_elem.get_text(strip=True)
                if description and len(description) > 20:
                    break

        return {
            'title': title,
            'link': link or '',
            'source': source_name,
            'date': date_str,
            'description': description,
            'scraped_at': datetime.now().isoformat()
        }

    def _clean_html(self, html_text: str) -> str:
        """Remove HTML tags from text"""
        if not html_text:
            return ""
        soup = BeautifulSoup(html_text, 'lxml')
        return soup.get_text(strip=True)


# Common RSS feed URLs for Ottawa news sources
OTTAWA_RSS_FEEDS = {
    'CBC Ottawa': 'https://www.cbc.ca/cmlink/rss-canada-ottawa',
    'CTV News Ottawa': 'https://ottawa.ctvnews.ca/rss/ctv-news-ottawa-1.822136',
    'Ottawa Citizen': 'https://ottawacitizen.com/feed',
    'Ottawa Sun': 'https://ottawasun.com/feed',
}
