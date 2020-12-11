from django.db import models
from account.models import User
from listings.models import Property


# Create your models here.
class Message(models.Model):
    # agent = models.ForeignKey(User)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
    consumer = models.ForeignKey(User, related_name="consumer", on_delete=models.CASCADE, null=True)
    message = models.TextField(null = True, blank = True)
    type = models.CharField(max_length=100, null=True)
    new = models.BooleanField(default=True)
    conversation_id = models.CharField(max_length=100, null=True)
    message_date = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     self.conversation_id = unique_key.gen_unique_key()
    #     return super(Message, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Messages"


    def __str__(self):
        return F"Message on {self.property} from {self.sender}"
