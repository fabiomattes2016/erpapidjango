from accounts.views.base import Base
from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class Signin(Base):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = Authentication.signin(self, email, password)
        enterprise = self.get_enterprise_user(user.id)
        
        serializer = UserSerializer(user)
        
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        
        return Response({
            "user": serializer.data,
            "enterprise": enterprise,
            "accessToken": str(access_token),
            "refreshToken": str(refresh_token)
        })