
from Buyer.models import Chat
from django.db.models import Q
def context_processor(request):
    if request.user.is_authenticated:
        Pending_conversations=Chat.objects.filter(Q(conversation_id__seller=request.user) | Q(conversation_id__buyer=request.user),~Q(sender=request.user),Q(status="Pending")| Q(status="Delivered"))
    
        
        return {
            "Pending_conversations":Pending_conversations.count()
        }
    else:
        return {
            "Pending_conversations":0
        }