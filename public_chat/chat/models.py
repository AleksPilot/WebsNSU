from django.db import models
from django.conf import settings


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, help_text='connected users0')

    def __str__(self):
        return self.title

    def connect_user(self, user):
        """
        return True if user is in the users list
        :param user:
        :return: True/False
        """
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        """
        return True if user is removed from the users list
        :param user:
        :return: True/False
        """
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        """
        Returns the channels group name where user can excange messages
        :return:
        """
        return f"PublicChatRoom-{self.id}"

class PublicRoomChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = PublicRoomChatMessage.objects.filter(room=room).order_by("-filestamp")
        return qs

class PublicRoomChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    def __str__(self):
        return self.content
