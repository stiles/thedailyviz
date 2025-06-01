module Jekyll
  module ContentProcessor
    def self.process_content(content)
      # First, remove WordPress HTML wrapper tags
      content = content.gsub(/<!DOCTYPE html[^>]*>/, '')
      content = content.gsub(/<html[^>]*>/, '')
      content = content.gsub(/<body[^>]*>/, '')
      content = content.gsub(/<\/body>/, '')
      content = content.gsub(/<\/html>/, '')
      
      # Fix HTML encoding issues
      content = content.gsub(/&amp;/, '&')
      content = content.gsub(/&quot;/, '"')
      content = content.gsub(/&#8217;/, "'")
      content = content.gsub(/&#8220;/, '"')
      content = content.gsub(/&#8221;/, '"')
      content = content.gsub(/&#8211;/, '–')
      content = content.gsub(/&#8212;/, '—')
      
      # Convert [pym src="..."] to proper HTML (AFTER cleanup)
      content = content.gsub(/\[pym src="([^"]+)"\]/) do |match|
        src = $1
        "<div class=\"pym-container\" data-pym-src=\"#{src}\"></div>"
      end
      
      # Fix image paths - the images in the media directories use UUID-style filenames
      # The structure is: media/{Post-Title}/{uuid-filename.ext}
      # We need to keep these paths as they are, but ensure they work in Jekyll
      
      # Fix old WordPress upload URLs to point to our media directory structure
      content = content.gsub(/(?:https?:\/\/)?(?:i[0-9]\.wp\.com\/)?thedailyviz\.com\/wp-content\/uploads\/[^\/]+\/[^\/]+\/([^"'>\s]+)/) do |match|
        filename = $1
        # For now, just reference the filename - we'll handle directory mapping in Jekyll
        "/media/images/#{filename}"
      end
      
      # Handle direct links to wp-content
      content = content.gsub(/(?:https?:\/\/)?thedailyviz\.com\/wp-content\/uploads\/[^\/]+\/[^\/]+\/([^"'>\s]+)/) do |match|
        filename = $1
        "/media/images/#{filename}"
      end
      
      # Clean up extra paragraph tags and line breaks
      content = content.gsub(/<p><\/p>/, '')
      content = content.gsub(/<p><br \/>\s*<\/p>/, '')
      content = content.strip
      
      content
    end
  end
end

# Hook to process posts during build
Jekyll::Hooks.register :posts, :post_convert do |post|
  post.content = Jekyll::ContentProcessor.process_content(post.content)
end

Jekyll::Hooks.register :pages, :post_convert do |page|
  page.content = Jekyll::ContentProcessor.process_content(page.content)
end 