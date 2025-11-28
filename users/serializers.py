from rest_framework import serializers

from core.validators import validate_phone

from .models import User


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()
    is_superuser = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "email", "name", "phone", "is_active", "is_staff", "is_superuser", "created_at", "avatar_url")
        read_only_fields = ("id", "created_at", "is_active", "is_staff", "is_superuser")
        extra_kwargs = {"phone": {"validators": [validate_phone]}}
    
    def get_is_active(self, obj):
        """Retorna sempre True por padrão (campo não existe no banco)"""
        return getattr(obj, 'is_active', True)
    
    def get_is_staff(self, obj):
        """Retorna se é staff"""
        return getattr(obj, 'is_staff', False)
    
    def get_is_superuser(self, obj):
        """Retorna se é superusuário"""
        return getattr(obj, 'is_superuser', False)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("email", "name", "phone", "password", "password_confirm")
        extra_kwargs = {
            "phone": {"required": False, "allow_blank": True},
        }

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("As senhas não coincidem")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password", None)
        
        # Criar usuário (Supabase gerencia autenticação, mas manter compatibilidade)
        user = User.objects.create(
            email=validated_data["email"],
            name=validated_data["name"],
            phone=validated_data.get("phone", ""),
        )
        
        # Armazenar hash da senha no cache para autenticação
        if password:
            user.set_password(password)
        
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
