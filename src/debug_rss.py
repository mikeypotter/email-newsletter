"""
RSS Feed Debugger
Tests RSS feeds to see what's being retrieved
"""

import feedparser
import requests
from datetime import datetime
from dateutil import parser as date_parser

def test_rss_feed(name, url):
    """Test a single RSS feed and show what we get"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print('='*60)

    try:
        # Try to fetch the feed
        print("Fetching feed...")
        feed = feedparser.parse(url)

        # Check for errors
        if feed.bozo:
            print(f"⚠️  Warning: Feed has errors - {feed.bozo_exception}")

        # Check feed info
        if hasattr(feed, 'status'):
            print(f"HTTP Status: {feed.status}")

        if hasattr(feed.feed, 'title'):
            print(f"Feed Title: {feed.feed.title}")

        # Count entries
        num_entries = len(feed.entries)
        print(f"\n✓ Found {num_entries} entries in feed")

        if num_entries == 0:
            print("❌ No articles found in feed!")
            return

        # Show first 5 entries
        print(f"\nShowing first {min(5, num_entries)} articles:")
        print("-" * 60)

        for i, entry in enumerate(feed.entries[:5], 1):
            print(f"\n[{i}] {entry.get('title', 'NO TITLE')}")

            # Show publication date
            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
                print(f"    Published: {pub_date.strftime('%Y-%m-%d %H:%M:%S')}")

                # Calculate age
                age = datetime.now() - pub_date
                hours_old = age.total_seconds() / 3600
                print(f"    Age: {hours_old:.1f} hours ago")
            elif hasattr(entry, 'published'):
                print(f"    Published: {entry.published}")
            else:
                print(f"    Published: NO DATE FOUND")

            # Show link
            if entry.get('link'):
                print(f"    Link: {entry.link}")

            # Show description (truncated)
            if entry.get('summary'):
                desc = entry.summary[:100].replace('\n', ' ')
                print(f"    Summary: {desc}...")

        print("\n✅ Feed test successful!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


def test_url_directly(name, url):
    """Test if we can even reach the URL"""
    print(f"\n{'='*60}")
    print(f"Direct URL Test: {name}")
    print(f"URL: {url}")
    print('='*60)

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"HTTP Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
        print(f"Content Length: {len(response.content)} bytes")

        if response.status_code == 200:
            print("✅ URL is accessible")
            # Show first 500 chars of content
            preview = response.text[:500].replace('\n', ' ')
            print(f"\nContent preview:\n{preview}...")
        else:
            print(f"❌ URL returned error status: {response.status_code}")

    except Exception as e:
        print(f"❌ Could not reach URL: {str(e)}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("RSS FEED DEBUG TOOL")
    print("="*60)

    # Test Ottawa RSS feeds
    feeds = [
        ("CBC Ottawa", "https://www.cbc.ca/cmlink/rss-canada-ottawa"),
        ("CTV News Ottawa", "https://ottawa.ctvnews.ca/rss/ctv-news-ottawa-1.822136"),
        ("Ottawa Citizen", "https://ottawacitizen.com/feed"),
        ("Ottawa Sun", "https://ottawasun.com/feed"),
    ]

    # First, test if we can reach the URLs
    print("\n\n" + "="*60)
    print("PHASE 1: Testing URL Accessibility")
    print("="*60)

    for name, url in feeds:
        test_url_directly(name, url)

    # Then test RSS parsing
    print("\n\n" + "="*60)
    print("PHASE 2: Testing RSS Feed Parsing")
    print("="*60)

    for name, url in feeds:
        test_rss_feed(name, url)

    print("\n\n" + "="*60)
    print("DEBUG COMPLETE")
    print("="*60)
