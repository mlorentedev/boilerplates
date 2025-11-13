// Custom JavaScript for boilerplates documentation

document.addEventListener('DOMContentLoaded', function() {
  // Add copy functionality to code blocks
  addCopyButtons();

  // Track search performance
  trackSearchPerformance();

  // Add keyboard shortcuts
  addKeyboardShortcuts();

  // Initialize tooltips
  initializeTooltips();

  // Track popular searches
  trackSearches();
});

// Add copy buttons to all code blocks
function addCopyButtons() {
  const codeBlocks = document.querySelectorAll('pre code');

  codeBlocks.forEach(function(codeBlock) {
    const pre = codeBlock.parentElement;

    // Skip if button already exists
    if (pre.querySelector('.copy-button')) {
      return;
    }

    const button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = 'Copy';
    button.style.cssText = `
      position: absolute;
      top: 0.5rem;
      right: 0.5rem;
      padding: 0.25rem 0.5rem;
      background: var(--md-primary-fg-color);
      color: white;
      border: none;
      border-radius: 0.25rem;
      cursor: pointer;
      font-size: 0.8rem;
      opacity: 0;
      transition: opacity 0.2s;
    `;

    pre.style.position = 'relative';
    pre.appendChild(button);

    pre.addEventListener('mouseenter', function() {
      button.style.opacity = '1';
    });

    pre.addEventListener('mouseleave', function() {
      button.style.opacity = '0';
    });

    button.addEventListener('click', function() {
      const text = codeBlock.textContent;

      navigator.clipboard.writeText(text).then(function() {
        button.textContent = 'Copied!';
        button.style.background = '#4caf50';

        setTimeout(function() {
          button.textContent = 'Copy';
          button.style.background = 'var(--md-primary-fg-color)';
        }, 2000);
      }).catch(function(err) {
        console.error('Failed to copy:', err);
        button.textContent = 'Failed';
        button.style.background = '#f44336';

        setTimeout(function() {
          button.textContent = 'Copy';
          button.style.background = 'var(--md-primary-fg-color)';
        }, 2000);
      });
    });
  });
}

// Track search performance
function trackSearchPerformance() {
  const searchInput = document.querySelector('.md-search__input');

  if (!searchInput) {
    return;
  }

  let searchStartTime;

  searchInput.addEventListener('input', function() {
    searchStartTime = performance.now();
  });

  // Monitor search results
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.type === 'childList' && searchStartTime) {
        const searchEndTime = performance.now();
        const searchTime = searchEndTime - searchStartTime;

        // Log search performance (for monitoring)
        if (window.console && console.debug) {
          console.debug(`Search completed in ${searchTime.toFixed(2)}ms`);
        }

        // Show performance badge if search is slow
        if (searchTime > 100) {
          showPerformanceWarning(searchTime);
        }

        searchStartTime = null;
      }
    });
  });

  const searchResults = document.querySelector('.md-search__output');
  if (searchResults) {
    observer.observe(searchResults, { childList: true, subtree: true });
  }
}

// Show performance warning for slow searches
function showPerformanceWarning(searchTime) {
  const existing = document.querySelector('.performance-warning');
  if (existing) {
    existing.remove();
  }

  const warning = document.createElement('div');
  warning.className = 'performance-warning';
  warning.style.cssText = `
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    padding: 0.75rem 1rem;
    background: #ff9800;
    color: white;
    border-radius: 0.25rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    font-size: 0.9rem;
  `;
  warning.textContent = `Search took ${searchTime.toFixed(0)}ms (target: <100ms)`;

  document.body.appendChild(warning);

  setTimeout(function() {
    warning.remove();
  }, 3000);
}

// Add keyboard shortcuts
function addKeyboardShortcuts() {
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      const searchInput = document.querySelector('.md-search__input');
      if (searchInput) {
        searchInput.focus();
      }
    }

    // Ctrl/Cmd + /: Show keyboard shortcuts
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
      e.preventDefault();
      showKeyboardShortcuts();
    }
  });
}

// Show keyboard shortcuts modal
function showKeyboardShortcuts() {
  const existing = document.querySelector('.shortcuts-modal');
  if (existing) {
    existing.remove();
    return;
  }

  const modal = document.createElement('div');
  modal.className = 'shortcuts-modal';
  modal.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: var(--md-default-bg-color);
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    max-width: 500px;
    width: 90%;
  `;

  modal.innerHTML = `
    <h3 style="margin-top: 0;">Keyboard Shortcuts</h3>
    <table style="width: 100%;">
      <tr><td><kbd>Ctrl/Cmd</kbd> + <kbd>K</kbd></td><td>Open search</td></tr>
      <tr><td><kbd>Esc</kbd></td><td>Close search</td></tr>
      <tr><td><kbd>↑</kbd> / <kbd>↓</kbd></td><td>Navigate results</td></tr>
      <tr><td><kbd>Enter</kbd></td><td>Go to result</td></tr>
      <tr><td><kbd>Ctrl/Cmd</kbd> + <kbd>/</kbd></td><td>Show shortcuts</td></tr>
    </table>
    <button id="close-shortcuts" style="margin-top: 1rem; padding: 0.5rem 1rem; background: var(--md-primary-fg-color); color: white; border: none; border-radius: 0.25rem; cursor: pointer;">Close</button>
  `;

  const overlay = document.createElement('div');
  overlay.className = 'shortcuts-overlay';
  overlay.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
  `;

  document.body.appendChild(overlay);
  document.body.appendChild(modal);

  function closeModal() {
    modal.remove();
    overlay.remove();
  }

  document.getElementById('close-shortcuts').addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}

// Initialize tooltips
function initializeTooltips() {
  const elements = document.querySelectorAll('[data-tooltip]');

  elements.forEach(function(element) {
    element.style.position = 'relative';
    element.style.cursor = 'help';

    element.addEventListener('mouseenter', function() {
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip';
      tooltip.textContent = element.getAttribute('data-tooltip');
      tooltip.style.cssText = `
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 0.5rem;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        border-radius: 0.25rem;
        font-size: 0.85rem;
        white-space: nowrap;
        z-index: 1000;
        margin-bottom: 0.5rem;
      `;

      element.appendChild(tooltip);
    });

    element.addEventListener('mouseleave', function() {
      const tooltip = element.querySelector('.tooltip');
      if (tooltip) {
        tooltip.remove();
      }
    });
  });
}

// Track popular searches
function trackSearches() {
  const searchInput = document.querySelector('.md-search__input');

  if (!searchInput) {
    return;
  }

  searchInput.addEventListener('change', function() {
    const query = this.value.trim();

    if (query) {
      // Store in localStorage
      const searches = JSON.parse(localStorage.getItem('bp-searches') || '[]');

      // Add new search
      searches.unshift({
        query: query,
        timestamp: Date.now()
      });

      // Keep only last 50 searches
      const recentSearches = searches.slice(0, 50);

      localStorage.setItem('bp-searches', JSON.stringify(recentSearches));
    }
  });
}

// Get popular searches
function getPopularSearches() {
  const searches = JSON.parse(localStorage.getItem('bp-searches') || '[]');

  // Count occurrences
  const counts = {};
  searches.forEach(function(search) {
    counts[search.query] = (counts[search.query] || 0) + 1;
  });

  // Sort by count
  const popular = Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(entry => entry[0]);

  return popular;
}

// Export for use in other scripts
window.bpDocs = {
  getPopularSearches: getPopularSearches,
  trackSearchPerformance: trackSearchPerformance
};
