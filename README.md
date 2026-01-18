# AI-Powered Newsletter Generator

An intelligent newsletter generation application that scrapes news from specified websites, uses AI to identify the most engaging stories, and creates newsletters in the style of Morning Brew.

## Features

- 🌐 **Web Scraping**: Automatically visits and scrapes news from configurable websites
- 🤖 **AI-Powered Analysis**: Uses Claude AI to identify the most newsworthy and engaging topics
- 📧 **Morning Brew Style**: Generates newsletters with the conversational, witty tone of Morning Brew
- ⚙️ **Highly Configurable**: Easy YAML configuration for news sources and settings
- 📱 **Responsive HTML**: Creates mobile-friendly newsletters with clean styling

## How It Works

1. **Scrape**: Visits configured news websites and extracts articles from the last 24 hours
2. **Analyze**: Sends all articles to Claude AI to identify the most relevant stories for your audience
3. **Generate**: Creates a complete newsletter with AI-written content in Morning Brew style
4. **Output**: Saves a beautifully formatted HTML newsletter ready to send

## Morning Brew Style

The generator follows these key principles:

- **The Smart Friend Tone**: Conversational, witty, and professional
- **Scannable Structure**: Short paragraphs, bullet points, clear sections
- **Explain Why It Matters**: Every story includes context and significance
- **Jargon-Free**: Complex topics explained with metaphors and plain language

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/email-newsletter.git
cd email-newsletter

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create your configuration files:

```bash
# Copy the example files
cp .env.example .env
cp config.example.yaml config.yaml

# Edit .env and add your Anthropic API key
nano .env
```

Add your Anthropic API key to `.env`:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Configure News Sources

Edit `config.yaml` to add your preferred news sources. The example includes TechCrunch, Hacker News, and The Verge, but you can add any website.

```yaml
sources:
  - name: "Your News Source"
    url: "https://example.com"
    selectors:
      article: "article"          # CSS selector for article containers
      title: "h2"                 # CSS selector for titles
      link: "a"                   # CSS selector for links
      date: "time"                # CSS selector for dates (optional)
```

### 4. Run

```bash
cd src
python main.py
```

The newsletter will be saved to the `output/` directory.

## Usage

### Basic Usage

```bash
cd src
python main.py
```

### Advanced Options

```bash
# Use a custom config file
python main.py --config /path/to/config.yaml

# Include articles from the last 48 hours
python main.py --hours 48

# Save to a custom directory
python main.py --output /path/to/output
```

### Command Line Options

- `--config`: Path to configuration file (default: config.yaml)
- `--hours`: Include articles from the last N hours (default: 24)
- `--output`: Output directory for newsletter (default: output)

## Configuration

### Newsletter Settings

Edit `config.yaml` to customize your newsletter:

```yaml
newsletter:
  name: "Your Newsletter Name"
  audience: "tech professionals, startup founders, and business leaders"

newsletter_settings:
  max_articles: 15           # Maximum articles to analyze
  top_stories_count: 5       # Number of top stories to feature
  include_market_data: false

ai:
  model: "claude-sonnet-4-5-20250929"
  max_tokens: 4000
  temperature: 0.7
```

### Adding News Sources

For each source, you need to specify CSS selectors to extract content. Use your browser's developer tools to find the right selectors:

1. Open the website in your browser
2. Right-click on an article title → Inspect
3. Find the CSS selector for the element
4. Add it to your config

Example:

```yaml
sources:
  - name: "Example News"
    url: "https://news.example.com"
    selectors:
      article: "div.article-item"
      title: "h3.article-title"
      link: "a.article-link"
      date: "span.publish-date"
      description: "p.summary"  # Optional
```

## Project Structure

```
email-newsletter/
├── README.md
├── requirements.txt
├── .env.example
├── config.example.yaml
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py                    # Main orchestrator
│   ├── scraper.py                 # Web scraping module
│   ├── ai_analyzer.py             # AI analysis and generation
│   └── newsletter_formatter.py    # HTML formatting
└── output/                        # Generated newsletters
```

## Requirements

- Python 3.8+
- Anthropic API key (get one at https://console.anthropic.com/)
- Internet connection for scraping and AI

## Example Output

The generator creates a complete HTML newsletter with:

- **Header**: Newsletter name and date
- **What's Brewing**: Quick summary of what's covered
- **Top Stories**: 3-5 main stories with engaging headlines
- **Context**: Why each story matters to your audience
- **Grab Bag**: Quick hits and additional news
- **Clean Design**: Mobile-responsive with Morning Brew-inspired styling

## Customization

### Changing the Style

Edit the `MORNING_BREW_STYLE` constant in `src/main.py` to adjust the writing style and tone.

### Custom AI Prompts

Modify the prompts in `src/ai_analyzer.py` to change how AI analyzes and writes the content.

### HTML Styling

Edit the CSS in `src/newsletter_formatter.py` to customize the newsletter appearance.

## Troubleshooting

### "No articles found"

- Check that your news source URLs are correct
- Verify CSS selectors are accurate (websites change their HTML)
- Try increasing the `--hours` parameter

### API Errors

- Verify your `ANTHROPIC_API_KEY` is set correctly in `.env`
- Check you have sufficient API credits
- Ensure you're using a supported model

### Scraping Issues

- Some websites block scrapers - you may need to respect robots.txt
- Consider adding delays between requests
- Use a custom User-Agent if needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this for your own newsletters!

## Acknowledgments

- Inspired by [Morning Brew](https://www.morningbrew.com/)
- Powered by [Anthropic's Claude AI](https://www.anthropic.com/)

## Support

For issues and questions, please open an issue on GitHub.
