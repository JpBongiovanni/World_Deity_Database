from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'

        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
        

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    about = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()

class Deity(models.Model):
    name = models.CharField(max_length=255)
    contributor = models.ForeignKey(User, related_name = "quotes", on_delete = models.CASCADE)
    alt_name = models.CharField(max_length=255)
    culture = models.CharField(max_length=255)
    description = models.TextField()
    pop_culture = models.TextField()
    source = models.TextField()
    image = models.ImageField(upload_to='diety_pic')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)