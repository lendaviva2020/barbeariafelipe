"""
Backend de autenticação customizado para integração com Supabase
"""
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.cache import cache
import hashlib
import hmac

User = get_user_model()


class SupabaseAuthBackend(BaseBackend):
    """
    Backend de autenticação que armazena senhas hasheadas em cache
    como solução temporária até integração completa com Supabase Auth
    """
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        if not user.is_active:
            return None
        
        # Verificar senha usando cache (armazenado durante registro)
        cache_key = f"user_password_{user.id}"
        stored_password_hash = cache.get(cache_key)
        
        if stored_password_hash:
            # Hash da senha fornecida
            password_hash = self._hash_password(password)
            # Comparar usando comparação segura
            if hmac.compare_digest(stored_password_hash, password_hash):
                return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def _hash_password(password):
        """Gera hash SHA-256 da senha"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def store_password_hash(user_id, password):
        """Armazena hash da senha no cache (24 horas)"""
        cache_key = f"user_password_{user_id}"
        password_hash = SupabaseAuthBackend._hash_password(password)
        cache.set(cache_key, password_hash, timeout=86400)  # 24 horas

