from django.db import models
from django.utils import timezone

class FAQCategory(models.Model):
    """Category for organizing FAQs"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "FAQ Categories"
    
    def __str__(self):
        return self.name

class FAQ(models.Model):
    """FAQ model storing questions and answers"""
    category = models.ForeignKey(
        FAQCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='faqs'
    )
    question = models.TextField()
    answer = models.TextField()
    keywords = models.TextField(
        help_text="Comma-separated keywords for better matching",
        blank=True
    )
    preprocessed_question = models.TextField(
        help_text="Preprocessed version of the question for matching",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    times_asked = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-times_asked', '-created_at']
    
    def __str__(self):
        return self.question[:50]

class ChatSession(models.Model):
    """Track chat sessions for analytics"""
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Session {self.session_id} - {self.created_at}"

class ChatMessage(models.Model):
    """Store chat messages for analytics"""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_user = models.BooleanField(default=True)  # True if user message, False if bot response
    message = models.TextField()
    matched_faq = models.ForeignKey(FAQ, on_delete=models.SET_NULL, null=True, blank=True)
    similarity_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']