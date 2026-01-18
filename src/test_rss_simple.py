"""
Simple RSS Feed Tester (no external dependencies except requests)
"""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

def test_rss_simple(name, url):
    """Test RSS feed with just standard library"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print('='*60)

    try:
        # Fetch the feed
        print("Fetching feed...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"✓ HTTP Status: {response.status}")
            content = response.read()
            print(f"✓ Downloaded {len(content)} bytes")

            # Try to parse XML
            print("Parsing XML...")
            root = ET.fromstring(content)

            # Find items (RSS) or entries (Atom)
            items = root.findall('.//item')  # RSS format
            if not items:
                items = root.findall('.//{http://www.w3.org/2005/Atom}entry')  # Atom format

            print(f"\n✓ Found {len(items)} articles in feed")

            if len(items) == 0:
                print("❌ No articles found!")
                # Show first 500 chars of XML for debugging
                print("\nXML Preview:")
                print(content[:500].decode('utf-8', errors='ignore'))
                return

            # Show first 5 articles
            print(f"\nShowing first {min(5, len(items))} articles:")
            print("-" * 60)

            for i, item in enumerate(items[:5], 1):
                # Get title (RSS or Atom)
                title_elem = item.find('title')
                if title_elem is None:
                    title_elem = item.find('{http://www.w3.org/2005/Atom}title')
                title = title_elem.text if title_elem is not None else "NO TITLE"

                print(f"\n[{i}] {title}")

                # Get publication date
                pub_date_elem = item.find('pubDate')  # RSS
                if pub_date_elem is None:
                    pub_date_elem = item.find('{http://www.w3.org/2005/Atom}published')  # Atom
                if pub_date_elem is None:
                    pub_date_elem = item.find('{http://www.w3.org/2005/Atom}updated')  # Atom updated

                if pub_date_elem is not None:
                    print(f"    Published: {pub_date_elem.text}")
                else:
                    print(f"    Published: NO DATE")

                # Get link
                link_elem = item.find('link')
                if link_elem is None:
                    link_elem = item.find('{http://www.w3.org/2005/Atom}link')
                    if link_elem is not None:
                        link = link_elem.get('href', 'NO LINK')
                    else:
                        link = "NO LINK"
                else:
                    link = link_elem.text if link_elem.text else "NO LINK"

                print(f"    Link: {link}")

            print(f"\n✅ {name} feed is working!")

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"❌ Connection Error: {e.reason}")
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SIMPLE RSS FEED TESTER")
    print("No external dependencies required!")
    print("="*60)

    feeds = [
        ("CBC Ottawa", "https://www.cbc.ca/cmlink/rss-canada-ottawa"),
        ("CTV News Ottawa", "https://ottawa.ctvnews.ca/rss/ctv-news-ottawa-1.822136"),
        ("Ottawa Citizen", "https://ottawacitizen.com/feed"),
        ("Ottawa Sun", "https://ottawasun.com/feed"),
    ]

    for name, url in feeds:
        test_rss_simple(name, url)

    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\nIf feeds are working but scraper isn't finding articles,")
    print("the issue might be:")
    print("  1. Articles are older than 24 hours (try --hours 48)")
    print("  2. Date parsing issues")
    print("  3. Network/proxy blocking")
