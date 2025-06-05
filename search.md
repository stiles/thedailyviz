---
layout: default
title: Search
permalink: /search/
---

# Search

<div id="search-container" class="search-container page-search-container">
  <input type="text" id="search-input" class="search-input" placeholder="Search posts by title, content, tags, or category...">
  <ul id="results-container" class="results-container"></ul>
</div>

<div id="search-results-info" class="search-results-info" style="display: none;">
  <p><span id="search-results-count">0</span> results found</p>
</div>

<script src="{{ '/assets/js/simple-jekyll-search.min.js' | relative_url }}"></script>
<script>
window.simpleJekyllSearch = new SimpleJekyllSearch({
  searchInput: document.getElementById('search-input'),
  resultsContainer: document.getElementById('results-container'),
  json: '{{ '/search.json' | relative_url }}',
  searchResultTemplate: '<li class="search-result"><h3><a href="{url}">{title}</a></h3><p class="search-meta"><time>{date}</time> • {category}</p><p class="search-excerpt">{content}</p></li>',
  noResultsText: '<li class="no-results">No results found</li>',
  limit: 10,
  fuzzy: false,
  exclude: []
});

// Show results count
document.getElementById('search-input').addEventListener('input', function() {
  setTimeout(function() {
    const results = document.querySelectorAll('#results-container .search-result');
    const count = results.length;
    const info = document.getElementById('search-results-info');
    const countSpan = document.getElementById('search-results-count');
    
    if (document.getElementById('search-input').value.trim() !== '') {
      info.style.display = 'block';
      countSpan.textContent = count;
    } else {
      info.style.display = 'none';
    }
  }, 100);
});
</script>

<style>
.search-container {
  margin: 2rem 0;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: rgb(120, 120, 120);
}

.results-container {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.search-result {
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.search-result:last-child {
  border-bottom: none;
}

.search-result h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.search-result h3 a {
  color: #333;
  text-decoration: none;
}

.search-result h3 a:hover {
  color:rgb(120, 120, 120);
}

.search-meta {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
}

.search-excerpt {
  color: #555;
  line-height: 1.5;
  margin: 0;
}

.no-results {
  color: #666;
  font-style: italic;
  padding: 1rem 0;
}

.search-results-info {
  color: #666;
  font-size: 0.9rem;
  margin: 1rem 0;
}
</style> 