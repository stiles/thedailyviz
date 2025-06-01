module Jekyll
  # Featured Image plugin to handle WordPress featured images in Jekyll
  class FeaturedImageGenerator < Generator
    safe true
    priority :high

    def generate(site)
      # Direct mapping of thumbnail IDs to image paths
      # This is built by manually checking key posts and their media directories
      thumbnail_map = {
        '3745' => '/media/Visualizing-Verified-Twitters-Reaction-to-Robert-Muellers-Investigation/968cd520-488e-11eb-8d10-75365b90901d.jpg', # Robert Mueller featured image
        '3786' => '/media/Visualizing-Historical-Political-Party-Identification-in-the-Era-of-Trump/d09d55a0-488e-11eb-8d10-75365b90901d.jpg', # Political party identification featured image
        '3738' => '/media/Trumps-Approval-Ratings-are-Resilient-How-Does-that-Compare-Historically/df4c2d10-487f-11eb-8d10-75365b90901d.jpg', # Trump approval ratings featured image
        '3778' => '/media/How-Wacky-Has-LAs-Weather-Been-in-2019-These-Charts-Help-Explain/07c002d0-4880-11eb-8d10-75365b90901d.jpg', # LA weather featured image
        '2450' => '/media/Editing-OJ-Simpson-Charting-Changes-to-His-Wikipedia-Page/0c14c8e0-487e-11eb-8d10-75365b90901d.png', # OJ Simpson featured image
        # Add more mappings as needed
      }
      
      # Process posts and add featured image paths
      site.posts.docs.each do |post|
        if post.data['meta'] && post.data['meta']['_thumbnail_id']
          thumbnail_id = post.data['meta']['_thumbnail_id']
          if thumbnail_map[thumbnail_id]
            post.data['featured_image'] = thumbnail_map[thumbnail_id]
          end
        end
      end
    end
  end

  # Liquid filter for featured images
  module FeaturedImageFilter
    def featured_image_url(post, size = 'large')
      return '' unless post['featured_image']
      post['featured_image']
    end
    
    def has_featured_image(post)
      !post['featured_image'].nil? && !post['featured_image'].empty?
    end
  end
end

Liquid::Template.register_filter(Jekyll::FeaturedImageFilter) 