"""
AI Analyzer Module
Uses Claude AI to analyze news articles and identify top stories
"""

import anthropic
import json
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsAnalyzer:
    """Analyzes news articles using Claude AI"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def analyze_and_select_top_stories(
        self,
        articles: List[Dict],
        audience: str,
        top_count: int = 5
    ) -> Dict:
        """
        Analyze articles and select the most relevant top stories

        Args:
            articles: List of scraped articles
            audience: Target audience description
            top_count: Number of top stories to select

        Returns:
            Dictionary containing top stories and analysis
        """
        logger.info(f"Analyzing {len(articles)} articles with Claude AI...")

        # Prepare article summaries for AI
        article_summaries = []
        for i, article in enumerate(articles):
            summary = f"{i+1}. [{article['source']}] {article['title']}"
            if article.get('description'):
                summary += f" - {article['description'][:150]}"
            article_summaries.append(summary)

        articles_text = "\n".join(article_summaries)

        prompt = f"""You are a newsletter editor analyzing news articles for an audience of {audience}.

Here are today's articles:

{articles_text}

Your task:
1. Identify the {top_count} most newsworthy and engaging stories that would appeal to this audience
2. Group related stories into thematic categories
3. For each selected story, explain why it's important and what the audience should know

Respond in JSON format:
{{
    "top_stories": [
        {{
            "article_numbers": [1, 5],  // Reference numbers from the list above
            "category": "AI & Technology",
            "headline": "Catchy headline summarizing the story/stories",
            "why_it_matters": "Brief explanation of significance",
            "key_points": ["Point 1", "Point 2"]
        }}
    ],
    "themes": ["Theme 1", "Theme 2", "Theme 3"],
    "overall_narrative": "What's the bigger picture today?"
}}

Focus on stories that are:
- Timely and relevant
- Impact the audience's work or interests
- Have interesting angles or unexpected developments
- Can be made engaging with the right framing"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract JSON from response
            response_text = response.content[0].text

            # Try to parse JSON from response
            # Sometimes the model wraps JSON in markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            analysis = json.loads(response_text)

            # Map article numbers back to actual articles
            for story in analysis.get('top_stories', []):
                story['articles'] = [
                    articles[num - 1] for num in story.get('article_numbers', [])
                    if 0 < num <= len(articles)
                ]

            logger.info(f"AI identified {len(analysis.get('top_stories', []))} top stories")
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing articles: {str(e)}")
            # Return a basic fallback structure
            return {
                "top_stories": [
                    {
                        "article_numbers": [i+1],
                        "category": article['source'],
                        "headline": article['title'],
                        "why_it_matters": "Breaking news",
                        "key_points": [],
                        "articles": [article]
                    }
                    for i, article in enumerate(articles[:top_count])
                ],
                "themes": ["Technology", "Business"],
                "overall_narrative": "Today's top stories from the tech world."
            }

    def generate_newsletter_content(
        self,
        analysis: Dict,
        newsletter_name: str,
        style_guide: str
    ) -> str:
        """
        Generate the full newsletter content in Morning Brew style

        Args:
            analysis: Analysis from analyze_and_select_top_stories
            newsletter_name: Name of the newsletter
            style_guide: Style guidelines to follow

        Returns:
            Newsletter content as HTML
        """
        logger.info("Generating newsletter content with Claude AI...")

        # Prepare the stories for the prompt
        stories_summary = []
        for i, story in enumerate(analysis.get('top_stories', [])):
            story_text = f"\nStory {i+1}: {story.get('headline', 'Untitled')}\n"
            story_text += f"Category: {story.get('category', 'General')}\n"
            story_text += f"Why it matters: {story.get('why_it_matters', '')}\n"
            story_text += f"Key points: {', '.join(story.get('key_points', []))}\n"

            # Add source articles
            for article in story.get('articles', []):
                story_text += f"  - [{article['source']}] {article['title']}\n"
                if article.get('link'):
                    story_text += f"    Link: {article['link']}\n"

            stories_summary.append(story_text)

        stories_text = "\n".join(stories_summary)
        themes = ", ".join(analysis.get('themes', []))
        narrative = analysis.get('overall_narrative', '')

        prompt = f"""You are the editor of "{newsletter_name}", a newsletter written in the style of Morning Brew.

STYLE GUIDE:
{style_guide}

TODAY'S CONTEXT:
Overall narrative: {narrative}
Key themes: {themes}

STORIES TO COVER:
{stories_text}

Write a complete newsletter following the Morning Brew style. Include:

1. A catchy subject line
2. An opening "What's Brewing" section with bullet points
3. 3-5 main stories written in the Morning Brew tone:
   - Conversational and witty
   - Start with the hook, explain why it matters
   - Use metaphors to explain complex concepts
   - Keep paragraphs to 2-3 sentences max
   - Include relevant links
4. A "Grab Bag" section with 2-3 quick hits
5. A fun closing

Use HTML formatting for the newsletter:
- <h1> for the newsletter title
- <h2> for major sections
- <h3> for story headlines
- <p> for paragraphs
- <ul> and <li> for lists
- <a> for links
- <strong> for emphasis

Make it engaging, informative, and fun to read. Remember: you're the smart friend explaining the news over coffee."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.8,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            newsletter_html = response.content[0].text

            # If the response is wrapped in markdown code blocks, extract it
            if "```html" in newsletter_html:
                html_start = newsletter_html.find("```html") + 7
                html_end = newsletter_html.find("```", html_start)
                newsletter_html = newsletter_html[html_start:html_end].strip()
            elif "```" in newsletter_html:
                html_start = newsletter_html.find("```") + 3
                html_end = newsletter_html.find("```", html_start)
                newsletter_html = newsletter_html[html_start:html_end].strip()

            logger.info("Newsletter content generated successfully")
            return newsletter_html

        except Exception as e:
            logger.error(f"Error generating newsletter: {str(e)}")
            raise
