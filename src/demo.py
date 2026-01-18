"""
Demo mode - Generate newsletter with sample Ottawa news data
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from ai_analyzer import NewsAnalyzer
from newsletter_formatter import NewsletterFormatter

# Sample Ottawa news articles
SAMPLE_ARTICLES = [
    {
        'title': 'Ottawa Council Approves New LRT Extension Plans',
        'source': 'CBC Ottawa',
        'link': 'https://www.cbc.ca/news/canada/ottawa/lrt-extension-approved',
        'description': 'City council voted 15-9 in favor of extending the LRT system to Barrhaven and Kanata, with construction expected to begin in 2027.',
        'date': '2026-01-18T09:30:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Record-Breaking Cold Snap Hits Ottawa This Weekend',
        'source': 'CTV News Ottawa',
        'link': 'https://www.ctvnews.ca/ottawa/cold-weather',
        'description': 'Environment Canada warns of temperatures dropping to -35°C with wind chill, advising residents to stay indoors.',
        'date': '2026-01-18T08:15:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Senators Rally Past Maple Leafs in Overtime Thriller',
        'source': 'Ottawa Citizen',
        'link': 'https://ottawacitizen.com/senators-win',
        'description': 'Brady Tkachuk scored the game-winner in OT as the Senators defeated Toronto 4-3 at Canadian Tire Centre.',
        'date': '2026-01-17T22:45:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'New Tech Hub Opening in Kanata Creates 500 Jobs',
        'source': 'Ottawa Sun',
        'link': 'https://ottawasun.com/tech-hub-jobs',
        'description': 'Silicon Valley tech giant announces plans to open a major development center in Kanata, bringing hundreds of high-paying jobs to the region.',
        'date': '2026-01-18T10:00:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'ByWard Market Vendors Report Strong Holiday Sales',
        'source': 'CBC Ottawa',
        'link': 'https://www.cbc.ca/news/canada/ottawa/byward-market-sales',
        'description': 'Local merchants say this was the best holiday season in five years, crediting increased foot traffic and tourism.',
        'date': '2026-01-18T07:30:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Ottawa University Researchers Develop New Ice-Resistant Road Surface',
        'source': 'CTV News Ottawa',
        'link': 'https://www.ctvnews.ca/ottawa/research-roads',
        'description': 'U of O engineers unveil innovative road coating that could reduce ice formation by 70%, potentially saving millions in winter maintenance.',
        'date': '2026-01-17T16:20:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Rideau Canal Skateway Opens Early This Year',
        'source': 'Ottawa Citizen',
        'link': 'https://ottawacitizen.com/skateway-opens',
        'description': 'The world-famous skating rink opened two weeks earlier than usual thanks to sustained cold temperatures.',
        'date': '2026-01-18T06:00:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Ottawa Food Bank Reports 40% Increase in Demand',
        'source': 'CBC Ottawa',
        'link': 'https://www.cbc.ca/news/canada/ottawa/food-bank-demand',
        'description': 'Rising cost of living pushes more Ottawa families to seek assistance, with the food bank serving record numbers.',
        'date': '2026-01-17T14:30:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Construction Begins on New Civic Hospital Campus',
        'source': 'Ottawa Sun',
        'link': 'https://ottawasun.com/civic-hospital',
        'description': 'Ground broken on $2.8 billion replacement facility at Tunney\'s Pasture, expected to open in 2032.',
        'date': '2026-01-18T11:00:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'OC Transpo Announces New Express Routes for Suburbs',
        'source': 'CTV News Ottawa',
        'link': 'https://www.ctvnews.ca/ottawa/octranspo-routes',
        'description': 'Transit commission approves five new express bus routes connecting outer neighborhoods to downtown core.',
        'date': '2026-01-17T15:45:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Parliament Hill Security Upgrades to Cost $500M',
        'source': 'Ottawa Citizen',
        'link': 'https://ottawacitizen.com/parliament-security',
        'description': 'Federal government announces massive security overhaul following comprehensive review of Parliamentary precinct.',
        'date': '2026-01-18T09:00:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Local Brewery Wins International Award',
        'source': 'Reddit Ottawa',
        'link': 'https://reddit.com/r/ottawa',
        'description': 'Hintonburg-based Beyond the Pale takes gold at World Beer Cup for their signature IPA.',
        'date': '2026-01-17T19:30:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Ottawa Housing Prices Drop 3% in December',
        'source': 'Ottawa Sun',
        'link': 'https://ottawasun.com/housing-prices',
        'description': 'Real estate board reports first price decline in eight months as inventory increases and buyer demand softens.',
        'date': '2026-01-17T13:00:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Winterlude Festival Announces Star-Studded Lineup',
        'source': 'CBC Ottawa',
        'link': 'https://www.cbc.ca/news/canada/ottawa/winterlude-2026',
        'description': 'Annual winter festival to feature major Canadian artists and expanded ice sculpture competition.',
        'date': '2026-01-18T08:00:00',
        'scraped_at': datetime.now().isoformat()
    },
    {
        'title': 'Ottawa Traffic Cameras Catch Record Number of Speeders',
        'source': 'CTV News Ottawa',
        'link': 'https://www.ctvnews.ca/ottawa/speed-cameras',
        'description': 'Automated speed enforcement program issued 125,000 tickets in 2025, generating $12M in revenue.',
        'date': '2026-01-17T17:00:00',
        'scraped_at': datetime.now().isoformat()
    }
]

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


def generate_demo_newsletter():
    """Generate a demo newsletter with sample Ottawa news"""

    # Load environment variables
    load_dotenv()

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    print("=" * 60)
    print("DEMO MODE: Generating Ottawa Daily Digest")
    print("=" * 60)
    print(f"\n✓ Using {len(SAMPLE_ARTICLES)} sample Ottawa news articles")

    # Initialize components
    analyzer = NewsAnalyzer(api_key=api_key)
    formatter = NewsletterFormatter()

    # Step 1: Analyze articles
    print("\n[Step 1/3] Analyzing articles with AI...")
    analysis = analyzer.analyze_and_select_top_stories(
        articles=SAMPLE_ARTICLES,
        audience="Ottawa residents, local business owners, and community members",
        top_count=5
    )

    print(f"✓ Identified {len(analysis.get('top_stories', []))} top stories")
    print(f"  Themes: {', '.join(analysis.get('themes', []))}")

    # Step 2: Generate content
    print("\n[Step 2/3] Generating newsletter content in Morning Brew style...")
    content = analyzer.generate_newsletter_content(
        analysis=analysis,
        newsletter_name="Ottawa Daily Digest",
        style_guide=MORNING_BREW_STYLE
    )

    print("✓ Newsletter content generated")

    # Step 3: Format and save
    print("\n[Step 3/3] Formatting and saving newsletter...")
    formatted_newsletter = formatter.format_newsletter(
        content=content,
        newsletter_name="Ottawa Daily Digest"
    )

    # Create output directory
    Path("../output").mkdir(parents=True, exist_ok=True)

    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"../output/ottawa_newsletter_demo_{timestamp}.html"

    formatter.save_newsletter(formatted_newsletter, output_path)

    print(f"✓ Newsletter saved to: {output_path}")

    # Extract subject line
    subject = formatter.extract_subject_line(content)
    print(f"\n📧 Subject Line: {subject}")

    print("\n" + "=" * 60)
    print("Demo newsletter generation complete!")
    print("=" * 60)
    print(f"\nOpen the file in your browser to view:")
    print(f"  {output_path}")

    return output_path


if __name__ == "__main__":
    try:
        generate_demo_newsletter()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
