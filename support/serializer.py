from rest_framework import serializers
from core.serializer import UserSerializer

from .models import Ticket, Message

class TicketSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields=['subject', 'created_at', 'status']
        read_only_fields= ['status','created_at']

    def get_status(self, obj):
        return obj.get_status_display()


class CustumTicketSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    supporter = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields=['id', 'subject', 'created_at', 'status','user', 'supporter']
        read_only_fields= ['created_at','user', 'supporter']

    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        instance.supporter = request_user
        return super().update(instance, validated_data)


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    def get_sender(self, message:Message):
        if self.context['request'].user.is_staff:
            return UserSerializer(message.sender).data
        return False


    class Meta:
        model = Message
        fields = ['id', 'sender', 'ticket', 'content', 'created_at', 'is_support']
        read_only_fields = ['sender', 'ticket', 'created_at', 'is_support']

    def validate(self, data):
        ticket = ticket_id = self.context['view'].kwargs['ticket_pk']
        ticket = Ticket.objects.get(id=ticket_id)
        request_user = self.context['request'].user

        if not request_user.is_staff and ticket.user != request_user:
            raise serializers.ValidationError("You can only send messages for your own tickets")
        if request_user.is_staff and ticket.supporter and ticket.supporter != request_user:
            raise serializers.ValidationError("Only the assigned supporter can respond to this ticket.")
         
        return data

    def create(self, validated_data):
        ticket_id = self.context['view'].kwargs['ticket_pk']
        ticket = Ticket.objects.get(id=ticket_id)
        request_user = self.context['request'].user

        validated_data['ticket']= ticket
        validated_data['sender']= request_user

        if request_user.is_staff:
            validated_data['is_support']= True

        if ticket.status == "U":
            raise serializers.ValidationError(" تیکت هنوز توسط پشتیبان دیده نشده!")
        if ticket.status == "C":
            raise serializers.ValidationError("تیکت بسته شده است!")

        return super().create(validated_data)
        
        

