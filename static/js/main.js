// Modern Documentation Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Show loading indicator
    showLoadingState();
    
    // Initialize all features
    Promise.all([
        initializeSearch(),
        initializeMobileMenu(),
        initializeSmoothScrolling(),
        initializeCodeHighlighting(),
        initializeThemeToggle(),
        initializePerformanceMetrics()
    ]).then(() => {
        hideLoadingState();
        // Fade in content
        document.body.classList.add('loaded');
    }).catch(error => {
        console.error('Initialization error:', error);
        hideLoadingState();
    });
});

// Performance metrics and loading states
function initializePerformanceMetrics() {
    return new Promise((resolve) => {
        // Track page load performance
        window.addEventListener('load', () => {
            if ('performance' in window) {
                const perfData = performance.getEntriesByType('navigation')[0];
                const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                const domContentTime = perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart;
                
                console.log('Performance Metrics:', {
                    loadTime: `${loadTime.toFixed(2)}ms`,
                    domContentTime: `${domContentTime.toFixed(2)}ms`,
                    totalTime: `${perfData.loadEventEnd - perfData.fetchStart}ms`
                });
                
                // Add performance indicator for debugging
                if (localStorage.getItem('showPerformance') === 'true') {
                    showPerformanceIndicator(loadTime);
                }
            }
            resolve();
        });
    });
}

function showPerformanceIndicator(loadTime) {
    const indicator = document.createElement('div');
    indicator.className = 'performance-indicator';
    indicator.innerHTML = `
        <div class="perf-metric">
            <span class="perf-label">Load Time:</span>
            <span class="perf-value">${loadTime.toFixed(0)}ms</span>
        </div>
    `;
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.classList.add('fade-out');
        setTimeout(() => indicator.remove(), 2000);
    }, 3000);
}

