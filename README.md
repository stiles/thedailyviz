# The Daily Viz

A (semi-retired) digital sketchpad for data stories, by Matt Stiles.

## Migration

This blog was successfully migrated from WordPress to Jekyll in May 2025. The migration included:

- **458 blog posts** from 2010-2021 
- **600 images** consolidated from WordPress uploads 
- **D3 visualizations** using the NPR dailygraphics rig with pym.js 
- **Original design** recreated using the same fonts (Source Sans Pro, PT Serif, Source Code Pro) 

## Running locally

```bash
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000` to view the blog.

## Features

- **Static site generation** with Jekyll 4.3
- **Responsive design** matching the original Illustratr WordPress theme
- **D3 chart embeds** automatically converted from `[pym src="..."]` format
- **Search engine optimization** with proper meta tags and RSS feed
- **Fast loading** with optimized images and minimal dependencies

## Content processing

The site includes custom plugins that:

- Convert WordPress `[pym src="..."]` shortcodes to proper HTML containers
- Clean up WordPress HTML artifacts and encoding issues
- Map original WordPress image filenames to UUID-based filenames via symlinks
- Preserve all categories, tags, and metadata

## Image handling

Images are organized as follows:
- Original WordPress images stored in `media/{Post-Title}/` subdirectories with UUID filenames
- Consolidated in `media/images/` with both UUID and original filenames (via symlinks)
- **106 image mappings** created automatically from WordPress exports

## Deployment options

This static site can be deployed to:

- **GitHub Pages** (free)
- **Netlify** (free tier)
- **Vercel** (free tier)  
- Any static hosting provider

## D3 visualizations

The blog's D3 charts are hosted externally at `mattstiles.org/dailygraphics` and embedded using pym.js for responsive iframe behavior. These continue to work exactly as they did in the original WordPress blog.

## Directory structure

```
├── _posts/           # All blog posts (imported from WordPress)
├── _layouts/         # Jekyll templates
├── _plugins/         # Custom content processors
├── css/             # Stylesheets matching original design
├── media/           # Original WordPress media structure
│   └── images/      # Consolidated image directory (UUID + symlinked originals)
├── _config.yml      # Jekyll configuration
└── Gemfile          # Ruby dependencies
```

## Original blog data

The original WordPress XML export file us preserved in the `data/` directory for reference. 