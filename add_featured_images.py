#!/usr/bin/env python3
"""
Script to add featured_image fields to Jekyll posts based on WordPress _thumbnail_id values.
This script will:
1. Scan all posts for _thumbnail_id values
2. Create a mapping strategy for thumbnail IDs to actual image files
3. Add featured_image fields to post front matter
"""

import os
import re
import yaml
from pathlib import Path

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

def find_image_files():
    """Find all available image files in media directory."""
    image_files = []
    media_dir = Path('media')
    
    if media_dir.exists():
        # Look for images in media/images and subdirectories
        for img_path in media_dir.rglob('*'):
            if img_path.is_file() and img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                # Store relative path from root
                image_files.append(str(img_path))
    
    return image_files

def create_thumbnail_mapping():
    """Create a mapping strategy for thumbnail IDs to images."""
    # For now, we'll create a generic featured image path pattern
    # In a real scenario, you'd have a WordPress database or export to map these
    
    # Common pattern: create a standard featured image path
    def get_featured_image_path(thumbnail_id, post_slug):
        # Strategy 1: Look for images with the thumbnail ID in the name
        image_files = find_image_files()
        
        # Try to find an image that might match this post
        for img_path in image_files:
            img_name = Path(img_path).stem.lower()
            if thumbnail_id in img_name:
                return f"/{img_path}"
        
        # Strategy 2: Look for images in a directory matching the post slug
        post_dir = f"media/{post_slug}"
        if Path(post_dir).exists():
            for img_path in Path(post_dir).glob('*'):
                if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                    return f"/{img_path}"
        
        # Strategy 3: Create a standard path (even if file doesn't exist yet)
        # This allows you to add images later with predictable naming
        return f"/media/images/featured-{thumbnail_id}.jpg"
    
    return get_featured_image_path

def process_posts():
    """Process all posts and add featured_image fields."""
    posts_dir = Path('_posts')
    mapping_func = create_thumbnail_mapping()
    
    processed_count = 0
    
    for post_file in posts_dir.glob('*.html'):
        print(f"Processing: {post_file.name}")
        
        # Read the post
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter
        front_matter, post_content = extract_front_matter(content)
        
        if not front_matter:
            print(f"  ⚠️  No front matter found in {post_file.name}")
            continue
        
        # Check if it has a thumbnail_id (could be at top level or under meta)
        thumbnail_id = front_matter.get('_thumbnail_id')
        if not thumbnail_id and 'meta' in front_matter:
            thumbnail_id = front_matter['meta'].get('_thumbnail_id')
        
        if not thumbnail_id:
            print(f"  ⚠️  No _thumbnail_id found in {post_file.name}")
            continue
        
        # Check if featured_image already exists
        if front_matter.get('featured_image'):
            print(f"  ✅ Featured image already exists in {post_file.name}")
            continue
        
        # Create post slug from filename
        post_slug = post_file.stem
        
        # Get featured image path
        featured_image_path = mapping_func(str(thumbnail_id), post_slug)
        
        # Add featured_image to front matter
        front_matter['featured_image'] = featured_image_path
        
        # Write back to file
        new_content = write_front_matter(front_matter, post_content)
        
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ Added featured_image: {featured_image_path}")
        processed_count += 1
    
    print(f"\n🎉 Processed {processed_count} posts!")
    print("\nNext steps:")
    print("1. Review the added featured_image paths")
    print("2. Create/upload actual image files to match the paths")
    print("3. Test the site locally to verify images display correctly")

if __name__ == "__main__":
    print("🖼️  Adding featured images to Jekyll posts...")
    print("=" * 50)
    process_posts() 