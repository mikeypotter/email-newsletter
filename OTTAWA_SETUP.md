# Ottawa Daily Digest - Setup Guide

Your newsletter generator is configured to scrape Ottawa-focused news from five local sources.

## Configured Sources

1. **CTV News Ottawa** - https://www.ctvnews.ca/ottawa/
2. **CBC Ottawa** - https://www.cbc.ca/news/canada/ottawa
3. **Reddit r/ottawa** - https://www.reddit.com/r/ottawa/
4. **Ottawa Citizen** - https://ottawacitizen.com/category/news/
5. **Ottawa Sun** - https://ottawasun.com

## Newsletter Details

**Name**: Ottawa Daily Digest
**Target Audience**: Ottawa residents, local business owners, and community members interested in local news and events
**Style**: Morning Brew (conversational, witty, engaging)
**Top Stories**: 5 featured stories per newsletter
**Max Articles Analyzed**: 20

## How to Run

### Option 1: Regular Mode (Live Scraping)

Run this in your own environment where you have unrestricted internet access:

```bash
cd src
python main.py --config ../config.yaml
```

This will:
- Scrape all 5 Ottawa news sources
- Find articles from the last 24 hours
- Use AI to select the top 5 stories
- Generate a complete newsletter in Morning Brew style
- Save as HTML in the `output/` directory

### Option 2: Demo Mode (Sample Data)

For testing without live scraping:

```bash
cd src
python demo.py
```

This uses 15 pre-loaded Ottawa news samples including:
- LRT extension updates
- Weather alerts
- Senators hockey
- Local tech jobs
- ByWard Market news
- And more...

## Prerequisites

1. **Python 3.8+** installed
2. **Dependencies** installed: `pip install -r requirements.txt`
3. **Anthropic API Key** with credits in your `.env` file
4. **Internet connection** for live scraping mode

## Configuration

The newsletter is configured in `config.yaml`:

```yaml
newsletter:
  name: "Ottawa Daily Digest"
  audience: "Ottawa residents, local business owners, and community members"

newsletter_settings:
  max_articles: 20
  top_stories_count: 5

ai:
  model: "claude-sonnet-4-5-20250929"
  max_tokens: 4000
  temperature: 0.7
```

## Customization

### Change the Number of Stories

Edit `config.yaml`:
```yaml
newsletter_settings:
  top_stories_count: 7  # Show 7 stories instead of 5
```

### Add More Sources

Add any Ottawa news site to `config.yaml`:
```yaml
sources:
  - name: "Your Source"
    url: "https://example.com"
    selectors:
      article: "article"
      title: "h2"
      link: "a"
      date: "time"
```

### Adjust Time Window

Include articles from the last 48 hours instead of 24:
```bash
python main.py --config ../config.yaml --hours 48
```

### Change the Tone

Edit the `MORNING_BREW_STYLE` in `src/main.py` to adjust the writing style.

## Output

The newsletter will be saved as:
```
output/newsletter_YYYYMMDD_HHMMSS.html
```

Open it in any web browser to view the beautifully formatted newsletter with:
- Ottawa Daily Digest header
- "What's Brewing" summary section
- Top 5 Ottawa stories with context
- Links to original articles
- Mobile-responsive design

## Next Steps

1. **Add credits** to your Anthropic account at https://console.anthropic.com/settings/plans
2. **Run the generator** using either regular or demo mode
3. **Review the output** and adjust configuration as needed
4. **Schedule it** (optional) - Set up a cron job to run daily:
   ```bash
   0 6 * * * cd /path/to/email-newsletter/src && python main.py
   ```

## Troubleshooting

### "No articles found"
- CSS selectors may need updating (websites change their HTML)
- Check network connectivity
- Try the demo mode first to verify AI setup

### "Credit balance too low"
- Add credits at https://console.anthropic.com/settings/plans
- Check your API key is correct in `.env`

### Network/Proxy Errors
- Some environments block external HTTPS (like the current one)
- Run in your local environment instead
- Use demo mode for testing

## Need Help?

Open an issue on GitHub or check the main README.md for more details.
