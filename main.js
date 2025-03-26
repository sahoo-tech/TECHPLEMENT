document.addEventListener('DOMContentLoaded', () => {
    const quoteText = document.getElementById('quote-text');
    const quoteAuthor = document.getElementById('quote-author');
    const quoteContent = document.querySelector('.quote-content');
    const prevBtn = document.getElementById('prev-quote');
    const nextBtn = document.getElementById('next-quote');
    const authorSearch = document.getElementById('author-search');
    const searchBtn = document.getElementById('search-btn');
    const searchResults = document.getElementById('search-results');

    let currentQuote = null;
    let shownQuotes = new Set(); // Track shown quotes
    let autoSlideInterval;
    const SLIDE_INTERVAL = 5000; // 5 seconds

    // Function to update quote display
    function updateQuoteDisplay(quote) {
        quoteText.textContent = quote.text;
        quoteAuthor.textContent = `- ${quote.author}`;
        currentQuote = quote;
        
        // Add quote to shown quotes set
        const quoteKey = `${quote.text}-${quote.author}`;
        shownQuotes.add(quoteKey);
    }

    // Function to slide quote
    function slideQuote(direction) {
        // Clear the auto-slide interval when user interacts
        clearInterval(autoSlideInterval);
        
        // Add slide animation class
        quoteContent.classList.add(direction === 'left' ? 'slide-left' : 'slide-right');
        
        // Fetch new quote
        fetchRandomQuote().then(quote => {
            // Update content after animation
            setTimeout(() => {
                updateQuoteDisplay(quote);
                quoteContent.classList.remove('slide-left', 'slide-right');
            }, 500);
        }).catch(error => {
            console.error('Error in slideQuote:', error);
            // Fallback quote if something goes wrong
            const fallbackQuote = {
                text: 'The best way to predict the future is to create it.',
                author: 'Peter Drucker'
            };
            setTimeout(() => {
                updateQuoteDisplay(fallbackQuote);
                quoteContent.classList.remove('slide-left', 'slide-right');
            }, 500);
        });
    }

    // Function to fetch and display a random quote
    async function fetchRandomQuote(retryCount = 0) {
        try {
            const response = await fetch('/api/quote/random');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            
            // Check if this quote has been shown before
            const quoteKey = `${data.text}-${data.author}`;
            if (shownQuotes.has(quoteKey)) {
                // If we've tried too many times, clear the shown quotes set and use this quote
                if (retryCount >= 5) {
                    shownQuotes.clear(); // Reset the shown quotes set
                    return data;
                }
                // If shown before, fetch another quote with increased retry count
                return fetchRandomQuote(retryCount + 1);
            }
            
            return data;
        } catch (error) {
            console.error('Error fetching quote:', error);
            return {
                text: 'Error loading quote. Please try again.',
                author: 'System'
            };
        }
    }

    // Function to start auto-sliding
    function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
            slideQuote('left');
        }, SLIDE_INTERVAL);
    }

    // Function to search quotes by author
    async function searchQuotes() {
        const author = authorSearch.value.trim();
        if (!author) {
            searchResults.innerHTML = '<p>Please enter an author name to search.</p>';
            return;
        }

        searchBtn.classList.add('loading');
        searchBtn.textContent = '';

        try {
            const response = await fetch(`/api/quote/search?author=${encodeURIComponent(author)}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            
            searchResults.innerHTML = '';
            if (!data || data.length === 0) {
                searchResults.innerHTML = `
                    <div class="no-results">
                        <p>No quotes found for "${author}".</p>
                        <p>Please check the spelling or try a different author.</p>
                    </div>`;
                return;
            }

            data.forEach((quote, index) => {
                const quoteElement = document.createElement('div');
                quoteElement.className = 'search-result-item';
                quoteElement.style.animationDelay = `${index * 0.1}s`;
                quoteElement.innerHTML = `
                    <p class="quote-text">${quote.text}</p>
                    <p class="quote-author">- ${quote.author}</p>
                    ${quote.category ? `<p class="quote-category">Category: ${quote.category}</p>` : ''}
                `;
                searchResults.appendChild(quoteElement);
            });
        } catch (error) {
            console.error('Error searching quotes:', error);
            searchResults.innerHTML = '<p>Error searching quotes. Please try again.</p>';
        } finally {
            searchBtn.classList.remove('loading');
            searchBtn.textContent = 'Search';
        }
    }

    // Event listeners
    prevBtn.addEventListener('click', () => slideQuote('right'));
    nextBtn.addEventListener('click', () => slideQuote('left'));
    searchBtn.addEventListener('click', searchQuotes);
    authorSearch.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchQuotes();
        }
    });

    // Initialize with first quote and start auto-sliding
    fetchRandomQuote().then(quote => {
        updateQuoteDisplay(quote);
        startAutoSlide();
    });
}); 