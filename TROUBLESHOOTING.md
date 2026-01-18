# Troubleshooting: "No Articles Found"

If you're getting "Found 0 articles" when scraping, here's how to debug it.

## Quick Fixes

### 1. **Increase the Time Window**

By default, the scraper only includes articles from the last 24 hours. If news sources haven't published recently, try:

```bash
# Get articles from the last 48 hours
cd src
python3 main_auto.py --config ../config.rss.yaml --hours 48

# Or even longer
python3 main_auto.py --config ../config.rss.yaml --hours 72
```

### 2. **Enable Debug Mode**

See exactly what's happening:

```bash
cd src
python3 main_auto.py --config ../config.rss.yaml --hours 48 --debug
```

This will show you:
- How many entries are in each RSS feed
- How many articles are being filtered out as too old
- Any errors that occur

### 3. **Test RSS Feeds Directly**

Run the debug script to check if RSS feeds are working:

```bash
cd src
python3 debug_rss.py
```

This will:
- Test connectivity to each RSS feed
- Show you the actual articles available
- Display publication dates and ages
- Identify any issues with the feeds

## Common Issues

### Issue 1: Articles Are Too Old

**Symptom:**
```
INFO:auto_scraper:Found 0 articles from CBC Ottawa
WARNING:auto_scraper:All 20 articles from CBC Ottawa were older than 2026-01-17 22:00:00
WARNING:auto_scraper:Try increasing --hours parameter
```

**Solution:**
```bash
python3 main_auto.py --config ../config.rss.yaml --hours 72
```

### Issue 2: RSS Feed Not Working

**Symptom:**
```
ERROR:auto_scraper:RSS parsing failed for CBC Ottawa: ...
```

**Solutions:**

1. **Test the RSS URL directly** in your browser:
   - Visit: https://www.cbc.ca/cmlink/rss-canada-ottawa
   - You should see XML content
   - If you get an error, the RSS feed URL might be wrong

2. **Check for network issues:**
   ```bash
   curl -I https://www.cbc.ca/cmlink/rss-canada-ottawa
   ```
   Should return `200 OK`

3. **Try alternative RSS URLs:**
   - Sometimes RSS feeds move or change
   - Google: "site:cbc.ca ottawa rss"
   - Check the website footer for RSS links

### Issue 3: Dependencies Not Installed

**Symptom:**
```
ModuleNotFoundError: No module named 'feedparser'
```

**Solution:**
```bash
cd /path/to/email-newsletter
pip3 install -r requirements.txt
```

Or with virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
```

### Issue 4: Wrong Config File

**Symptom:**
```
FileNotFoundError: Configuration file config.rss.yaml not found
```

**Solution:**
Make sure you're using the right config file:

```bash
# For RSS version (recommended)
python3 main_auto.py --config ../config.rss.yaml

# For manual selector version
python3 main.py --config ../config.yaml
```

## Debugging Steps

### Step 1: Test RSS Feeds

```bash
cd src
python3 test_rss_simple.py
```

Expected output:
```
Testing: CBC Ottawa
✓ HTTP Status: 200
✓ Found 20 articles in feed

[1] Some Article Title
    Published: Sat, 18 Jan 2026 10:30:00 EST
```

### Step 2: Run with Debug Mode

```bash
python3 main_auto.py --config ../config.rss.yaml --hours 48 --debug
```

Look for:
- `Total entries in feed: X` - Shows RSS feed has articles
- `Filtered out X old articles` - Shows filtering is working
- Any `ERROR` or `WARNING` messages

### Step 3: Check Article Ages

If you see:
```
Filtered out 15 old articles (older than cutoff)
Kept 0 recent articles
```

This means all articles are older than your time window. Increase `--hours`.

### Step 4: Test Individual Feed

Edit `config.rss.yaml` to comment out all sources except one:

```yaml
sources:
  - name: "CBC Ottawa"
    rss_url: "https://www.cbc.ca/cmlink/rss-canada-ottawa"

  # - name: "CTV News Ottawa"
  #   rss_url: "https://ottawa.ctvnews.ca/rss/ctv-news-ottawa-1.822136"
```

Then run again. This helps isolate which feed has issues.

## Manual Verification

### Check RSS Feed in Browser

1. Open: https://www.cbc.ca/cmlink/rss-canada-ottawa
2. You should see XML with `<item>` tags
3. Look at `<pubDate>` fields - are they recent?

### Check RSS Feed with curl

```bash
curl -s "https://www.cbc.ca/cmlink/rss-canada-ottawa" | grep -A 5 "<item>"
```

Should show article items with titles and dates.

## Alternative: Use Demo Mode

If RSS feeds aren't working, use the demo mode with sample data:

```bash
cd src
python3 demo.py
```

This uses pre-loaded Ottawa news to test the AI generation without scraping.

## Getting Help

If still stuck, run this diagnostic and share the output:

```bash
cd src
python3 main_auto.py --config ../config.rss.yaml --hours 72 --debug 2>&1 | tee debug_output.txt
```

This saves all debug info to `debug_output.txt` for troubleshooting.

## Quick Reference

| Problem | Solution |
|---------|----------|
| "Found 0 articles" | Add `--hours 48` or `--hours 72` |
| ModuleNotFoundError | Run `pip3 install -r requirements.txt` |
| All articles too old | Increase `--hours` parameter |
| RSS feed error | Test with `python3 debug_rss.py` |
| Want to see details | Add `--debug` flag |
| Testing without network | Use `python3 demo.py` |

## Prevention Tips

1. **Schedule during active hours** - Run in morning when news is fresh
2. **Use generous time windows** - `--hours 48` is safer than `--hours 24`
3. **Monitor RSS feeds** - Occasionally check they haven't moved
4. **Test before automating** - Run manually first to verify sources work

## Still Not Working?

The RSS feeds might have issues. Try the manual selector version:

```bash
# Use the manual config with CSS selectors
python3 main.py --config ../config.yaml
```

See README.md for how to find CSS selectors for each website.
