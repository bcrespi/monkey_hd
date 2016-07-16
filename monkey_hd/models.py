from django.db import models
from django.contrib.auth.models import User


class Permission(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    phone = models.CharField(max_length=15, blank=True, null=True)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Priority(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Scalability(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    date_creation = models.DateField(auto_now_add=True)
    date_start = models.DateField(blank=True, null=True)
    date_solved = models.DateField(blank=True, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, related_name='ticket_user', blank=True, null=True, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    scalability = models.ForeignKey(Scalability, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class History(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    writer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_creation = models.DateField(auto_now_add=True, blank=True)
    last_modified = models.DateField(auto_now=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.writer.user.username
