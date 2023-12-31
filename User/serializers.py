from djoser.email import ActivationEmail, ConfirmationEmail
from djoser.serializers import UserCreateSerializer, UserSerializer, ActivationSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from djoser import utils
from django.conf import settings as djangosettings
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings
from django.utils import timezone
import random
import string
import pyotp
import hashlib
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    image = serializers.ImageField(required=False)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "name", "email", "image", "password")

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, user):
        if user.image:
            image_url = user.image.url
            if image_url.startswith("/media/media"):
                image_url = image_url.replace("/media/media", "/media")
            return image_url
        else:
            return None
    class Meta:
        model = UserAccount
        fields = "__all__"
        exclude = ("password",)

class CustomActivationEmail(ActivationEmail):
    template_name = "activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        print(context)
        user = context.get("user")
        key = User.objects.get(email=user.email).id
        print(key)
        hashed_user_id = hashlib.sha256(str(key).encode("utf-8")).hexdigest()

        # Set the seed for the random number generator based on the hashed user ID
        random.seed(hashed_user_id)

        # Generate a random string of characters for the secret key
        secret_key = "".join(random.choices(string.ascii_uppercase + "234567", k=16))
        # Create a TOTP object with a 30 second interval
        totp = pyotp.TOTP(secret_key, interval=600)
        print(secret_key, key)

        # Generate an OTP
        otp = totp.now()

        print(secret_key)
        context["name"] = "E-Learning"
        context["msg"] = "OTP VERIFICATION"
        context["otp"] = otp
        return context

class ConfirmationEmail(ConfirmationEmail):
    template_name = "ConfirmationEmail.html"

class ActivationSerializer(serializers.Serializer):
    otp = serializers.CharField()
    user_id = serializers.IntegerField()
    def validate(self,attrs):
        attrs = super().validate(attrs)
        print(attrs)
        user_id = attrs.get("user_id")
        print(user_id)
        self.user = UserAccount.objects.get(id = user_id)
        return attrs
        