function showLoadingState() {
    const loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.innerHTML = `
        <div class="loader-content">
            <div class="loader-spinner"></div>
            <div class="loader-text">Loading...</div>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoadingState() {
    const loader = document.getElementById('page-loader');
    if (loader) {
        loader.classList.add('fade-out');
        setTimeout(() => loader.remove(), 500);
    }
}

function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Hide search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}

function performSearch(query) {
    const searchResults = document.getElementById('search-results');
    
    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(results => {
            displaySearchResults(results);
        })
        .catch(error => {
            console.error('Search error:', error);
            searchResults.style.display = 'none';
        });
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('search-results');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-result">No results found</div>';
        searchResults.style.display = 'block';
        return;
    }
    
    const html = results.map(result => `
        <a href="/docs/${result.slug}" class="search-result">
            <strong>${result.title}</strong>
            <small class="text-muted d-block">${result.section}</small>
        </a>
    `).join('');
    
    searchResults.innerHTML = html;
    searchResults.style.display = 'block';
}

function initializeMobileMenu() {
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const sidebar = document.querySelector('.docs-sidebar');
    const overlay = document.getElementById('mobile-overlay');
    
    if (!mobileToggle || !sidebar) return;
    
    // Enhanced mobile menu with gesture support
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    let isMenuOpen = false;
    
    mobileToggle.addEventListener('click', function() {
        isMenuOpen ? closeMobileMenu() : openMobileMenu();
    });
    
    // Touch gesture support for sidebar
    if (overlay) {
        overlay.addEventListener('click', closeMobileMenu);
        
        // Swipe to close gesture
        overlay.addEventListener('touchstart', handleTouchStart, { passive: true });
        overlay.addEventListener('touchmove', handleTouchMove, { passive: true });
        overlay.addEventListener('touchend', handleTouchEnd, { passive: true });
    }
    
    // Swipe from edge to open gesture
    document.addEventListener('touchstart', handleEdgeSwipe, { passive: true });
    document.addEventListener('touchmove', handleEdgeMove, { passive: true });
    document.addEventListener('touchend', handleEdgeEnd, { passive: true });
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isMenuOpen) {
            closeMobileMenu();
        }
    });
    
    // Close on window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && isMenuOpen) {
            closeMobileMenu();
        }
    });
    
    function handleTouchStart(e) {
        startX = e.touches[0].clientX;
        isDragging = true;
    }
    
    function handleTouchMove(e) {
        if (!isDragging) return;
        currentX = e.touches[0].clientX;
        const diffX = currentX - startX;
        
        // Only allow swipe to close (left swipe)
        if (diffX < -50 && isMenuOpen) {
            const opacity = Math.max(0, 1 - Math.abs(diffX) / 200);
            overlay.style.opacity = opacity;
        }
    }
    
    function handleTouchEnd(e) {
        if (!isDragging) return;
        isDragging = false;
        
        const diffX = currentX - startX;
        if (diffX < -100 && isMenuOpen) {
            closeMobileMenu();
        } else if (overlay) {
            overlay.style.opacity = '';
        }
    }
    
    function handleEdgeSwipe(e) {
        if (window.innerWidth > 768 || isMenuOpen) return;
        
        const touch = e.touches[0];
        if (touch.clientX < 20) { // Edge swipe area
            startX = touch.clientX;
            isDragging = true;
        }
    }
    
    function handleEdgeMove(e) {
        if (!isDragging || isMenuOpen || window.innerWidth > 768) return;
        
        currentX = e.touches[0].clientX;
        const diffX = currentX - startX;
        
        if (diffX > 50) {
            // Preview opening
            const progress = Math.min(diffX / 200, 0.3);
            sidebar.style.transform = `translateX(${-100 + progress * 100}%)`;
            if (overlay) {
                overlay.style.opacity = progress;
                overlay.style.display = 'block';
            }
        }
    }
    
    function handleEdgeEnd(e) {
        if (!isDragging || window.innerWidth > 768) return;
        isDragging = false;
        
        const diffX = currentX - startX;
        if (diffX > 150) {
            openMobileMenu();
        } else {
            // Reset sidebar position
            sidebar.style.transform = '';
            if (overlay) {
                overlay.style.opacity = '';
                overlay.style.display = 'none';
            }
        }
    }
    
    function openMobileMenu() {
        isMenuOpen = true;
        sidebar.classList.add('show');
        sidebar.style.transform = '';
        if (overlay) {
            overlay.classList.add('show');
            overlay.style.opacity = '';
            overlay.style.display = 'block';
        }
        document.body.style.overflow = 'hidden';
        mobileToggle.querySelector('i').className = 'fas fa-times';
        
        // Add animation class
        sidebar.classList.add('opening');
        setTimeout(() => sidebar.classList.remove('opening'), 300);
    }
    
    function closeMobileMenu() {
        isMenuOpen = false;
        sidebar.classList.add('closing');
        sidebar.classList.remove('show');
        if (overlay) {
            overlay.classList.remove('show');
            overlay.style.opacity = '';
        }
        document.body.style.overflow = '';
        mobileToggle.querySelector('i').className = 'fas fa-bars';
        
        setTimeout(() => {
            sidebar.classList.remove('closing');
            sidebar.style.transform = '';
            if (overlay) overlay.style.display = 'none';
        }, 300);
    }
}

function initializeSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeCodeHighlighting() {
    // Add enhanced copy buttons to code blocks
    document.querySelectorAll('pre code').forEach((block) => {
        const pre = block.parentElement;
        
        // Create wrapper for better positioning
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);
        
        // Create copy button with improved styling
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.innerHTML = `
            <svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <svg class="check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
                <polyline points="20,6 9,17 4,12"></polyline>
            </svg>
            <span class="copy-text">Copy</span>
        `;
        
        // Add language label if available
        const language = block.className.match(/language-(\w+)/);
        if (language) {
            const label = document.createElement('span');
            label.className = 'code-language';
            label.textContent = language[1].toUpperCase();
            wrapper.appendChild(label);
        }
        
        wrapper.appendChild(button);
        
        // Enhanced copy functionality
        button.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(block.textContent);
                
                // Animate button state
                const copyIcon = button.querySelector('.copy-icon');
                const checkIcon = button.querySelector('.check-icon');
                const copyText = button.querySelector('.copy-text');
                
                button.classList.add('copied');
                copyIcon.style.display = 'none';
                checkIcon.style.display = 'block';
                copyText.textContent = 'Copied!';
                
                // Reset after 2 seconds
                setTimeout(() => {
                    button.classList.remove('copied');
                    copyIcon.style.display = 'block';
                    checkIcon.style.display = 'none';
                    copyText.textContent = 'Copy';
                }, 2000);
                
            } catch (err) {
                console.error('Failed to copy code:', err);
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = block.textContent;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
            }
        });
        
        // Show/hide button on hover
        wrapper.addEventListener('mouseenter', () => {
            button.style.opacity = '1';
        });
        
        wrapper.addEventListener('mouseleave', () => {
            if (!button.classList.contains('copied')) {
                button.style.opacity = '0.7';
            }
        });
    });
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced theme toggle with animations
function initializeThemeToggle() {
    return new Promise((resolve) => {
        // Create theme toggle button
        const themeToggle = createThemeToggleButton();
        
        // Get saved theme or detect system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const currentTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
        
        // Apply initial theme
        setTheme(currentTheme, false);
        updateToggleButton(themeToggle, currentTheme);
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                const newTheme = e.matches ? 'dark' : 'light';
                setTheme(newTheme, true);
                updateToggleButton(themeToggle, newTheme);
            }
        });
        
        // Handle toggle click
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            setTheme(newTheme, true);
            updateToggleButton(themeToggle, newTheme);
            localStorage.setItem('theme', newTheme);
        });
        
        resolve();
    });
}

function createThemeToggleButton() {
    const themeToggle = document.createElement('button');
    themeToggle.id = 'theme-toggle';
    themeToggle.className = 'theme-toggle';
    themeToggle.setAttribute('aria-label', 'Toggle theme');
    themeToggle.innerHTML = `
        <div class="theme-toggle-track">
            <div class="theme-toggle-thumb">
                <svg class="sun-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
                <svg class="moon-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>
                </svg>
            </div>
        </div>
    `;
    
    // Add to navbar
    const navbar = document.querySelector('.navbar .container');
    if (navbar) {
        navbar.appendChild(themeToggle);
    }
    
    return themeToggle;
}

function setTheme(theme, animate = false) {
    if (animate) {
        // Add transition class for smooth animation
        document.documentElement.classList.add('theme-transition');
        
        // Remove transition class after animation
        setTimeout(() => {
            document.documentElement.classList.remove('theme-transition');
        }, 300);
    }
    
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        metaThemeColor.content = theme === 'dark' ? '#23272f' : '#ffffff';
    }
}

function updateToggleButton(button, theme) {
    const isDark = theme === 'dark';
    button.setAttribute('aria-pressed', isDark);
    button.classList.toggle('dark', isDark);
}
