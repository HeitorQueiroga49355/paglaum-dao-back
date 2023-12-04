from .models import User, EmailConfirmationToken
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .utils import send_confirmation_email
from django.shortcuts import render
import hashlib

JWT_authenticator = JWTAuthentication()


class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            logged_user = self.get_queryset().all().filter(email=user)
            return Response(UserSerializer(logged_user[0]).data)
        except Exception as error:
            print(error)
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            missing_fields = {}
            if 'password' not in request.data:
                missing_fields['password'] = ['This field is required']
            if 'username' not in request.data:
                missing_fields['username'] = ['This field is required']
            if 'email' not in request.data:
                missing_fields['email'] = ['This field is required']
            if 'first_name' not in request.data:
                missing_fields['first_name'] = ['This field is required']
            if 'last_name' not in request.data:
                missing_fields['last_name'] = ['This field is required']
            if (len(missing_fields) > 0):
                return Response(missing_fields, status=400)
            new_user = User.objects.create_user(
                request.data['username'], request.data['email'], request.data['password'])
        except Exception as error:
            return Response({"detail": error.__str__()}, status=400)
        return Response(UserSerializer(new_user).data)

    def get(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            logged_user = self.get_queryset().all().filter(email=user)
            if logged_user[0].is_staff != True:
                Response(
                    {"detail": "You don't have permission for this"}, status=401)
        except Exception as error:
            print(error)
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)
        return super().get(request, *args, **kwargs)


class SendEmailConfirmationTokenAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        message_to_hash = str("security1234" + user.email)
        token = hashlib.sha256(message_to_hash.encode('utf-8')).hexdigest()
        EmailConfirmationToken.objects.create(id=str(token), user=user)
        send_confirmation_email(
            email=user.email, token_id=token, user_id=user.pk)
        return Response(data=None, status=201)


def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    user_id = request.GET.get('user_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        user.is_trusty = True
        user.save()
        data = {'is_trusty': True}
        return render(request, template_name='confirmation_email_view.html', context=data)
    except EmailConfirmationToken.DoesNotExist:
        data = {'is_trusty': False}
        return render(request, template_name='confirmation_email_view.html', context=data)
