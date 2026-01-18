"""
Web Scraper Module
Extracts news articles from configured websites
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArticleScraper:
    """Scrapes articles from configured news sources"""

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
                articles = self._scrape_source(source, cutoff_time)
                all_articles.extend(articles)
                logger.info(f"Found {len(articles)} articles from {source['name']}")
            except Exception as e:
                logger.error(f"Error scraping {source['name']}: {str(e)}")

        return all_articles

    def _scrape_source(self, source: Dict, cutoff_time: datetime) -> List[Dict]:
        """Scrape a single news source"""
        try:
            response = requests.get(source['url'], headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            articles = []
            selectors = source['selectors']

            # Find all article elements
            article_elements = soup.select(selectors.get('article', 'article'))

            for element in article_elements[:50]:  # Limit to first 50 articles
                try:
                    article = self._extract_article_data(element, selectors, source['name'], source['url'])
                    if article and self._is_recent(article.get('date'), cutoff_time):
                        articles.append(article)
                except Exception as e:
                    logger.debug(f"Error extracting article: {str(e)}")
                    continue

            return articles

        except requests.RequestException as e:
            logger.error(f"Request failed for {source['url']}: {str(e)}")
            return []

    def _extract_article_data(self, element, selectors: Dict, source_name: str, base_url: str) -> Optional[Dict]:
        """Extract article data from HTML element"""
        title_elem = element.select_one(selectors.get('title', 'h2'))
        if not title_elem:
            return None

        title = title_elem.get_text(strip=True)
        if not title:
            return None

        # Extract link
        link_elem = element.select_one(selectors.get('link', 'a'))
        link = link_elem.get('href', '') if link_elem else ''

        # Make link absolute if relative
        if link and not link.startswith('http'):
            from urllib.parse import urljoin
            link = urljoin(base_url, link)

        # Extract date if available
        date_elem = element.select_one(selectors.get('date', 'time'))
        date_str = None
        if date_elem:
            date_str = date_elem.get('datetime') or date_elem.get_text(strip=True)

        # Extract description/summary if available
        description = ""
        if 'description' in selectors:
            desc_elem = element.select_one(selectors['description'])
            if desc_elem:
                description = desc_elem.get_text(strip=True)

        return {
            'title': title,
            'link': link,
            'source': source_name,
            'date': date_str,
            'description': description,
            'scraped_at': datetime.now().isoformat()
        }

    def _is_recent(self, date_str: Optional[str], cutoff_time: datetime) -> bool:
        """Check if article date is recent enough"""
        if not date_str:
            # If no date, assume it's recent (front page articles)
            return True

        try:
            article_date = date_parser.parse(date_str)
            # Make timezone-naive for comparison
            if article_date.tzinfo:
                article_date = article_date.replace(tzinfo=None)
            return article_date >= cutoff_time
        except Exception:
            # If we can't parse the date, include it
            return True

    def get_article_content(self, url: str) -> Optional[str]:
        """Fetch full article content from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            # Try to find main content (common patterns)
            content_selectors = [
                'article',
                '.article-content',
                '.post-content',
                '.entry-content',
                'main'
            ]

            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    # Get text, removing scripts and styles
                    for script in content(['script', 'style']):
                        script.decompose()
                    return content.get_text(strip=True, separator='\n')

            return None

        except Exception as e:
            logger.debug(f"Could not fetch content from {url}: {str(e)}")
            return None
