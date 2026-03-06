from django.contrib import admin
from .models import FAQCategory, FAQ, ChatSession, ChatMessage

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'times_asked', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'keywords']
    readonly_fields = ['preprocessed_question', 'times_asked']
    fieldsets = (
        ('FAQ Information', {
            'fields': ('category', 'question', 'answer', 'keywords')
        }),
        ('Metadata', {
            'fields': ('is_active', 'times_asked', 'preprocessed_question'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Preprocess question before saving
        if not obj.preprocessed_question:
            from .nlp_processor import nlp_processor
            obj.preprocessed_question = nlp_processor.preprocess_text(obj.question)
        super().save_model(request, obj, form, change)

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'last_activity']
    readonly_fields = ['session_id']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'is_user', 'message', 'created_at']
    list_filter = ['is_user', 'created_at']
    search_fields = ['message']