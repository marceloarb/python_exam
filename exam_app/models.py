from django.db import models
import re
import datetime
class UserManager(models.Manager):
    def basic_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['name']) < 3:
            errors['name'] = "Name is too short"
        users_with_name = User.objects.filter(name=requestPOST['name'])
        if len(users_with_name) > 0:
            errors['duplicate'] = "Name already taken"
        if len(requestPOST['password']) < 8:
            errors['password'] = "Password is too short"
        if requestPOST['password'] != requestPOST['password_conf']:
            errors['no_match'] = "Password and Password Confirmation must match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors
    def basic_validator_update(self, requestPOST):
        errors = {}
        if len(requestPOST['name']) == 0:
            errors['name'] = "You can not leave empty field"
        if len(requestPOST['name']) < 3:
            errors['name'] = "Name is too short"
        users_with_name = User.objects.filter(name=requestPOST['name'])
        if len(users_with_name) > 0:
            errors['duplicate'] = "Name already taken"
            
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        users_with_email = User.objects.filter(email=requestPOST['email'])
        if len(users_with_email) > 0:
            errors['duplicate'] = "email already taken"
        return errors
class User(models.Model):
    name = models.TextField()
    password = models.TextField()
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class QuoteManager(models.Manager):
    def basic_validator_quote(self, requestPOST):
        errors = {}
        if len(requestPOST['author']) < 3:
            errors['author'] = "Name is too short"
        if len(requestPOST['quote']) < 10:
            errors['quote'] = "Quote is too short"
        return errors


class Quote(models.Model):
    author = models.TextField()
    quote = models.TextField()
    user = models.ForeignKey(User,related_name='quotes',on_delete=models.CASCADE)
    users_who_liked = models.ManyToManyField(User,related_name='quotes_liked_for')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()