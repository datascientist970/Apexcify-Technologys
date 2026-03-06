import uuid
from .models import ChatSession, ChatMessage

def get_or_create_session(request):
    """
    Get or create a chat session from request
    """
    session_id = request.session.get('chat_session_id')
    
    if session_id:
        try:
            session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            session = create_new_session(request)
    else:
        session = create_new_session(request)
    
    return session

def create_new_session(request):
    """
    Create a new chat session
    """
    session_id = str(uuid.uuid4())
    session = ChatSession.objects.create(session_id=session_id)
    request.session['chat_session_id'] = session_id
    return session

def save_chat_message(session, is_user, message, matched_faq=None, similarity_score=0):
    """
    Save a chat message to the database
    """
    return ChatMessage.objects.create(
        session=session,
        is_user=is_user,
        message=message,
        matched_faq=matched_faq,
        similarity_score=similarity_score
    )