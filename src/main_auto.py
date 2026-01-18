"""
Main Orchestrator - Auto Scraping Version
Uses RSS feeds and automatic extraction (no manual CSS selectors!)
"""

import os
import sys
import yaml
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from auto_scraper import AutoScraper
from ai_analyzer import NewsAnalyzer
from newsletter_formatter import NewsletterFormatter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Morning Brew style guide
MORNING_BREW_STYLE = """
1. The Tone: "The Smart Friend"
   - Conversational & Witty: Use slang, internet culture references, and puns
   - Professional enough to read at work, but casual enough to feel like a break
   - Self-Aware & Meta: Break the fourth wall, make jokes about boring topics
   - Optimistic but Realistic: Keep it punchy and forward-looking

2. Structural Signatures
   - "What's Brewing": Bulleted summary at the top
   - Section Headers: Use clear headers like "Deep Dive," "Grab Bag"
   - Short paragraphs: 2-3 sentences max
   - Aggressive use of bullet points

3. Writing Tactics
   - The "So What?" Factor: Explain why it matters immediately
   - Jargon Translation: Explain complex terms in plain English with metaphors
   - Brevity: Keep it scannable and quick to read
"""


class NewsletterGenerator:
    """Main orchestrator for newsletter generation using auto-scraping"""

    def __init__(self, config_path: str = "config.rss.yaml"):
        """
        Initialize the newsletter generator

        Args:
            config_path: Path to configuration file
        """
        # Load environment variables
        load_dotenv()

        # Load configuration
        self.config = self._load_config(config_path)

        # Initialize components
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.scraper = AutoScraper(self.config['sources'])
        self.analyzer = NewsAnalyzer(
            api_key=api_key,
            model=self.config.get('ai', {}).get('model', 'claude-sonnet-4-5-20250929')
        )
        self.formatter = NewsletterFormatter()

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file {config_path} not found. "
                "Please create it based on config.rss.yaml"
            )

        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def generate(self, hours_ago: int = 24, output_dir: str = "output") -> str:
        """
        Generate the newsletter

        Args:
            hours_ago: Include articles from the last N hours
            output_dir: Directory to save the newsletter

        Returns:
            Path to the generated newsletter file
        """
        logger.info("=" * 60)
        logger.info("Starting AUTO newsletter generation (no selectors needed!)")
        logger.info("=" * 60)

        # Step 1: Scrape articles using RSS/auto-detection
        logger.info(f"\n[Step 1/4] Auto-scraping articles from the last {hours_ago} hours...")
        logger.info("Using RSS feeds and automatic content detection...")
        articles = self.scraper.scrape_all_sources(hours_ago=hours_ago)

        if not articles:
            logger.error("No articles found! Check your RSS feed URLs or network connection.")
            sys.exit(1)

        logger.info(f"✓ Found {len(articles)} articles total")

        # Step 2: Analyze and select top stories
        logger.info("\n[Step 2/4] Analyzing articles with AI...")
        newsletter_config = self.config.get('newsletter', {})
        newsletter_settings = self.config.get('newsletter_settings', {})

        audience = newsletter_config.get('audience', 'general readers')
        top_count = newsletter_settings.get('top_stories_count', 5)

        # Limit articles if configured
        max_articles = newsletter_settings.get('max_articles', len(articles))
        articles = articles[:max_articles]

        analysis = self.analyzer.analyze_and_select_top_stories(
            articles=articles,
            audience=audience,
            top_count=top_count
        )

        logger.info(f"✓ Identified {len(analysis.get('top_stories', []))} top stories")
        logger.info(f"  Themes: {', '.join(analysis.get('themes', []))}")

        # Step 3: Generate newsletter content
        logger.info("\n[Step 3/4] Generating newsletter content...")
        newsletter_name = newsletter_config.get('name', 'Daily Newsletter')

        content = self.analyzer.generate_newsletter_content(
            analysis=analysis,
            newsletter_name=newsletter_name,
            style_guide=MORNING_BREW_STYLE
        )

        logger.info("✓ Newsletter content generated")

        # Step 4: Format and save
        logger.info("\n[Step 4/4] Formatting and saving newsletter...")

        formatted_newsletter = self.formatter.format_newsletter(
            content=content,
            newsletter_name=newsletter_name
        )

        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(output_dir) / f"newsletter_{timestamp}.html"

        self.formatter.save_newsletter(formatted_newsletter, str(output_path))

        logger.info(f"✓ Newsletter saved to: {output_path}")

        # Extract and log subject line
        subject = self.formatter.extract_subject_line(content)
        logger.info(f"\n📧 Subject Line: {subject}")

        logger.info("\n" + "=" * 60)
        logger.info("Newsletter generation complete!")
        logger.info("=" * 60)

        return str(output_path)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate an AI-powered newsletter using RSS feeds (no manual selectors!)'
    )
    parser.add_argument(
        '--config',
        default='config.rss.yaml',
        help='Path to configuration file (default: config.rss.yaml)'
    )
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Include articles from the last N hours (default: 24)'
    )
    parser.add_argument(
        '--output',
        default='output',
        help='Output directory for newsletter (default: output)'
    )

    args = parser.parse_args()

    try:
        generator = NewsletterGenerator(config_path=args.config)
        newsletter_path = generator.generate(
            hours_ago=args.hours,
            output_dir=args.output
        )
        print(f"\n✅ Success! Newsletter saved to: {newsletter_path}")
        return 0

    except Exception as e:
        logger.error(f"\n❌ Error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
