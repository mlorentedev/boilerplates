"""
Fast search functionality for documentation and snippets
Target: <100ms search time
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import re

# Get paths
REPO_ROOT = Path(__file__).parent.parent.parent.absolute()
DOCS_DIR = REPO_ROOT / "docs"
CACHE_DIR = Path.home() / ".cache" / "bp"
SEARCH_INDEX = CACHE_DIR / "search_index.json"
HISTORY_FILE = CACHE_DIR / "search_history.json"

# Ensure cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def build_search_index() -> Dict:
    """Build search index from documentation"""
    index = {
        'documents': [],
        'snippets': [],
        'templates': [],
        'categories': {},
        'tags': {},
        'last_updated': time.time()
    }

    # Index documentation files
    if DOCS_DIR.exists():
        for md_file in DOCS_DIR.rglob('*.md'):
            relative_path = md_file.relative_to(DOCS_DIR)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else 'root'

            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem

                # Extract description (first paragraph after title)
                desc_match = re.search(r'^#.+\n\n(.+)$', content, re.MULTILINE)
                description = desc_match.group(1)[:200] if desc_match else ''

                # Extract tags
                tags = []
                tag_matches = re.findall(r'#(\w+)', content)
                tags.extend(tag_matches[:10])  # Limit tags

                # Extract code blocks for snippets
                code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)

                doc_entry = {
                    'title': title,
                    'description': description,
                    'path': str(relative_path),
                    'full_path': str(md_file),
                    'category': category,
                    'tags': tags,
                    'content': content[:1000],  # First 1000 chars for search
                    'code_blocks': len(code_blocks)
                }

                index['documents'].append(doc_entry)

                # Add to category index
                if category not in index['categories']:
                    index['categories'][category] = []
                index['categories'][category].append(doc_entry)

                # Add to tag index
                for tag in tags:
                    if tag not in index['tags']:
                        index['tags'][tag] = []
                    index['tags'][tag].append(doc_entry)

            except Exception as e:
                print(f"Warning: Could not index {md_file}: {e}")

    # Index template directories
    template_dirs = ['terraform', 'kubernetes', 'docker-compose', 'ansible', 'microservices']
    for template_dir in template_dirs:
        dir_path = REPO_ROOT / template_dir
        if dir_path.exists() and dir_path.is_dir():
            for item in dir_path.iterdir():
                if item.is_dir():
                    template_entry = {
                        'name': item.name,
                        'category': template_dir,
                        'path': str(item.relative_to(REPO_ROOT)),
                        'full_path': str(item)
                    }
                    index['templates'].append(template_entry)

    # Save index
    with open(SEARCH_INDEX, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)

    return index


def load_search_index() -> Dict:
    """Load search index from cache"""
    if not SEARCH_INDEX.exists():
        return build_search_index()

    try:
        with open(SEARCH_INDEX, 'r', encoding='utf-8') as f:
            index = json.load(f)

        # Check if index is stale (older than 1 hour)
        if time.time() - index.get('last_updated', 0) > 3600:
            return build_search_index()

        return index

    except Exception as e:
        print(f"Warning: Could not load index, rebuilding: {e}")
        return build_search_index()


def search_docs(query: str, category: Optional[str] = None,
                tag: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """
    Fast search through documentation
    Target: <100ms
    """
    start_time = time.time()

    # Load index
    index = load_search_index()

    # Normalize query
    query_lower = query.lower()
    query_terms = query_lower.split()

    results = []

    # Search documents
    for doc in index['documents']:
        # Apply category filter
        if category and doc['category'] != category:
            continue

        # Apply tag filter
        if tag and tag not in doc.get('tags', []):
            continue

        # Calculate relevance score
        score = 0

        # Title match (highest priority)
        if query_lower in doc['title'].lower():
            score += 100

        # Exact phrase match
        if query_lower in doc.get('content', '').lower():
            score += 50

        # Term matching
        for term in query_terms:
            # Title
            if term in doc['title'].lower():
                score += 10

            # Description
            if term in doc.get('description', '').lower():
                score += 5

            # Content
            if term in doc.get('content', '').lower():
                score += 2

            # Tags
            if term in ' '.join(doc.get('tags', [])).lower():
                score += 3

            # Category
            if term in doc['category'].lower():
                score += 3

        if score > 0:
            # Extract snippet around match
            snippet = extract_snippet(doc.get('content', ''), query_terms)

            results.append({
                'title': doc['title'],
                'description': doc.get('description', ''),
                'path': doc['path'],
                'full_path': doc['full_path'],
                'category': doc['category'],
                'tags': doc.get('tags', []),
                'snippet': snippet,
                'score': score
            })

    # Search templates
    for template in index['templates']:
        if category and template['category'] != category:
            continue

        score = 0

        # Name match
        if query_lower in template['name'].lower():
            score += 80

        # Category match
        if query_lower in template['category'].lower():
            score += 40

        # Term matching
        for term in query_terms:
            if term in template['name'].lower():
                score += 8
            if term in template['category'].lower():
                score += 4

        if score > 0:
            results.append({
                'title': template['name'],
                'description': f"Template in {template['category']}",
                'path': template['path'],
                'full_path': template['full_path'],
                'category': template['category'],
                'tags': [],
                'snippet': '',
                'score': score
            })

    # Sort by relevance score
    results.sort(key=lambda x: x['score'], reverse=True)

    # Limit results
    results = results[:limit]

    # Calculate search time
    search_time = (time.time() - start_time) * 1000

    # Log performance (for monitoring)
    if search_time > 100:
        print(f"Warning: Search took {search_time:.2f}ms (target: <100ms)")

    return results


def extract_snippet(content: str, terms: List[str], context_chars: int = 150) -> str:
    """Extract relevant snippet from content around search terms"""
    content_lower = content.lower()

    # Find first occurrence of any term
    first_pos = len(content)
    for term in terms:
        pos = content_lower.find(term)
        if pos != -1 and pos < first_pos:
            first_pos = pos

    if first_pos == len(content):
        # No match found, return beginning
        return content[:context_chars] + '...'

    # Extract context around match
    start = max(0, first_pos - context_chars // 2)
    end = min(len(content), first_pos + context_chars // 2)

    snippet = content[start:end]

    # Add ellipsis
    if start > 0:
        snippet = '...' + snippet
    if end < len(content):
        snippet = snippet + '...'

    return snippet.strip()


def list_category(category: str) -> List[Dict]:
    """List all items in a category"""
    index = load_search_index()

    category_items = []

    # Get documents in category
    if category in index['categories']:
        category_items.extend(index['categories'][category])

    # Get templates in category
    for template in index['templates']:
        if template['category'] == category:
            category_items.append({
                'title': template['name'],
                'description': f"Template in {category}",
                'path': template['path'],
                'category': category,
                'tags': []
            })

    return category_items


def save_search(query: str):
    """Save search to history"""
    history = search_history()

    # Add new search
    history.insert(0, {
        'query': query,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })

    # Keep only last 50 searches
    history = history[:50]

    # Save history
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save search history: {e}")


def search_history() -> List[Dict]:
    """Get search history"""
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def fuzzy_match(query: str, target: str) -> int:
    """Simple fuzzy matching score"""
    query = query.lower()
    target = target.lower()

    # Exact match
    if query == target:
        return 100

    # Contains
    if query in target:
        return 80

    # All characters present in order
    query_idx = 0
    for char in target:
        if query_idx < len(query) and char == query[query_idx]:
            query_idx += 1

    if query_idx == len(query):
        return 60

    # Count matching characters
    matching = sum(1 for c in query if c in target)
    return int((matching / len(query)) * 50)


if __name__ == '__main__':
    # Test search performance
    print("Building search index...")
    start = time.time()
    build_search_index()
    print(f"Index built in {(time.time() - start)*1000:.2f}ms")

    # Test search
    print("\nTesting search...")
    queries = ['kubernetes', 'docker postgres', 'terraform aws', 'ansible ubuntu']

    for query in queries:
        start = time.time()
        results = search_docs(query, limit=5)
        elapsed = (time.time() - start) * 1000
        print(f"\nQuery: '{query}' - {len(results)} results in {elapsed:.2f}ms")
        for r in results[:3]:
            print(f"  - {r['title']} (score: {r['score']})")
