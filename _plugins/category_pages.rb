module Jekyll
  class CategoryPageGenerator < Generator
    safe true

    def generate(site)
      # Generate category pages
      if site.layouts.key? 'category'
        dir = site.config['category_dir'] || 'category'
        site.categories.each_key do |category|
          site.pages << CategoryPage.new(site, site.source, File.join(dir, category.downcase.gsub(/\s+/, '-').gsub(/[^\w\-]/, '')), category)
        end
      end
      
      # Generate tag pages
      if site.layouts.key? 'tag'
        dir = site.config['tag_dir'] || 'tag'
        site.tags.each_key do |tag|
          site.pages << TagPage.new(site, site.source, File.join(dir, tag.downcase.gsub(/\s+/, '-').gsub(/[^\w\-]/, '')), tag)
        end
      end
    end
  end

  class CategoryPage < Page
    def initialize(site, base, dir, category)
      @site = site
      @base = base
      @dir  = dir
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'category.html')
      self.data['category'] = category
      self.data['title'] = "#{category}"
      
      # Add descriptions for known categories
      case category.downcase
      when 'policy & politics', 'policy &amp; politics'
        self.data['title'] = 'Politics'
        self.data['description'] = 'Election analysis, voting patterns, and political data stories'
      when 'data visualization'
        self.data['description'] = 'Charts, maps, and interactive graphics exploring various datasets'
      when 'sports'
        self.data['description'] = 'Baseball analytics, player statistics, and sports data analysis'
      when 'economy & finance', 'economy &amp; finance'
        self.data['title'] = 'Economics'
        self.data['description'] = 'Economic indicators, market analysis, and financial data'
      when 'demographics'
        self.data['description'] = 'Population data, census analysis, and community statistics'
      when 'crime'
        self.data['title'] = 'Crime and justice'
        self.data['description'] = 'Crime statistics, law enforcement data, and justice system analysis'
      when 'north korea'
        self.data['title'] = 'North Korea'
        self.data['description'] = 'Analysis and data stories about North Korea'
      when 'south korea'
        self.data['title'] = 'South Korea'
        self.data['description'] = 'Analysis and data stories about South Korea'
      when 'social media'
        self.data['title'] = 'Social Media'
        self.data['description'] = 'Social media analysis and data stories'
      when 'weather'
        self.data['title'] = 'Weather'
        self.data['description'] = 'Weather data and climate analysis'
      when 'tutorials'
        self.data['title'] = 'Tutorials'
        self.data['description'] = 'How-to guides and tutorials'
      end
    end
  end
  
  class TagPage < Page
    def initialize(site, base, dir, tag)
      @site = site
      @base = base
      @dir  = dir
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'tag.html')
      self.data['tag'] = tag
      self.data['title'] = "Posts tagged \"#{tag}\""
    end
  end
end 