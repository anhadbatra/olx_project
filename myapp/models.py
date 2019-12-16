from django.utils import timezone
from django.db import models
# from django.db.models import TextField, DateTimeField, ForeignKey, CASCADE
from django.contrib.auth.models import User
from PIL import Image
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=True)

    def __unicode__(self):
        return User

    class Meta:
        db_table = "user_detail"
        verbose_name = "User Detail"
        managed = True


class Location(models.Model):
    location_name = models.CharField(max_length=30, blank=True, null=True)
    current_user = models.IntegerField()

    class Meta:
        db_table = 'location'
        verbose_name_plural = 'Location'
        managed = True

    def __str__(self):
        return self.location_name.capitalize()


class Category(models.Model):
    category_name = models.CharField(max_length=30, blank=True, null=True)
    current_user = models.IntegerField()

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'
        managed = True

    def __str__(self):
        return self.category_name.capitalize()


class Advertise(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)
    user = models.IntegerField()
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=300)
    image = models.FileField(upload_to='image/ad_image', null=True, blank=True,
                             help_text="Upload only .png, .jpg & .jpeg image extension.")
    image1 = models.FileField(upload_to='image/ad_image', null=True, blank=True,
                             help_text="Upload only .png, .jpg & .jpeg image extension.")
    image2 = models.FileField(upload_to='image/ad_image', null=True, blank=True,
                             help_text="Upload only .png, .jpg & .jpeg image extension.")
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    contact = models.BigIntegerField()
    price = models.IntegerField(blank=True, null=True)
    date_created = models.DateField(default=timezone.now)


    class Meta:
        db_table = 'advertise'
        verbose_name_plural = 'Advertise'
        managed = True

    def __unicode__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=200, null=True)
    message = models.TextField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "contact"
        verbose_name = "Contact"
        managed = True


class Favorites(models.Model):
    ad_id = models.IntegerField()
    user_id = models.CharField(max_length=100,blank=True,null=True)
    title = models.ForeignKey(Advertise, blank=True, null=True, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.ad_id

    class Meta:
        db_table = "favourites"
        verbose_name = "favourite"
        managed = True


class MessageModel(models.Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = models.TextField('body')

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    class Meta:
        app_label = 'myapp'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
