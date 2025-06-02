#!/usr/bin/env python3
"""
Script to clean up posts with featured_image paths pointing to non-existent files.
This script will remove the featured_image field from posts that reference missing files.
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

def cleanup_missing_featured_images():
    """Remove featured_image fields that point to non-existent files."""
    posts_dir = Path('_posts')
    cleaned_count = 0
    
    print("🧹 Cleaning up posts with missing featured images...")
    print("=" * 55)
    
    for post_file in posts_dir.glob('*.html'):
        post_slug = post_file.stem
        
        # Read the post
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter
        front_matter, post_content = extract_front_matter(content)
        
        if not front_matter or 'featured_image' not in front_matter:
            continue
        
        featured_image_path = front_matter['featured_image']
        
        # Check if it's one of the problematic paths
        if '/media/images/featured-' in featured_image_path:
            # Check if the file actually exists
            file_path = Path(featured_image_path.lstrip('/'))
            if not file_path.exists():
                print(f"Processing: {post_slug}")
                print(f"  ❌ Removing missing: {featured_image_path}")
                
                # Remove the featured_image field
                del front_matter['featured_image']
                
                # Write back to file
                new_content = write_front_matter(front_matter, post_content)
                
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                cleaned_count += 1
    
    print(f"\n🎉 Cleaned up {cleaned_count} posts by removing missing featured images!")
    print("These posts will no longer generate 404 errors.")

if __name__ == "__main__":
    cleanup_missing_featured_images() 