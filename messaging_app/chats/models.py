"""
Models for messaging app: User, Conversation, Message.
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	"""Custom user model extending AbstractUser."""
	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	role = models.CharField(max_length=10, choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')])
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.username} ({self.email})"

class Conversation(models.Model):
	"""Conversation model tracking participants."""
	conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	participants = models.ManyToManyField('User', related_name='conversations')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Conversation {self.conversation_id}"

class Message(models.Model):
	"""Message model containing sender, conversation, and body."""
	message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	sender = models.ForeignKey('User', on_delete=models.CASCADE)
	conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='messages')
	message_body = models.TextField()
	sent_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Message {self.message_id} from {self.sender}"
