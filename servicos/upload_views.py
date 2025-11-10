"""
Service Image Upload with Pillow
Upload real de imagens para serviços
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import uuid
from .models import Servico


class UploadServiceImageView(APIView):
    """Upload e processa imagem do serviço"""
    permission_classes = (IsAdminUser,)
    
    def post(self, request, service_id):
        # Validar arquivo
        if 'image' not in request.FILES:
            return Response(
                {'error': 'Nenhum arquivo enviado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar serviço
        try:
            service = Servico.objects.get(pk=service_id)
        except Servico.DoesNotExist:
            return Response(
                {'error': 'Serviço não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        image_file = request.FILES['image']
        
        # Validar tipo
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if image_file.content_type not in allowed_types:
            return Response(
                {'error': 'Tipo de arquivo inválido. Use JPG, PNG ou WEBP'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar tamanho (max 5MB)
        if image_file.size > 5 * 1024 * 1024:
            return Response(
                {'error': 'Arquivo muito grande. Máximo 5MB'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Processar imagem com Pillow
            image = Image.open(image_file)
            
            # Converter para RGB se necessário
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Resize para 800x600 (mantendo aspect ratio)
            image.thumbnail((800, 600), Image.Resampling.LANCZOS)
            
            # Criar thumbnail 200x150
            thumb = image.copy()
            thumb.thumbnail((200, 150), Image.Resampling.LANCZOS)
            
            # Gerar nome único
            filename = f"services/{service_id}_{uuid.uuid4().hex[:8]}.jpg"
            thumb_filename = f"services/thumbs/{service_id}_{uuid.uuid4().hex[:8]}.jpg"
            
            # Salvar imagem principal
            from io import BytesIO
            output = BytesIO()
            image.save(output, format='JPEG', quality=90, optimize=True)
            output.seek(0)
            
            # Salvar thumbnail
            thumb_output = BytesIO()
            thumb.save(thumb_output, format='JPEG', quality=85, optimize=True)
            thumb_output.seek(0)
            
            # Deletar imagem antiga se existir
            if service.image_url:
                try:
                    old_path = service.image_url.replace('/media/', '')
                    if default_storage.exists(old_path):
                        default_storage.delete(old_path)
                except:
                    pass
            
            # Salvar novos arquivos
            saved_path = default_storage.save(filename, ContentFile(output.read()))
            thumb_path = default_storage.save(thumb_filename, ContentFile(thumb_output.read()))
            
            # Atualizar serviço
            image_url = f'/media/{saved_path}'
            service.image_url = image_url
            service.save()
            
            return Response({
                'message': 'Imagem atualizada com sucesso',
                'image_url': image_url,
                'thumb_url': f'/media/{thumb_path}'
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erro ao processar imagem: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

