from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime
import os
from quotes_data import QUOTES_DATABASE, QUOTES_INDEX

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)  # Made nullable to handle existing records
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': self.author,
            'category': self.category,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

def get_random_quote():
    try:
        # First try to get a quote from the database
        quote = Quote.query.order_by(db.func.random()).first()
        if quote:
            return quote.to_dict()
    except Exception as e:
        print(f"Error getting random quote from database: {str(e)}")
    
    # Fallback to in-memory database if there's an error
    return random.choice(QUOTES_DATABASE)

def search_quotes_by_author(author_query):
    if not author_query:
        return []
        
    author_query = author_query.lower().strip()
    matching_quotes = []
    
    try:
        # First try to get quotes from the database
        quotes = Quote.query.filter(
            db.func.lower(Quote.author) == author_query
        ).all()
        
        if quotes:
            matching_quotes = [quote.to_dict() for quote in quotes]
        else:
            # Fallback to in-memory index if no database results
            if author_query in QUOTES_INDEX['by_author']:
                matching_quotes = QUOTES_INDEX['by_author'][author_query]
            
            # If still no results, try partial matching
            if not matching_quotes:
                # Try to find authors that contain the query
                partial_matches = Quote.query.filter(
                    db.func.lower(Quote.author).like(f'%{author_query}%')
                ).all()
                
                if partial_matches:
                    matching_quotes = [quote.to_dict() for quote in partial_matches]
                else:
                    # Try the in-memory index for partial matches
                    for author, quotes in QUOTES_INDEX['by_author'].items():
                        if author_query in author:
                            matching_quotes.extend(quotes)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_quotes = []
        for quote in matching_quotes:
            quote_key = (quote['text'], quote['author'])
            if quote_key not in seen:
                seen.add(quote_key)
                unique_quotes.append(quote)
        
        return unique_quotes
    except Exception as e:
        print(f"Search error: {str(e)}")
        # Fallback to in-memory index if database query fails
        if author_query in QUOTES_INDEX['by_author']:
            return QUOTES_INDEX['by_author'][author_query]
        return []

def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning! Have a wonderful day ahead!"
    elif 12 <= hour < 17:
        return "Good afternoon! Hope you're having a great day!"
    elif 17 <= hour < 22:
        return "Good evening! Welcome to your daily dose of inspiration!"
    else:
        return "Good night! Time for some peaceful thoughts!"

@app.route('/')
def greeting():
    return render_template('greeting.html',
                         greeting="Namaste! Welcome to Quote of the Day",
                         time_based_greeting=get_time_based_greeting())

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/api/quote/random')
def random_quote():
    try:
        quote_data = get_random_quote()
        quote = Quote(
            text=quote_data['text'],
            author=quote_data['author'],
            category=quote_data.get('category', 'General')
        )
        db.session.add(quote)
        db.session.commit()
        return jsonify(quote.to_dict())
    except Exception as e:
        print(f"Random quote error: {str(e)}")
        return jsonify({
            'text': 'The best way to predict the future is to create it.',
            'author': 'Peter Drucker',
            'category': 'General'
        })

@app.route('/api/quote/search')
def search_quotes():
    try:
        author = request.args.get('author', '')
        if not author:
            return jsonify([])
        
        matching_quotes = search_quotes_by_author(author)
        if not matching_quotes:
            return jsonify([])  # Return empty list if no matches found
        
        return jsonify(matching_quotes)
    except Exception as e:
        print(f"Search route error: {str(e)}")
        return jsonify([])

def init_db():
    with app.app_context():
        try:
            # Drop all tables to start fresh
            db.drop_all()
            # Create all tables
            db.create_all()
            
            # Populate the database with unique quotes
            seen_quotes = set()
            for quote_data in QUOTES_DATABASE:
                quote_key = (quote_data['text'], quote_data['author'])
                if quote_key not in seen_quotes:
                    quote = Quote(
                        text=quote_data['text'],
                        author=quote_data['author'],
                        category=quote_data.get('category', 'General')
                    )
                    db.session.add(quote)
                    seen_quotes.add(quote_key)
            
            db.session.commit()
            print(f"Successfully initialized database with {len(seen_quotes)} unique quotes")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    # Initialize the database with the new schema
    init_db()
    app.run(debug=True) 