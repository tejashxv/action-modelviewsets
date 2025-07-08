from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    capacity = models.IntegerField()
    ticket_price = models.FloatField(default=50.0)
    status = models.CharField(max_length=200, default=(('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed') , ('cancelled', 'Cancelled')))
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    
    
    
    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=100 , choices=(('regular', 'Regular'), ('vip', 'VIP'), ('student', 'Student')))
    price = models.FloatField(default=50.0)
    
class Booking(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pending')
    total_price = models.FloatField()
    ticket_type = models.CharField(max_length=100, choices=(('regular', 'Regular'), ('vip', 'VIP'), ('student', 'Student')))
    booking_date = models.DateTimeField(auto_now_add=True)