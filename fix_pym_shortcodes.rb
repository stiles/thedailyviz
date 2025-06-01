#!/usr/bin/env ruby

# Script to convert [pym src="..."] shortcodes to proper HTML

Dir.glob('_posts/**/*.html').each do |file|
  content = File.read(file)
  original_content = content.dup
  
  # Convert [pym src="..."] to proper HTML
  content.gsub!(/\[pym\s+src=['"]([^'"]+)['"]\s*\]/) do |match|
    src_url = $1
    %Q(<div class="pym-container" data-pym-src="#{src_url}"></div>)
  end
  
  if content != original_content
    puts "Converting shortcodes in: #{file}"
    File.write(file, content)
  end
end

puts "Done! All pym shortcodes have been converted to proper HTML." 