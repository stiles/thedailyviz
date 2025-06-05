---
layout: default
title: Blog topics
permalink: /topics/
---

# Blog topics

Explore posts by category and topic. Browse by subject area to find data stories and visualizations that interest you.

## Popular categories

<div class="topics-grid">
  <div class="topic-card">
    <h3><a href="/category/policy-amp-politics/">Politics</a></h3>
    <p>Election analysis, voting patterns, and political data stories</p>
  </div>
  
  <div class="topic-card">
    <h3><a href="/category/sports/">Sports</a></h3>
    <p>Baseball analytics, player statistics, and sports data analysis</p>
  </div>
  
  <div class="topic-card">
    <h3><a href="/category/economy-amp-finance/">Economics</a></h3>
    <p>Economic indicators, market analysis, and financial data</p>
  </div>
  
  <div class="topic-card">
    <h3><a href="/category/demographics/">Demographics</a></h3>
    <p>Population data, census analysis, and community statistics</p>
  </div>
  
  <div class="topic-card">
    <h3><a href="/category/crime/">Crime and justice</a></h3>
    <p>Crime statistics, law enforcement data, and justice system analysis</p>
  </div>
  
  <div class="topic-card">
    <h3><a href="/category/north-korea/">North Korea</a></h3>
    <p>Analysis and data stories about North Korea</p>
  </div>
</div>

## All categories

{% assign categories = site.categories | sort %}
<div class="categories-list">
  {% for category in categories %}
    <div class="category-item">
      <h4><a href="/category/{{ category[0] | downcase | replace: ' ', '-' | replace: '&amp;', 'amp' | replace: '&', 'amp' }}/">{{ category[0] | replace: '&amp;', '&' }}</a></h4>
      <span class="post-count">{{ category[1] | size }} posts</span>
    </div>
  {% endfor %}
</div>

## Browse by tag

{% assign tags = site.tags | sort %}
<div class="tags-cloud">
  {% for tag in tags %}
    <a href="/tag/{{ tag[0] | downcase | replace: ' ', '-' | replace: '&amp;', 'amp' | replace: '&', 'amp' }}/" class="tag-link" style="font-size: {{ tag[1] | size | times: 0.1 | plus: 1 }}em;">
      {{ tag[0] }}
    </a>
  {% endfor %}
</div>

---

**Can't find what you're looking for?** Try the [search function](/search/) or [browse all posts](/) chronologically. 