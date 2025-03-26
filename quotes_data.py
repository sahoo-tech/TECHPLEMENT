import csv
import os
from collections import defaultdict

# Initialize the quotes database and index
QUOTES_DATABASE = [
    # Technology Leaders
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "Technology"
    },
    {
        "text": "Innovation distinguishes between a leader and a follower.",
        "author": "Steve Jobs",
        "category": "Technology"
    },
    {
        "text": "The future of AI is not about replacing humans, but augmenting them.",
        "author": "Satya Nadella",
        "category": "Technology"
    },
    {
        "text": "Technology is best when it brings people together.",
        "author": "Matt Mullenweg",
        "category": "Technology"
    },
    
    # Business Leaders
    {
        "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "author": "Winston Churchill",
        "category": "Business"
    },
    {
        "text": "The best way to predict the future is to create it.",
        "author": "Peter Drucker",
        "category": "Business"
    },
    {
        "text": "Your time is limited, don't waste it living someone else's life.",
        "author": "Steve Jobs",
        "category": "Business"
    },
    {
        "text": "The only sustainable competitive advantage is an organization's ability to learn faster than the competition.",
        "author": "Peter Senge",
        "category": "Business"
    },
    
    # Modern Entrepreneurs
    {
        "text": "Move fast and break things.",
        "author": "Mark Zuckerberg",
        "category": "Entrepreneurship"
    },
    {
        "text": "The biggest risk is not taking any risk.",
        "author": "Mark Zuckerberg",
        "category": "Entrepreneurship"
    },
    {
        "text": "If you're not embarrassed by the first version of your product, you've launched too late.",
        "author": "Reid Hoffman",
        "category": "Entrepreneurship"
    },
    {
        "text": "The best entrepreneurs I know are all good at not just seeing things as they are, but seeing things as they could be.",
        "author": "Sam Altman",
        "category": "Entrepreneurship"
    },
    
    # Personal Development
    {
        "text": "The only person you are destined to become is the person you decide to be.",
        "author": "Ralph Waldo Emerson",
        "category": "Personal Growth"
    },
    {
        "text": "The journey of a thousand miles begins with one step.",
        "author": "Lao Tzu",
        "category": "Personal Growth"
    },
    {
        "text": "The best way to find yourself is to lose yourself in the service of others.",
        "author": "Mahatma Gandhi",
        "category": "Personal Growth"
    },
    {
        "text": "The only true wisdom is in knowing you know nothing.",
        "author": "Socrates",
        "category": "Personal Growth"
    },
    
    # Modern Thought Leaders
    {
        "text": "The future belongs to those who prepare for it today.",
        "author": "Malcolm X",
        "category": "Leadership"
    },
    {
        "text": "The best way to predict the future is to study the past.",
        "author": "Sun Tzu",
        "category": "Leadership"
    },
    {
        "text": "The only way to have a good day is to start it with a positive attitude.",
        "author": "Unknown",
        "category": "Motivation"
    },
    {
        "text": "The best way to find happiness is to stop looking for it.",
        "author": "Unknown",
        "category": "Motivation"
    },
    
    # Innovation & Creativity
    {
        "text": "Everything you can imagine is real.",
        "author": "Pablo Picasso",
        "category": "Creativity"
    },
    {
        "text": "The best way to learn is to teach.",
        "author": "Unknown",
        "category": "Education"
    },
    {
        "text": "The only way to be truly satisfied is to do what you believe is great work.",
        "author": "Steve Jobs",
        "category": "Work"
    },
    
    # Modern Tech Visionaries
    {
        "text": "AI is the new electricity.",
        "author": "Andrew Ng",
        "category": "Technology"
    },
    {
        "text": "The future of work is not about jobs, it's about tasks.",
        "author": "Thomas Frey",
        "category": "Future"
    },
    {
        "text": "The best way to predict the future is to invent it.",
        "author": "Alan Kay",
        "category": "Technology"
    },
    {
        "text": "The future is already here – it's just not evenly distributed.",
        "author": "William Gibson",
        "category": "Future"
    },

    # Additional Quotes - Indian Wisdom
    {
        "text": "You must be the change you wish to see in the world.",
        "author": "Mahatma Gandhi",
        "category": "Indian Wisdom"
    },
    {
        "text": "The truth is not something outside to be discovered, it is something inside to be realized.",
        "author": "Osho",
        "category": "Indian Wisdom"
    },
    {
        "text": "The greatest meditation is a mind that lets go.",
        "author": "Patrul Rinpoche",
        "category": "Indian Wisdom"
    },
    {
        "text": "When you compete with others, you become bitter. When you compete with yourself, you become better.",
        "author": "Unknown",
        "category": "Indian Wisdom"
    },

    # Additional Quotes - Science & Discovery
    {
        "text": "The important thing is not to stop questioning. Curiosity has its own reason for existence.",
        "author": "Albert Einstein",
        "category": "Science"
    },
    {
        "text": "The good thing about science is that it's true whether or not you believe in it.",
        "author": "Neil deGrasse Tyson",
        "category": "Science"
    },
    {
        "text": "The most beautiful experience we can have is the mysterious.",
        "author": "Albert Einstein",
        "category": "Science"
    },
    {
        "text": "Science is not only compatible with spirituality; it is a profound source of spirituality.",
        "author": "Carl Sagan",
        "category": "Science"
    },

    # Additional Quotes - Literature & Arts
    {
        "text": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.",
        "author": "Ralph Waldo Emerson",
        "category": "Literature"
    },
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "Literature"
    },
    {
        "text": "Art washes away from the soul the dust of everyday life.",
        "author": "Pablo Picasso",
        "category": "Arts"
    },
    {
        "text": "The purpose of art is washing the dust of daily life off our souls.",
        "author": "Pablo Picasso",
        "category": "Arts"
    },

    # Additional Quotes - Philosophy & Ethics
    {
        "text": "The unexamined life is not worth living.",
        "author": "Socrates",
        "category": "Philosophy"
    },
    {
        "text": "Happiness is not something ready made. It comes from your own actions.",
        "author": "Dalai Lama",
        "category": "Philosophy"
    },
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "Philosophy"
    },
    {
        "text": "The journey of a thousand miles begins with one step.",
        "author": "Lao Tzu",
        "category": "Philosophy"
    },

    # Additional Quotes - Success & Achievement
    {
        "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "author": "Winston Churchill",
        "category": "Success"
    },
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "Success"
    },
    {
        "text": "Success is walking from failure to failure with no loss of enthusiasm.",
        "author": "Winston Churchill",
        "category": "Success"
    },
    {
        "text": "The road to success and the road to failure are almost exactly the same.",
        "author": "Colin R. Davis",
        "category": "Success"
    }
]

