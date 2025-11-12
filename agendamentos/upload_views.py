"""
Views para upload de fotos de agendamentos
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from agendamentos.models import Agendamento
from PIL import Image
import io
import os


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_appointment_photo(request, pk):
    """
    Upload de foto do resultado do agendamento
    POST /api/appointments/<id>/upload-photo/
    
    Validações:
    - Tipo de arquivo (JPG, PNG, WebP)
    - Tamanho máximo (5MB)
    - Redimensionamento automático se necessário
    """
    try:
        # Buscar agendamento
        appointment = Agendamento.objects.get(pk=pk)
        
        # Verificar permissão
        if not (request.user.is_staff or 
                request.user.role in ['admin', 'owner', 'barber'] or 
                appointment.user == request.user):
            return Response({
                'error': 'Você não tem permissão para fazer upload neste agendamento'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Verificar se foto foi enviada
        if 'photo' not in request.FILES:
            return Response({
                'error': 'Nenhuma foto foi enviada'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        photo = request.FILES['photo']
        
        # Validar tipo de arquivo
        valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if photo.content_type not in valid_types:
            return Response({
                'error': 'Formato inválido. Use JPG, PNG ou WebP'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar tamanho (5MB)
        max_size = 5 * 1024 * 1024
        if photo.size > max_size:
            return Response({
                'error': 'Arquivo muito grande. Máximo 5MB'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar extensão
        ext = os.path.splitext(photo.name)[1].lower()
        valid_exts = ['.jpg', '.jpeg', '.png', '.webp']
        if ext not in valid_exts:
            return Response({
                'error': 'Extensão inválida'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Processar imagem
        try:
            # Abrir imagem com Pillow
            image = Image.open(photo)
            
            # Redimensionar se muito grande (max 1920px)
            max_dimension = 1920
            if image.width > max_dimension or image.height > max_dimension:
                image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            # Converter para RGB se necessário
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Salvar imagem otimizada
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Gerar nome único
            filename = f'appointments/{appointment.id}_{photo.name}'
            
            # Salvar arquivo
            path = default_storage.save(filename, ContentFile(output.read()))
            
            # Atualizar agendamento
            if hasattr(appointment, 'result_photo'):
                # Deletar foto antiga se existir
                if appointment.result_photo:
                    default_storage.delete(appointment.result_photo.name)
                
                appointment.result_photo = path
                appointment.save()
            
            # Retornar sucesso
            return Response({
                'success': True,
                'message': 'Foto enviada com sucesso',
                'photo_url': default_storage.url(path),
                'filename': os.path.basename(path)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Erro ao processar imagem: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Agendamento.DoesNotExist:
        return Response({
            'error': 'Agendamento não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Erro no upload: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

