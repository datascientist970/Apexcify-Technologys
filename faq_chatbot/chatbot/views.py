from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging
from django.conf import settings
import json
from .models import FAQ, FAQCategory, ChatSession
from .nlp_processor import nlp_processor
from .utils import get_or_create_session, save_chat_message
logger = logging.getLogger(__name__)


def index(request):
    """Home page view"""
    return render(request, 'chatbot/index.html')


def test_nlp(request):
    """Simple test view to verify NLP is working"""
    from .nlp_processor import nlp_processor
    
    # Get some FAQs
    faqs = list(FAQ.objects.filter(is_active=True)[:5])
    
    if not faqs:
        return HttpResponse("No FAQs found. Please add some FAQs first.")
    
    # Test preprocessing
    test_text = "Can I track my order?"
    preprocessed = nlp_processor.preprocess_text(test_text)
    
    # Test matching
    nlp_processor.prepare_faqs(faqs)
    matches = nlp_processor.find_best_match(test_text)
    
    result = f"""
    <h1>NLP Test Results</h1>
    <h2>Test Query: "{test_text}"</h2>
    <p><strong>Preprocessed:</strong> {preprocessed}</p>
    
    <h2>Matches Found: {len(matches)}</h2>
    """
    
    for i, match in enumerate(matches):
        result += f"""
        <div style="border:1px solid #ccc; margin:10px; padding:10px;">
            <h3>Match {i+1} (Score: {match['score']:.3f})</h3>
            <p><strong>Question:</strong> {match['question']}</p>
            <p><strong>Answer:</strong> {match['answer']}</p>
        </div>
        """
    
    return HttpResponse(result)

def chat_interface(request):
    """Main chat interface"""
    # Get or create chat session
    session = get_or_create_session(request)
    
    # Get recent messages
    recent_messages = session.messages.all()[:50]
    
    context = {
        'recent_messages': recent_messages,
        'total_faqs': FAQ.objects.filter(is_active=True).count(),
    }
    return render(request, 'chatbot/chat_interface.html', context)

@csrf_exempt
def process_message(request):
    """Process user message and return bot response"""
    if request.method == 'POST':
        try:
            # Log the request
            logger.info("=" * 50)
            logger.info("Processing message request")
            
            # Parse request body
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            logger.info(f"User message: '{user_message}'")
            
            if not user_message:
                logger.warning("Empty message received")
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Get or create session
            session = get_or_create_session(request)
            logger.info(f"Session ID: {session.session_id}")
            
            # Save user message
            save_chat_message(session, True, user_message)
            
            # Get all active FAQs
            faqs = list(FAQ.objects.filter(is_active=True))
            logger.info(f"Found {len(faqs)} active FAQs")
            
            if not faqs:
                logger.warning("No FAQs found in database")
                response_data = {
                    'answer': "I don't have any FAQs in my database yet. Please add some FAQs first.",
                    'confidence': 0,
                    'found': False,
                    'matches': []
                }
            else:
                # Log the FAQs for debugging
                for i, faq in enumerate(faqs[:3]):  # Log first 3 FAQs
                    logger.info(f"FAQ {i+1}: {faq.question[:50]}...")
                
                # Prepare FAQs for matching
                logger.info("Preparing FAQs for matching...")
                nlp_processor.prepare_faqs(faqs)
                
                # Get response
                logger.info(f"Getting response for: '{user_message}'")
                result = nlp_processor.get_response(
                    user_message, 
                    threshold=settings.CHATBOT_SIMILARITY_THRESHOLD
                )
                
                logger.info(f"Result from NLP: {result}")
                
                # Format matches for frontend
                matches = []
                for match in result.get('matches', []):
                    matches.append({
                        'question': match.get('question', ''),
                        'answer': match.get('answer', ''),
                        'score': float(match.get('score', 0))
                    })
                
                response_data = {
                    'answer': result.get('answer', 'Sorry, I could not find an answer.'),
                    'confidence': float(result.get('confidence', 0)),
                    'found': result.get('found', False),
                    'matches': matches
                }
            
            logger.info(f"Response data: {response_data}")
            
            # Save bot response
            matched_faq = None
            if response_data.get('matches') and len(response_data['matches']) > 0:
                try:
                    best_match_question = response_data['matches'][0]['question']
                    matched_faq = FAQ.objects.filter(question=best_match_question).first()
                    logger.info(f"Matched FAQ: {matched_faq}")
                except Exception as e:
                    logger.error(f"Error finding matched FAQ: {str(e)}")
            
            save_chat_message(
                session, 
                False, 
                response_data['answer'], 
                matched_faq, 
                response_data['confidence']
            )
            
            logger.info("Response sent successfully")
            return JsonResponse(response_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    
    logger.warning(f"Invalid request method: {request.method}")
    return JsonResponse({'error': 'Invalid request method'}, status=405)

