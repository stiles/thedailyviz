#!/usr/bin/env python3
"""
Enhanced script to map more posts to their featured images using flexible matching.
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

def write_front_matter(front_matter, content):
    """Write front matter and content back to post format."""
    yaml_content = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
    return f"---\n{yaml_content}---\n{content}"

def normalize_for_matching(text):
    """Normalize text for better matching."""
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

def find_featured_image_in_directory(media_dir):
    """Find the best candidate for a featured image in a media directory."""
    if not media_dir or not media_dir.exists():
        return None
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    images = []
    
    for file_path in media_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            images.append(file_path)
    
    if not images:
        return None
    
    # Prefer certain naming patterns for featured images
    for img in images:
        name_lower = img.name.lower()
        if any(keyword in name_lower for keyword in ['featured', 'promo', 'topper', 'main']):
            return img
    
    # If no obvious featured image, take the first one
    return images[0]

def map_more_featured_images():
    """Map more posts to their featured images using enhanced matching."""
    posts_dir = Path('_posts')
    media_dir = Path('media')
    
    if not media_dir.exists():
        print("No media directory found")
        return
    
    # Get all media directories
    media_dirs = [d for d in media_dir.iterdir() if d.is_dir()]
    
    print("🖼️  Mapping additional featured images with enhanced matching...")
    print("=" * 65)
    
    mapped_count = 0
    
    for post_file in posts_dir.glob('*.html'):
        post_slug = post_file.stem
        
        # Read the post
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter
        front_matter, post_content = extract_front_matter(content)
        
        if not front_matter:
            continue
        
        # Skip if already has featured image
        if 'featured_image' in front_matter:
            continue
        
        # Try to find a matching media directory
        best_match, score = find_best_media_match(post_slug, media_dirs)
        
        if best_match and score > 0.8:  # Only map high-confidence matches
            # Find featured image in that directory
            featured_image_file = find_featured_image_in_directory(best_match)
            
            if featured_image_file:
                # Create relative path from root
                featured_image_path = f"/{featured_image_file}"
                
                # Update front matter
                front_matter['featured_image'] = featured_image_path
                
                # Write back to file
                new_content = write_front_matter(front_matter, post_content)
                
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ {post_slug}")
                print(f"   → {featured_image_path}")
                print(f"   Score: {score:.2f}")
                print()
                
                mapped_count += 1
    
    print(f"🎉 Successfully mapped {mapped_count} additional posts!")

if __name__ == "__main__":
    map_more_featured_images() 