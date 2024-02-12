from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib import auth

from auth_api.serializer import RegisterSerializer, LoginSerializer


class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid(raise_exception=True):
            register_serializer.save()
            return Response({"user": register_serializer.data, "message": "User Created Successfully"},
                            status=status.HTTP_201_CREATED)
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(generics.GenericAPIView):

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data, context={'request': request})
        login_serializer.is_valid(raise_exception=True)
        return Response(login_serializer.data, status=200)


@api_view(['GET'])
def signout(request):
    auth.logout(request=request)
    return Response("User logged out.", status=status.HTTP_200_OK)


@api_view(['POST'])
def forgot_password(request):
    htmly = get_template('account/email.html')
    d = {'username': request.data['username']}
    subject, from_email, to = 'Password Reset', 'no-reply@kaizn.com', request.data['username']
    html_content = htmly.render(d)
    # 'reset_password_url': "{}?token={}".format(
    #     instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
    #     reset_password_token.key)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
