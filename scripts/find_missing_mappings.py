#!/usr/bin/env python3
"""
Script to find posts that might have corresponding media directories but weren't mapped.
"""

import os
import re
import yaml
from pathlib import Path
from difflib import SequenceMatcher

def extract_front_matter(content):
    """Extract YAML front matter from post content."""
    if not content.startswith('---'):
        return None, content
    
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return None, content
    
    front_matter_text = content[3:end_match.start() + 3]
    post_content = content[end_match.end() + 3:]
    
    try:
        front_matter = yaml.safe_load(front_matter_text)
        return front_matter, post_content
    except yaml.YAMLError:
        return None, content

def normalize_for_matching(text):
    """Normalize text for better matching."""
    # Remove dates, convert to lowercase, remove special chars
    text = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', text)
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def find_best_media_match(post_slug, media_dirs):
    """Find the best matching media directory for a post slug."""
    post_normalized = normalize_for_matching(post_slug)
    
    best_match = None
    best_score = 0.0
    
    for media_dir in media_dirs:
        media_normalized = normalize_for_matching(media_dir.name)
        
        # Calculate similarity
        score = SequenceMatcher(None, post_normalized, media_normalized).ratio()
        
        # Boost score for keyword matches
        post_words = set(post_normalized.split())
        media_words = set(media_normalized.split())
        common_words = post_words.intersection(media_words)
        if common_words:
            word_boost = len(common_words) / max(len(post_words), len(media_words))
            score += word_boost * 0.3
        
        if score > best_score and score > 0.6:  # Minimum threshold
            best_score = score
            best_match = media_dir
    
    return best_match, best_score

def find_missing_mappings():
    """Find posts without featured images that might have media directories."""
    posts_dir = Path('_posts')
    media_dir = Path('media')
    
    if not media_dir.exists():
        print("No media directory found")
        return
    
    # Get all media directories
    media_dirs = [d for d in media_dir.iterdir() if d.is_dir()]
    
    print("🔍 Finding missing featured image mappings...")
    print("=" * 50)
    
    missing_mappings = []
    
    for post_file in posts_dir.glob('*.html'):
        # Read the post
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter
        front_matter, _ = extract_front_matter(content)
        
        if not front_matter:
            continue
        
        # Skip if already has featured image
        if 'featured_image' in front_matter:
            continue
        
        # Try to find a matching media directory
        post_slug = post_file.stem
        best_match, score = find_best_media_match(post_slug, media_dirs)
        
        if best_match:
            # Check if the directory has images
            image_files = [f for f in best_match.iterdir() 
                          if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']]
            
            if image_files:
                missing_mappings.append({
                    'post': post_slug,
                    'media_dir': best_match.name,
                    'score': score,
                    'image_count': len(image_files)
                })
    
    # Sort by score
    missing_mappings.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"Found {len(missing_mappings)} potential mappings:")
    print()
    
    for mapping in missing_mappings[:20]:  # Show top 20
        print(f"📄 {mapping['post']}")
        print(f"   → {mapping['media_dir']}")
        print(f"   Score: {mapping['score']:.2f}, Images: {mapping['image_count']}")
        print()
    
    return missing_mappings

if __name__ == "__main__":
    find_missing_mappings() 