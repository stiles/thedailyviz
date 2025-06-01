module Jekyll
  class PymTag < Liquid::Tag
    
    def initialize(tag_name, markup, tokens)
      super
      @markup = markup.strip
    end

    def render(context)
      # Parse the src attribute from the markup
      if @markup =~ /src=['"]([^'"]+)['"]/
        src_url = $1
        %Q(<div class="pym-container" data-pym-src="#{src_url}"></div>)
      else
        %Q(<div class="pym-container"><!-- Invalid pym tag: #{@markup} --></div>)
      end
    end
  end
end

Liquid::Template.register_tag('pym', Jekyll::PymTag)

# Also register a filter to handle the shortcode syntax in markdown content
module Jekyll
  module PymFilter
    def pym_shortcodes(content)
      # Convert [pym src="..."] to proper HTML
      content.gsub(/\[pym\s+src=['"]([^'"]+)['"]\s*\]/) do |match|
        src_url = $1
        %Q(<div class="pym-container" data-pym-src="#{src_url}"></div>)
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::PymFilter)

Jekyll::Hooks.register :posts, :post_render do |post|
  puts "Processing post: #{post.data['title']}"
  
  # Convert [pym src="..."] shortcodes to proper HTML
  original_output = post.output.dup
  post.output = post.output.gsub(/\[pym\s+src=['"]([^'"]+)['"]\s*\]/) do |match|
    src_url = $1
    puts "Converting pym shortcode: #{match} -> #{src_url}"
    %Q(<div class="pym-container" data-pym-src="#{src_url}"></div>)
  end
  
  if original_output != post.output
    puts "Content was modified for #{post.data['title']}"
  else
    puts "No pym shortcodes found in #{post.data['title']}"
  end
end

Jekyll::Hooks.register :pages, :post_render do |page|
  # Convert [pym src="..."] shortcodes to proper HTML
  page.output = page.output.gsub(/\[pym\s+src=['"]([^'"]+)['"]\s*\]/) do |match|
    src_url = $1
    %Q(<div class="pym-container" data-pym-src="#{src_url}"></div>)
  end
end 