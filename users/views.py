from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


@method_decorator(ratelimit(key="ip", rate="3/h", method="POST"), name="dispatch")
class RegisterView(generics.CreateAPIView):
    """Registro de novos usuários

    Rate limit: 3 registros por hora por IP
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = serializer.save()
            
            # Gerar tokens JWT
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "success": True,
                    "message": "Conta criada com sucesso! Bem-vindo à Barbearia Francisco!",
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    "redirect": "/perfil/"  # Redirecionar para dashboard do cliente (perfil)
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {
                    "success": False,
                    "error": f"Erro ao criar conta: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(ratelimit(key="ip", rate="5/m", method="POST"), name="dispatch")
class LoginView(APIView):
    """Login de usuários

    Rate limit: 5 tentativas por minuto por IP
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"success": False, "error": "Email ou senha incorretos"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Verificar se usuário está ativo (sempre True por padrão, mas verificar cache)
        if not user.is_active:
            return Response(
                {"success": False, "error": "Usuário inativo. Entre em contato com o suporte."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Gerar tokens JWT
            refresh = RefreshToken.for_user(user)
            
            # SEMPRE redirecionar para /perfil/ após login
            # O botão de admin aparecerá no perfil se o usuário tiver permissão
            # Verificar no banco se o email tem permissão de admin
            is_admin = user.is_staff or user.is_superuser

            return Response(
                {
                    "success": True,
                    "message": "Login realizado com sucesso!",
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    "redirect": "/perfil/",  # Sempre redirecionar para perfil
                    "is_admin": is_admin  # Informar se é admin para o frontend
                }
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {"success": False, "error": f"Erro ao fazer login: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserDetailView(generics.RetrieveUpdateAPIView):
    """Detalhes e edição do usuário autenticado"""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """Logout do usuário"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckAdminView(APIView):
    """Verifica se o usuário atual tem permissão de administrador
    Consulta o banco de dados para verificar se o email está autorizado
    """
    
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        """
        Verifica se o usuário atual é admin consultando o banco de dados
        Retorna True se o email do usuário tem permissão de admin
        """
        user = request.user
        
        # Verificar no banco se o usuário tem permissão de admin
        # Consulta o cache/banco para verificar is_staff ou is_superuser
        is_admin = user.is_staff or user.is_superuser
        
        return Response({
            "is_admin": is_admin,
            "email": user.email,
            "user_id": str(user.id)
        })
