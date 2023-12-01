import logging
import traceback

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from rest_framework import views, generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.exceptions import SomethingWentWrong, AccountAlreadyExists, IncorrectCredentials, CustomAPIException
from user.models import User
from user.serializers import UserSerializer, LoginSerializer

logger = logging.getLogger(__name__)


class GetUsersView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileCreate(views.APIView):
    def post(self, request):
        username = self.request.data.get("username")
        email = self.request.data.get("email")
        password = self.request.data.get("password")
        firstName = self.request.data.get("firstName")
        lastName = self.request.data.get("lastName")
        gender = self.request.data.get("gender")
        nationality = self.request.data.get("nationality")
        birthDate = self.request.data.get("birthDate")

        email = email.lower().strip()
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.firstName = firstName
            user.lastName = lastName
            user.gender = gender
            user.nationality = nationality
            user.birthDate = birthDate

            user.save()

            try:
                Token.objects.create(user=user)
            except Exception as e:
                logger.info(e)
                logger.info(traceback.format_exc())
                user.delete()
                raise SomethingWentWrong
            data = UserSerializer(user).data
            return JsonResponse(data)

        raise AccountAlreadyExists


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            raise IncorrectCredentials
        email = email.lower().strip()
        user = User.objects.filter(email=email).first()
        if not user:
            raise IncorrectCredentials
        user.save()
        if user:
            pwd_valid = check_password(password, user.password)
            if pwd_valid:
                data = {
                    "token":user.auth_token.key,
                    "username":user.username,
                    "email":user.email,
                    "firstName":user.firstName,
                    "lastName":user.lastName,
                    "gender":user.gender,
                    "nationality":user.nationality,
                    "birthDate":user.birthDate,
                    "role":user.role
                }
                return Response(data)
        raise IncorrectCredentials


class UpdateProfileView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        username = self.request.data.get("username")
        email = self.request.data.get("email")
        firstName = self.request.data.get("firstName")
        lastName = self.request.data.get("lastName")
        gender = self.request.data.get("gender")
        nationality = self.request.data.get("nationality")
        birthDate = self.request.data.get("birthDate")

        prev_email = user.email

        data = {}

        if email and email != prev_email:
            email = email.lower().strip()
            if not User.objects.filter(email=email).exists():
                user.email = email
                data["email"] = user.email
            else:
                raise AccountAlreadyExists

        if username:
            user.username = username
            data["username"] = username

        if firstName:
            user.firstName = firstName
            data["firstName"] = firstName

        if lastName:
            user.lastName = lastName
            data["lastName"] = lastName

        if gender:
            user.gender = gender
            data["gender"] = gender

        if nationality:
            user.nationality = nationality
            data["nationality"] = nationality

        if birthDate:
            user.birthDate = birthDate
            data["birthDate"] = birthDate

        data['role'] = user.role

        user.save()

        return JsonResponse(data, status=202)


class UpdateUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

class DeleteUserView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    lookup_field = 'id'


class UpdatePasswordView(views.APIView):
    permissions_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user

        current_password = self.request.data.get("oldPassword")
        new_password = self.request.data.get("password")

        valid = user.check_password(current_password)
        if not valid:
            raise CustomAPIException(
                "InvalidPassword", "provided password is incorrect", code=400
            )

        if len(new_password) < 6:
            raise CustomAPIException("InvalidPassword", "password too short", code=400)

        user.set_password(new_password)
        user.save()

        return JsonResponse({"ok": True})



