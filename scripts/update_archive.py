#!/usr/bin/env python3
"""
Generate archive.html with lazy loading for 25k+ poems
Run from scripts/ directory
"""

import json
import os
from datetime import datetime

def load_poems():
    """Load poems from JSON file"""
    poems_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'poems.json')
    try:
        with open(poems_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generate_archive_html(poems):
    """Generate archive.html with lazy loading (first 10 poems, then load more via JS)"""
    # Split poems into pages of 10
    limit = 10
    first_page_poems = poems[:limit]
    has_next_page = len(poems) > limit

    # Generate poems HTML for first page
    poems_html = ""
    for poem in first_page_poems:
        poem_date = datetime.fromisoformat(poem['date'].replace('Z', '+00:00'))
        formatted_date = poem_date.strftime('%B %d, %Y, %I:%M %p')

        poems_html += f'''
                            <div class="poem">
                                <pre>{poem['content']}</pre>
                                <div class="date">
                                    {formatted_date}
                                </div>
                                <a href="https://fed.brid.gy/" class="webmention-link">Bridgy Fed</a>
                            </div>
                        '''

    html_template = f'''<html>
                <head>
                    <title>Serendipitous Oulipo Haiku Archive</title>

                    <style>
                        /* Your existing styles here */
                        body {{
                            font-family: sans-serif;
                            max-width: 800px;
                            margin: 100px;
                            padding: 20px;
                            line-height: 1.6;
                            background:  #d4cdc5;
                        }}
                        .poem {{
                            margin: 2em 0;
                            padding: 1.5em;
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            background: white;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }}
                        .date {{
                            color: #666;
                            font-size: 0.9em;
                            margin-top: 1em;
                            border-top: 1px solid #eee;
                            padding-top: 0.5em;
                        }}
                        pre {{
                            white-space: pre-wrap;
                            font-family: inherit;
                            margin: 0;
                            font-size: 1.1em;
                            line-height: 1.8;
                        }}
                        .back-link {{
                            display: inline-block;
                            margin: 20px 0;
                            color: #0066cc;
                            text-decoration: none;
                            padding: 10px 20px;
                            background: white;
                            border-radius: 4px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }}
                        .back-link:hover {{
                            background: #f8f8f8;
                        }}

                        .nav {{
                            position: fixed;
                            top: 0;
                            left: 0;
                            right: 0;
                            z-index: 100;
                            background: white;
                            padding: 1rem 2rem;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            display: flex;
                            align-items: center;
                            gap: 2rem;
                            flex-wrap: wrap;
                        }}
                        .nav h1 {{
                            margin: 0;
                            font-size:2rem;
                        }}

                        .nav p {{
                            margin: 0;
                            color: #666;
                            font-size: 2rem;
                        }}

                        .nav-links {{
                            display: flex;
                            gap: 1rem;
                            margin-left: auto;
                        }}

                        .back-link {{
                            color: #0066cc;
                            text-decoration: none;
                            padding: 0.5rem 1rem;
                            border-radius: 4px;
                            transition: background-color 0.2s;
                            font-size:1.1em;
                        }}

                        .back-link:hover {{
                            background-color: #f0f0f0;
                        }}

                        @media (max-width: 600px) {{
                            .nav {{
                                padding: 1rem;
                                gap: 1rem;
                            }}

                            .nav-links {{
                                width: 100%;
                                justify-content: center;
                            }}
                            .back-link {{
                             font-size:2em;

                            }}
                        }}
                        .webmention-link {{
                            position: absolute;
                            width: 1px;
                            height: 1px;
                            padding: 0;
                            margin: -1px;
                            overflow: hidden;
                            clip: rect(0, 0, 0, 0);
                            white-space: nowrap;
                            border: 0;
                            }}
                        #loader {{
                            text-align: center;
                            padding: 20px;
                            color: #666;
                            display: {'block' if has_next_page else 'none'};
                        }}
                    </style>
                </head>
                <body>
                   <div class="nav">
                      <h1>Haiku Archive</h1>
                      <p>times in UTC</p>
                      <div class="nav-links">
                          <a href="/" class="back-link">&#8962;</a>
                          <a href="/rss.xml" class="back-link">RSS</a>
                      </div>
                  </div>

                    <div id="poems-container">{poems_html}
                    </div>
                    <div id="loader" class="loader">Loading more poems...</div>

                    <script>
                        // Only embed metadata, fetch full data as needed
                        let allPoems = null; // Will be loaded on first scroll
                        let currentPage = 2;
                        const limit = {limit};
                        let isLoading = false;
                        let hasNextPage = {str(has_next_page).lower()};
                        const totalPoems = {len(poems)};

                        async function loadAllPoems() {{
                            if (allPoems) return allPoems; // Already loaded

                            try {{
                                console.log("Loading full poems data...");
                                const response = await fetch('/data/poems.json');
                                if (!response.ok) throw new Error('Failed to load poems');
                                allPoems = await response.json();
                                console.log("Loaded", allPoems.length, "poems");
                                return allPoems;
                            }} catch (error) {{
                                console.error("Error loading poems:", error);
                                // Fallback: disable further loading
                                hasNextPage = false;
                                document.getElementById('loader').style.display = 'none';
                                return [];
                            }}
                        }}

                        async function loadMorePoems() {{
                            if (isLoading || !hasNextPage) return;
                            isLoading = true;
                            console.log("Loading more poems...");

                            // Fetch all poems data if not already loaded
                            const poems = await loadAllPoems();
                            if (!poems.length) {{
                                isLoading = false;
                                return;
                            }}

                            const startIndex = (currentPage - 1) * limit;
                            const endIndex = startIndex + limit;
                            const paginatedPoems = poems.slice(startIndex, endIndex);

                            console.log("Rendering poems:", paginatedPoems.length);

                            const poemsContainer = document.getElementById('poems-container');
                            paginatedPoems.forEach(poem => {{
                                const poemDiv = document.createElement('div');
                                poemDiv.className = 'poem';
                                poemDiv.innerHTML = `
                                    <pre>${{poem.content}}</pre>
                                    <div class="date">${{new Date(poem.date).toLocaleDateString('en-US', {{
                                        year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
                                    }})}}</div>
                                    <a href="https://fed.brid.gy/" class="webmention-link">Bridgy Fed</a>`;
                                poemsContainer.appendChild(poemDiv);
                            }});

                            currentPage++;
                            hasNextPage = endIndex < poems.length;
                            isLoading = false;

                            // Hide loader if no more pages
                            if (!hasNextPage) {{
                                document.getElementById('loader').style.display = 'none';
                            }}
                        }}

                        window.addEventListener('scroll', () => {{
                            if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {{
                                loadMorePoems();
                            }}
                        }});
                    </script>
                </body>
            </html>'''

    return html_template

def main():
    """Generate archive.html"""
    # Load poems
    poems = load_poems()

    if not poems:
        print("No poems found. Run the haiku generator first.")
        return

    # Generate archive page with lazy loading
    archive_content = generate_archive_html(poems)

    # Save to parent directory (same level as scripts/)
    archive_path = os.path.join(os.path.dirname(__file__), '..', 'archive.html')
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(archive_content)

    print(f"Generated archive.html with {len(poems)} poems")

if __name__ == "__main__":
    main()