QUOTES_INDEX = {
    'by_author': defaultdict(list),
    'by_category': defaultdict(list),
    'by_text': defaultdict(list)
}

def load_quotes_from_csv():
    try:
        # Load quotes from the CSV file
        with open('quotes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                quote_data = {
                    'text': row['quote'],
                    'author': row['author'],
                    'category': row.get('category', 'General')
                }
                QUOTES_DATABASE.append(quote_data)
                
                # Index by author (case-insensitive)
                author = row['author'].lower()
                QUOTES_INDEX['by_author'][author].append(quote_data)
                
                # Index by category
                category = row.get('category', 'General').lower()
                QUOTES_INDEX['by_category'][category].append(quote_data)
                
                # Index by text keywords
                for word in row['quote'].lower().split():
                    if len(word) > 2:  # Only index words longer than 2 characters
                        QUOTES_INDEX['by_text'][word].append(quote_data)
        
        print(f"Successfully loaded {len(QUOTES_DATABASE)} quotes from CSV")
    except FileNotFoundError:
        print("quotes.csv not found. Using default quotes.")
        # Fallback to default quotes if CSV is not found
        default_quotes = [
            {
                "text": "The only way to do great work is to love what you do.",
                "author": "Steve Jobs",
                "category": "Technology"
            },
            {
                "text": "Innovation distinguishes between a leader and a follower.",
                "author": "Steve Jobs",
                "category": "Technology"
            },
            {
                "text": "The future of AI is not about replacing humans, but augmenting them.",
                "author": "Satya Nadella",
                "category": "Technology"
            },
            {
                "text": "Technology is best when it brings people together.",
                "author": "Matt Mullenweg",
                "category": "Technology"
            },
            {
                "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                "author": "Winston Churchill",
                "category": "Business"
            }
        ]
        
        # Add default quotes to database and index
        for quote_data in default_quotes:
            QUOTES_DATABASE.append(quote_data)
            
            # Index by author
            author = quote_data['author'].lower()
            QUOTES_INDEX['by_author'][author].append(quote_data)
            
            # Index by category
            category = quote_data['category'].lower()
            QUOTES_INDEX['by_category'][category].append(quote_data)
            
            # Index by text keywords
            for word in quote_data['text'].lower().split():
                if len(word) > 2:
                    QUOTES_INDEX['by_text'][word].append(quote_data)
        
        print(f"Using {len(QUOTES_DATABASE)} default quotes")
    except Exception as e:
        print(f"Error loading quotes: {str(e)}")
        # Use the same default quotes as above
        default_quotes = [
            {
                "text": "The only way to do great work is to love what you do.",
                "author": "Steve Jobs",
                "category": "Technology"
            },
            {
                "text": "Innovation distinguishes between a leader and a follower.",
                "author": "Steve Jobs",
                "category": "Technology"
            },
            {
                "text": "The future of AI is not about replacing humans, but augmenting them.",
                "author": "Satya Nadella",
                "category": "Technology"
            },
            {
                "text": "Technology is best when it brings people together.",
                "author": "Matt Mullenweg",
                "category": "Technology"
            },
            {
                "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                "author": "Winston Churchill",
                "category": "Business"
            }
        ]
        
        # Add default quotes to database and index
        for quote_data in default_quotes:
            QUOTES_DATABASE.append(quote_data)
            
            # Index by author
            author = quote_data['author'].lower()
            QUOTES_INDEX['by_author'][author].append(quote_data)
            
            # Index by category
            category = quote_data['category'].lower()
            QUOTES_INDEX['by_category'][category].append(quote_data)
            
            # Index by text keywords
            for word in quote_data['text'].lower().split():
                if len(word) > 2:
                    QUOTES_INDEX['by_text'][word].append(quote_data)
        
        print(f"Using {len(QUOTES_DATABASE)} default quotes")

# Load quotes when the module is imported
load_quotes_from_csv()

# Create a search index for faster lookups
QUOTES_INDEX = {
    'by_author': {},
    'by_category': {},
    'by_text': {}
}

# Build search indices
seen_quotes = set()  # Track unique quotes
for quote in QUOTES_DATABASE:
    quote_key = (quote['text'], quote['author'])
    if quote_key in seen_quotes:
        continue
        
    # Index by author
    author = quote['author'].lower()
    if author not in QUOTES_INDEX['by_author']:
        QUOTES_INDEX['by_author'][author] = []
    QUOTES_INDEX['by_author'][author].append(quote)
    
    # Index by category
    category = quote['category'].lower()
    if category not in QUOTES_INDEX['by_category']:
        QUOTES_INDEX['by_category'][category] = []
    QUOTES_INDEX['by_category'][category].append(quote)
    
    # Index by text keywords
    for word in quote['text'].lower().split():
        if word not in QUOTES_INDEX['by_text']:
            QUOTES_INDEX['by_text'][word] = []
        QUOTES_INDEX['by_text'][word].append(quote)
    
    seen_quotes.add(quote_key) 