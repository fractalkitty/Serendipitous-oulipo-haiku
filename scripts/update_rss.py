#!/usr/bin/env python3
"""
Generate rss.xml with same format as Node.js version
Run from scripts/ directory
"""

import json
import os
from datetime import datetime, timedelta

def load_poems():
    """Load poems from JSON file"""
    poems_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'poems.json')
    try:
        with open(poems_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generate_rss_xml(poems, base_url="https://sohaiku.art"):
    """Generate RSS feed XML in the exact same format as Node.js version"""
    # Filter poems from last 30 days - use UTC timezone
    from datetime import timezone
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    recent_poems = [
        poem for poem in poems
        if datetime.fromisoformat(poem['date'].replace('Z', '+00:00')) >= thirty_days_ago
    ]

    # Reference date: January 1, 2022 (same as Node.js)
    reference_date = int(datetime(2022, 1, 1).timestamp())

    rss_items = []
    for poem in recent_poems:
        poem_date_seconds = int(datetime.fromisoformat(poem['date'].replace('Z', '+00:00')).timestamp())
        seconds_since_reference = poem_date_seconds - reference_date
        content_snippet = poem['content'][:20].replace(' ', '').replace('\n', '').lower()
        unique_guid = f"{seconds_since_reference}-{content_snippet}"

        # Format date for RSS
        pub_date = datetime.fromisoformat(poem['date'].replace('Z', '+00:00')).strftime('%a, %d %b %Y %H:%M:%S GMT')

        # Get title and description (match Node.js exactly)
        title = poem['content'].split('\n')[0]
        description = poem['content'].replace('\n', '&lt;br&gt;')

        rss_items.append(f'''    <item>
      <title>{title}</title>
      <description>{description}</description>
      <pubDate>{pub_date}</pubDate>
      <category>haiku</category>
      <category>oulipo</category>
      <category>soHaiku</category>
      <category>botPoet</category>
      <guid>{unique_guid}</guid>
      <link>{base_url}/poems/{unique_guid}</link>
    </item>''')

    rss_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Serendipitous Oulipo Haiku</title>
    <description>Generated haikus based on the serendipitous-oulipo-haiku project</description>
    <link>{base_url}</link>
    <language>en</language>
    <category>poetry</category>
    <category>haiku</category>
    <category>oulipo</category>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
{chr(10).join(rss_items)}
  </channel>
</rss>'''

    return rss_content

def main():
    """Generate rss.xml"""
    # Load poems
    poems = load_poems()

    if not poems:
        print("No poems found. Run the haiku generator first.")
        return

    # Generate RSS feed (same format as Node.js)
    rss_content = generate_rss_xml(poems)

    # Save to parent directory (same level as scripts/)
    rss_path = os.path.join(os.path.dirname(__file__), '..', 'rss.xml')
    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write(rss_content)

    # Filter for recent poems count
    from datetime import timezone
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    recent_count = len([
        poem for poem in poems
        if datetime.fromisoformat(poem['date'].replace('Z', '+00:00')) >= thirty_days_ago
    ])

    print(f"Generated rss.xml with {recent_count} recent poems (last 30 days)")

if __name__ == "__main__":
    main()