import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

# NOTA: A tabela 'profiles' do Supabase não tem campos de autenticação do Django
# (password, last_login, etc.). O Supabase usa seu próprio sistema de autenticação.
# Este modelo mapeia para 'profiles' mas mantém compatibilidade com Django Auth.
# Não herdamos de AbstractBaseUser para evitar problemas com campos inexistentes.

class UserManager(BaseUserManager):
    def get_queryset(self):
        """Retorna queryset carregando apenas campos que existem no banco"""
        # Usar only() para carregar apenas campos que existem na tabela profiles
        return super().get_queryset().only(
            'id', 'email', 'name', 'phone', 'avatar_url', 'created_at', 'updated_at'
        )
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # Não salvar password na tabela profiles (Supabase gerencia isso)
        user.save(using=self._db)
        # Definir campos de autenticação em cache após salvar
        if 'is_staff' in extra_fields:
            user.is_staff = extra_fields['is_staff']
        if 'is_superuser' in extra_fields:
            user.is_superuser = extra_fields['is_superuser']
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(email, password, **extra_fields)


class User(PermissionsMixin):
    """Modelo User mapeado para tabela profiles do Supabase"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="E-mail", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Nome", db_column="display_name", null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    avatar_url = models.URLField(blank=True, null=True, verbose_name="Avatar URL")
    
    # NOTA: password e last_login não existem na tabela profiles
    # Eles são gerenciados via métodos set_password() e check_password()
    # que usam cache para armazenar hashes de senha
    
    class Meta:
        db_table = "profiles"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["-created_at"]
        managed = True
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Atualizado em")
    
    # Campos que não existem na tabela profiles - usar como propriedades em memória
    # Esses campos são necessários para Django Auth mas não existem no Supabase
    # Armazenamos em cache ou memória

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "profiles"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name or 'Sem nome'} ({self.email or 'Sem email'})"
    
    def save(self, *args, **kwargs):
        """Sobrescrever save para não tentar salvar campos que não existem no banco"""
        # Remover campos que não existem na tabela profiles antes de salvar
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            # Remover password e last_login se estiverem em update_fields
            update_fields = [f for f in update_fields if f not in ['password', 'last_login']]
            kwargs['update_fields'] = update_fields
        
        # Armazenar valores temporários de password e last_login se existirem
        temp_password = getattr(self, 'password', None)
        temp_last_login = getattr(self, 'last_login', None)
        
        # Remover do objeto antes de salvar
        if hasattr(self, 'password'):
            delattr(self, 'password')
        if hasattr(self, 'last_login'):
            delattr(self, 'last_login')
        
        try:
            # Chamar save do modelo base
            super().save(*args, **kwargs)
        finally:
            # Restaurar valores temporários (para compatibilidade com código Django)
            if temp_password is not None:
                setattr(self, 'password', temp_password)
            if temp_last_login is not None:
                setattr(self, 'last_login', temp_last_login)
    
    # Propriedades para compatibilidade com Django Auth (não salvam no banco)
    # Armazenamos em cache usando o ID do usuário como chave
    def _get_auth_field(self, field_name, default):
        """Obtém campo de autenticação do cache"""
        from django.core.cache import cache
        cache_key = f"user_{field_name}_{self.id}"
        value = cache.get(cache_key)
        return value if value is not None else default
    
    def _set_auth_field(self, field_name, value):
        """Armazena campo de autenticação no cache"""
        from django.core.cache import cache
        cache_key = f"user_{field_name}_{self.id}"
        cache.set(cache_key, bool(value), timeout=86400 * 365)  # 1 ano
    
    @property
    def is_active(self):
        """Usuário sempre ativo por padrão (não há campo no banco)"""
        return self._get_auth_field('is_active', True)
    
    @is_active.setter
    def is_active(self, value):
        self._set_auth_field('is_active', value)
    
    @property
    def is_staff(self):
        """Verifica se é staff (não há campo no banco)"""
        return self._get_auth_field('is_staff', False)
    
    @is_staff.setter
    def is_staff(self, value):
        self._set_auth_field('is_staff', value)
    
    @property
    def is_superuser(self):
        """Verifica se é superusuário (não há campo no banco)"""
        return self._get_auth_field('is_superuser', False)
    
    @is_superuser.setter
    def is_superuser(self, value):
        self._set_auth_field('is_superuser', value)
    
    def set_password(self, raw_password):
        """
        Armazena hash da senha no cache (não no banco)
        Compatível com SupabaseAuthBackend
        """
        from users.backends import SupabaseAuthBackend
        if raw_password:
            SupabaseAuthBackend.store_password_hash(self.id, raw_password)
        # Armazenar também em memória para compatibilidade
        self._password = raw_password
    
    def check_password(self, raw_password):
        """
        Verifica senha usando cache (backend customizado)
        """
        from django.core.cache import cache
        import hashlib
        import hmac
        
        if not raw_password:
            return False
        
        # Verificar no cache primeiro
        cache_key = f"user_password_{self.id}"
        stored_hash = cache.get(cache_key)
        
        if stored_hash:
            password_hash = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()
            if hmac.compare_digest(stored_hash, password_hash):
                return True
        
        # Fallback: verificar senha em memória (durante criação)
        if hasattr(self, '_password'):
            return self._password == raw_password
        
        return False
    
    @property
    def is_anonymous(self):
        """Sempre False para usuários autenticados (necessário para Django Auth)"""
        return False
    
    @property
    def is_authenticated(self):
        """Sempre True para instâncias de User (necessário para Django Auth)"""
        return True
    
    @property
    def is_admin(self):
        """Verifica se é administrador (baseado em is_staff)"""
        return self.is_staff or self.is_superuser
    
    @property
    def is_barber(self):
        """Verifica se é barbeiro (pode ser implementado via relacionamento)"""
        # Pode ser verificado via relacionamento com Barbeiro
        return hasattr(self, 'barbeiro_profile')
