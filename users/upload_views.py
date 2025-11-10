"""
User Avatar Upload with Pillow
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import uuid

class UploadAvatarView(APIView):
    """Upload e processa avatar do usuário"""
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        # Validar arquivo
        if 'avatar' not in request.FILES:
            return Response(
                {'error': 'Nenhum arquivo enviado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        avatar_file = request.FILES['avatar']
        
        # Validar tipo
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if avatar_file.content_type not in allowed_types:
            return Response(
                {'error': 'Tipo de arquivo inválido. Use JPG, PNG ou WEBP'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar tamanho (max 5MB)
        if avatar_file.size > 5 * 1024 * 1024:
            return Response(
                {'error': 'Arquivo muito grande. Máximo 5MB'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Processar imagem com Pillow
            image = Image.open(avatar_file)
            
            # Converter para RGB se necessário
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Resize para 400x400 (mantendo aspect ratio)
            image.thumbnail((400, 400), Image.Resampling.LANCZOS)
            
            # Criar thumbnail 100x100
            thumb = image.copy()
            thumb.thumbnail((100, 100), Image.Resampling.LANCZOS)
            
            # Gerar nome único
            filename = f"avatars/{request.user.id}_{uuid.uuid4().hex[:8]}.jpg"
            thumb_filename = f"avatars/thumbs/{request.user.id}_{uuid.uuid4().hex[:8]}.jpg"
            
            # Salvar imagem principal
            from io import BytesIO
            output = BytesIO()
            image.save(output, format='JPEG', quality=90, optimize=True)
            output.seek(0)
            
            # Salvar thumbnail
            thumb_output = BytesIO()
            thumb.save(thumb_output, format='JPEG', quality=85, optimize=True)
            thumb_output.seek(0)
            
            # Deletar avatar antigo se existir
            if request.user.avatar_url:
                try:
                    old_path = request.user.avatar_url.replace('/media/', '')
                    if default_storage.exists(old_path):
                        default_storage.delete(old_path)
                except:
                    pass
            
            # Salvar novos arquivos
            saved_path = default_storage.save(filename, ContentFile(output.read()))
            thumb_path = default_storage.save(thumb_filename, ContentFile(thumb_output.read()))
            
            # Atualizar usuário
            avatar_url = f'/media/{saved_path}'
            request.user.avatar_url = avatar_url
            request.user.save()
            
            return Response({
                'message': 'Avatar atualizado com sucesso',
                'avatar_url': avatar_url,
                'thumb_url': f'/media/{thumb_path}'
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erro ao processar imagem: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

