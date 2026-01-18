#!/usr/bin/env python3
"""
Quick test for a single RSS feed
"""

import feedparser
import sys

def test_feed(url):
    print(f"\nTesting RSS feed: {url}\n")
    print("=" * 70)

    # Parse the feed
    print("Fetching and parsing feed...")
    feed = feedparser.parse(url)

    # Show what feedparser found
    print(f"\nFeed object attributes:")
    print(f"  - bozo: {feed.bozo} (0=valid, 1=has errors)")
    if feed.bozo:
        print(f"  - bozo_exception: {feed.bozo_exception}")

    if hasattr(feed, 'status'):
        print(f"  - HTTP status: {feed.status}")

    if hasattr(feed, 'version'):
        print(f"  - Feed version: {feed.version}")

    if hasattr(feed, 'encoding'):
        print(f"  - Encoding: {feed.encoding}")

    # Check feed info
    print(f"\nFeed info:")
    if hasattr(feed, 'feed'):
        if hasattr(feed.feed, 'title'):
            print(f"  - Title: {feed.feed.title}")
        if hasattr(feed.feed, 'link'):
            print(f"  - Link: {feed.feed.link}")

    # Check entries
    num_entries = len(feed.entries)
    print(f"\nEntries found: {num_entries}")

    if num_entries == 0:
        print("\n❌ NO ENTRIES FOUND!")
        print("\nPossible reasons:")
        print("  1. Network/firewall blocking the feed")
        print("  2. Feed URL is incorrect")
        print("  3. Feed requires authentication")
        print("  4. Feed is temporarily down")
        print("\nTry opening this URL in your browser:")
        print(f"  {url}")
        return False

    # Show first 3 entries
    print(f"\n✅ SUCCESS! Showing first {min(3, num_entries)} entries:\n")
    print("-" * 70)

    for i, entry in enumerate(feed.entries[:3], 1):
        print(f"\n[{i}] {entry.get('title', 'NO TITLE')}")

        if hasattr(entry, 'published'):
            print(f"    Published: {entry.published}")
        elif hasattr(entry, 'updated'):
            print(f"    Updated: {entry.updated}")
        else:
            print(f"    Date: NO DATE FOUND")

        if entry.get('link'):
            print(f"    Link: {entry.link}")

        if entry.get('summary'):
            summary = entry.summary[:100].replace('\n', ' ')
            print(f"    Summary: {summary}...")

    print("\n" + "=" * 70)
    print(f"✅ Feed is working! Found {num_entries} total entries.\n")
    return True


if __name__ == "__main__":
    # Test Ottawa Citizen by default
    url = "https://ottawacitizen.com/feed"

    if len(sys.argv) > 1:
        url = sys.argv[1]

    print(f"""
╔════════════════════════════════════════════════════════════════════╗
║                     RSS Feed Diagnostic Tool                       ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    success = test_feed(url)

    if not success:
        print("\n💡 Troubleshooting tips:")
        print("  1. Check your internet connection")
        print("  2. Try the URL in your browser to verify it works")
        print("  3. Check if you're behind a firewall/proxy")
        print("  4. Try a different RSS feed to test")
        print("\nExample usage:")
        print("  python3 test_single_feed.py https://ottawacitizen.com/feed")
        sys.exit(1)

    sys.exit(0)
