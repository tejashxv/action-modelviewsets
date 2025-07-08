from rest_framework import serializers
from home.models import *
from django.contrib.auth.models import User
import sys
import os

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
    
class TicketSerializer(serializers.Serializer):
    try:
        event = serializers.IntegerField()
        ticket_type = serializers.CharField()
        total_person = serializers.IntegerField()
        user = serializers.IntegerField()


        def validate_event(self, value):
            if not Event.objects.filter(id=value).exists():
                raise serializers.ValidationError("Event does not exist")
            return value

        def validate_user(self, value):
            if not User.objects.filter(id=value).exists():
                raise serializers.ValidationError("User does not exist")
            return value


        def create(self, validated_data):
            print(validated_data)
            event = Event.objects.get(id=validated_data['event'])
            user = User.objects.get(id=validated_data['user'])
            ticket = Ticket.objects.create(
                event=event,
                ticket_type=validated_data['ticket_type'],
                total_person=validated_data['total_person']

            )

            booking = Booking.objects.create(
                ticket=ticket,
                user=user,
                total_price=ticket.event.ticket_price * validated_data['total_person'],
                status='Booking Confirmed'
            )

            return booking

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


    # def validate_ticket_type(self, value):
    #     valid_ticket_types = ['regular', 'vip', 'student']
    #     if value not in valid_ticket_types:
    #         raise serializers.ValidationError(f"Ticket type must be one of {valid_ticket_types}")
    #     return value