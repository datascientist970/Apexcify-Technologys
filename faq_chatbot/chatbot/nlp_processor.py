import re
import nltk
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

class NLPProcessor:
    """Handle all NLP preprocessing and matching"""
    
    def __init__(self):
        """Initialize NLP components"""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Try to load spaCy model for better processing
        try:
            self.nlp = spacy.load('en_core_web_sm')
            self.use_spacy = True
        except:
            self.use_spacy = False
            print("Spacy model not found. Using NLTK only.")
        
        # Cache for vectorizer and vectors
        self.vectorizer = None
        self.faq_vectors = None
        self.faqs = None
    
    def preprocess_text(self, text):
        """
        Preprocess text by cleaning, tokenizing, and lemmatizing
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        if self.use_spacy:
            # Use spaCy for advanced preprocessing
            doc = self.nlp(text)
            tokens = [token.lemma_ for token in doc 
                     if not token.is_stop and not token.is_punct]
        else:
            # Use NLTK for basic preprocessing
            tokens = word_tokenize(text)
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                     if token not in self.stop_words]
        
        return ' '.join(tokens)
    
    def extract_keywords(self, text, top_n=5):
        """
        Extract important keywords from text
        """
        if self.use_spacy:
            doc = self.nlp(text)
            # Extract nouns and proper nouns as keywords
            keywords = [token.text for token in doc 
                       if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop]
            return keywords[:top_n]
        else:
            # Simple frequency-based keyword extraction
            words = word_tokenize(text.lower())
            words = [w for w in words if w not in self.stop_words and len(w) > 2]
            freq_dist = nltk.FreqDist(words)
            return [word for word, _ in freq_dist.most_common(top_n)]
    
    def prepare_faqs(self, faqs):
        """
        Prepare FAQs for matching by preprocessing and vectorizing
        """
        self.faqs = faqs
        
        # Preprocess all questions
        preprocessed_questions = []
        for faq in faqs:
            if not faq.preprocessed_question:
                # Preprocess and save for future use
                preprocessed = self.preprocess_text(faq.question)
                faq.preprocessed_question = preprocessed
                faq.save()
            else:
                preprocessed = faq.preprocessed_question
            
            # Add keywords to improve matching
            if faq.keywords:
                preprocessed += " " + faq.keywords.lower()
            
            preprocessed_questions.append(preprocessed)
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)  # Use unigrams and bigrams
        )
        
        # Vectorize questions
        self.faq_vectors = self.vectorizer.fit_transform(preprocessed_questions)
        
        return preprocessed_questions
    
    def find_best_match(self, user_question, threshold=0.3, top_n=3):
        """
        Find the best matching FAQ for a user question
        """
        if not self.faqs or self.faq_vectors is None:
            return []
        
        # Preprocess user question
        processed_question = self.preprocess_text(user_question)
        
        # Vectorize user question
        question_vector = self.vectorizer.transform([processed_question])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(question_vector, self.faq_vectors).flatten()
        
        # Get top matches above threshold
        matches = []
        for idx, score in enumerate(similarities):
            if score >= threshold:
                matches.append({
                    'faq': self.faqs[idx],
                    'score': score,
                    'question': self.faqs[idx].question,
                    'answer': self.faqs[idx].answer
                })
        
        # Sort by similarity score
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        return matches[:top_n]
    
    def get_response(self, user_question, threshold=0.3):
        """
        Get the best response for a user question
        """
        print(f"\n[NLP] Getting response for: '{user_question}'")
        print(f"[NLP] Threshold: {threshold}")
        print(f"[NLP] Number of FAQs: {len(self.faqs) if self.faqs else 0}")
        
        matches = self.find_best_match(user_question, threshold)
        
        print(f"[NLP] Found {len(matches)} matches")
        
        if matches:
            best_match = matches[0]
            print(f"[NLP] Best match: '{best_match['question']}' with score {best_match['score']}")
            
            # Update times asked
            try:
                if best_match['faq']:
                    best_match['faq'].times_asked += 1
                    best_match['faq'].save()
                    print(f"[NLP] Updated times_asked for FAQ ID {best_match['faq'].id}")
            except Exception as e:
                print(f"[NLP] Error updating times_asked: {str(e)}")
            
            return {
                'answer': best_match['answer'],
                'confidence': float(best_match['score']),
                'matches': matches,
                'found': True
            }
        else:
            print(f"[NLP] No matches found")
            return {
                'answer': "I'm sorry, I don't have an answer for that question. Please try rephrasing or contact support.",
                'confidence': 0.0,
                'matches': [],
                'found': False
            }
# Create a singleton instance
nlp_processor = NLPProcessor()