from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
	"""Manager for user profiles"""

	def create_user(self, email, name, password = None):
		"""Create a new user profile"""

		#check email
		if not email:
			raise ValueError("Users must have an email address.")

		#normalize email
		email = self.normalize_email(email)
		#create user
		user = self.model(email = email, name = name)
		#encrypt password
		user.set_password(password)
		#save model in django db
		user.save(using = self._db)
		return user

	def create_superuser(self, email, name, password):
		"""Create a new superuser"""
		user = self.create_user(email, name, password)
		user.is_superuser = True
		user.is_staff = True
		user.save(using = self._db)
		return user


# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
	"""
	DB model for users in the system
	"""
	#variables for the class
	email = models.EmailField(max_length = 255, unique = True)
	name = models.CharField(max_length = 255)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)

	#to work with django admin and auth system
	objects = UserProfileManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	#used by django
	def get_full_name(self):
		"""Retrieve full name of the user"""
		return self.name

	def get_short_name(self):
		"""Retrieve short name of the user"""
		return self.name

	#magic function to give correct o/p for print(obj)
	def __str__(self):
		"""Returns string rep. of our user"""
		return self.email
