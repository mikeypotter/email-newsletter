# RSS-Based Newsletter (No Selectors Needed!)

## The Easy Way: Use RSS Feeds

Instead of manually finding CSS selectors for each website, you can use RSS feeds. Most news sites provide these, and they're much more reliable.

## Quick Start

### 1. Use the RSS Configuration

```bash
cd src
python main_auto.py --config ../config.rss.yaml
```

That's it! No CSS selectors needed.

### 2. Configuration Format

Instead of this (manual selectors):
```yaml
sources:
  - name: "CBC Ottawa"
    url: "https://www.cbc.ca/news/canada/ottawa"
    selectors:
      article: "div.card"
      title: "h3.headline"
      # ... etc
```

Just use this (RSS feed):
```yaml
sources:
  - name: "CBC Ottawa"
    rss_url: "https://www.cbc.ca/cmlink/rss-canada-ottawa"
```

## How to Find RSS Feeds

### Method 1: Check the Website

Look for an RSS icon (📡) in the footer or header of news websites.

### Method 2: Common Patterns

Try these URL patterns:
- `https://example.com/feed`
- `https://example.com/rss`
- `https://example.com/rss.xml`
- `https://example.com/feed.xml`

### Method 3: View Page Source

1. Go to the news website
2. Right-click → View Page Source
3. Search for `rss` or `feed`
4. Look for `<link type="application/rss+xml">`

### Method 4: Let the Scraper Find It

Just provide the URL without selectors:
```yaml
sources:
  - name: "My News Site"
    url: "https://example.com"
    # The scraper will auto-discover the RSS feed
```

## Ottawa News RSS Feeds (Pre-Configured)

The `config.rss.yaml` already includes these working RSS feeds:

| Source | RSS Feed URL |
|--------|--------------|
| CBC Ottawa | https://www.cbc.ca/cmlink/rss-canada-ottawa |
| CTV News Ottawa | https://ottawa.ctvnews.ca/rss/ctv-news-ottawa-1.822136 |
| Ottawa Citizen | https://ottawacitizen.com/feed |
| Ottawa Sun | https://ottawasun.com/feed |

## Benefits of RSS

✅ **No manual CSS selector hunting**
✅ **More reliable** - RSS structure doesn't change like HTML does
✅ **Faster** - Less processing needed
✅ **Standardized** - Same format across all sites
✅ **Complete data** - Includes title, link, date, description automatically

## Running Both Versions

You have two options:

### Option 1: RSS/Auto Version (Recommended)
```bash
cd src
python main_auto.py --config ../config.rss.yaml
```

### Option 2: Manual Selector Version
```bash
cd src
python main.py --config ../config.yaml
```

## Troubleshooting

### "No articles found"

**Check if RSS feed exists:**
```bash
curl -I https://example.com/feed
# Should return 200 OK
```

**Test the RSS feed:**
Visit the RSS URL in your browser - you should see XML content.

### "Feed parsing failed"

- The URL might not be a valid RSS feed
- Try alternative RSS URLs (`/rss`, `/rss.xml`, `/feed.xml`)
- Use the auto-discovery feature by providing just the base URL

### Auto-Discovery Not Working

Some sites don't advertise their RSS feeds well. In that case:
1. Search Google for "site:example.com rss"
2. Check the site's help/about pages
3. Use a browser extension like "RSS Feed Finder"

## Adding New Sources

### If you know the RSS feed:
```yaml
sources:
  - name: "New Source"
    rss_url: "https://newssite.com/feed"
```

### If you don't know the RSS feed:
```yaml
sources:
  - name: "New Source"
    url: "https://newssite.com"
    # Auto-discovery will try to find it
```

### If RSS doesn't exist:
Fall back to the manual selector version in `config.yaml` and use the original `main.py`.

## Finding More Ottawa News RSS Feeds

Here are some other Ottawa news sources you might want to add:

```yaml
sources:
  - name: "Ottawa Business Journal"
    url: "https://obj.ca/"

  - name: "Ottawa Matters"
    url: "https://www.ottawamatters.com/"

  - name: "Apt613"
    url: "https://apt613.ca/"
```

The scraper will attempt to auto-discover their RSS feeds.

## Best Practices

1. **Use RSS whenever possible** - It's more reliable than scraping HTML
2. **Provide both URL and rss_url** - Falls back gracefully if RSS fails
3. **Test new sources** - Run with just one source first to verify it works
4. **Monitor for changes** - RSS feeds can be deprecated or moved

## Example: Testing a New Source

```bash
# Create a test config with just one source
cat > test_source.yaml << EOF
newsletter:
  name: "Test Newsletter"
  audience: "test audience"

sources:
  - name: "Test Source"
    rss_url: "https://example.com/feed"

newsletter_settings:
  max_articles: 5
  top_stories_count: 3
EOF

# Run it
cd src
python main_auto.py --config ../test_source.yaml --hours 48
```

## Need Help?

1. Check if the RSS feed is valid: https://validator.w3.org/feed/
2. View the RSS feed directly in your browser
3. Use the demo mode for testing: `python demo.py`
