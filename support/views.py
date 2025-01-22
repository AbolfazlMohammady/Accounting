from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import Ticket, Message
from .permissions import IsSupporterOrReadOnly, IsOwnerOrReadOnly
from .serializer import CustumTicketSerializer, TicketSerializer, MessageSerializer

class TicketViewSet(GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin):
    
    permission_classes =[IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.select_related('user', 'supporter').all()
        return Ticket.objects.select_related('user', 'supporter').filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return CustumTicketSerializer
        return TicketSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsSupporterOrReadOnly()]
        if self.action in ['retrieve']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    

class MessageViewSet(GenericViewSet, 
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin, 
                    mixins.RetrieveModelMixin): 
    queryset = Message.objects.select_related('ticket', 'sender').all()
    serializer_class= MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [IsSupporterOrReadOnly()]
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return super().get_permissions()