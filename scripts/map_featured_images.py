#!/usr/bin/env python3
"""
Script to properly map existing images to Jekyll posts based on WordPress media structure.
This script will:
1. Scan media directories for images that match post slugs
2. Update featured_image fields to point to actual existing images
3. Create a proper mapping between WordPress structure and Jekyll needs
"""

import os
import re
import yaml
from pathlib import Path
import unicodedata

def extract_front_matter(content):
    """Extract YAML front matter from post content."""
    if not content.startswith('---'):
        return None, content
    
    # Find the end of front matter
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

def slug_to_title_case(slug):
    """Convert a slug to title case for directory matching."""
    # Remove date prefix if present
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', slug)
    
    # Split on hyphens and capitalize
    words = slug.split('-')
    title_words = []
    
    for word in words:
        # Handle special cases
        if word.lower() in ['and', 'or', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']:
            title_words.append(word.lower())
        elif word.lower() in ['us', 'uk', 'gop', 'fbi', 'mlb', 'nfl', 'dc', 'korea', 'korean', 'north', 'south']:
            title_words.append(word.upper())
        else:
            title_words.append(word.capitalize())
    
    # Always capitalize first word
    if title_words:
        title_words[0] = title_words[0].capitalize()
    
    return '-'.join(title_words)

def find_media_directory_for_post(post_slug):
    """Find the media directory that corresponds to a post slug."""
    media_dir = Path('media')
    if not media_dir.exists():
        return None
    
    # Try different variations of the post title
    variations = [
        slug_to_title_case(post_slug),
        post_slug.replace('-', '-').title(),
        post_slug.replace('-', ' ').title().replace(' ', '-')
    ]
    
    # Look for directories that match
    for media_subdir in media_dir.iterdir():
        if media_subdir.is_dir():
            dir_name = media_subdir.name
            
            # Try exact matches and partial matches
            for variation in variations:
                if dir_name == variation:
                    return media_subdir
                # Also try partial matching for long titles
                if len(variation) > 20 and variation[:20] in dir_name:
                    return media_subdir
    
    return None

def find_featured_image_in_directory(media_dir):
    """Find the best candidate for a featured image in a media directory."""
    if not media_dir or not media_dir.exists():
        return None
    
    # Look for images in the directory
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

def update_featured_images():
    """Update all posts with proper featured image paths."""
    posts_dir = Path('_posts')
    updated_count = 0
    
    print("🔍 Mapping existing media to posts...")
    print("=" * 50)
    
    for post_file in posts_dir.glob('*.html'):
        post_slug = post_file.stem
        
        print(f"Processing: {post_slug}")
        
        # Read the post
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter
        front_matter, post_content = extract_front_matter(content)
        
        if not front_matter:
            print(f"  ⚠️  No front matter found")
            continue
        
        # Find corresponding media directory
        media_dir = find_media_directory_for_post(post_slug)
        
        if not media_dir:
            print(f"  ❌ No media directory found")
            continue
        
        # Find featured image in that directory
        featured_image_file = find_featured_image_in_directory(media_dir)
        
        if not featured_image_file:
            print(f"  ❌ No images found in {media_dir.name}")
            continue
        
        # Create relative path from root
        featured_image_path = f"/{featured_image_file}"
        
        # Update front matter
        front_matter['featured_image'] = featured_image_path
        
        # Write back to file
        new_content = write_front_matter(front_matter, post_content)
        
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ Mapped to: {featured_image_path}")
        updated_count += 1
    
    print(f"\n🎉 Successfully updated {updated_count} posts with existing images!")
    print("\nThese images should now display correctly on your site.")

if __name__ == "__main__":
    update_featured_images() 