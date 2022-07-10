from django.db import models
from django.db.models import Q
from accounts.models import User


class Chat(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user1_name')
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user2_name')
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = (("user1", "user2"))
        verbose_name = 'Chat Message'
        ordering = ['-updated_on']

    def __str__(self):
        return '%s_%s' %(self.user1.username,self.user2.username)

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    @staticmethod
    def chat_session_exists(user1,user2):
        return Chat.objects.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).first()

    @staticmethod
    def create_if_not_exists(user1,user2):
        res = Chat.chat_session_exists(user1,user2)
        return False if res else Chat.objects.create(user1=user1,user2=user2)

    @staticmethod
    def chat_sessions(user):
        return Chat.objects.filter(Q(user1=user) | Q(user2=user)).all()

class Message(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User,
                            on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat,
                            on_delete=models.CASCADE,
                            related_name='user_messages')
    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.text[:20]

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        Chat.objects.get(id = self.chat.id).save()
