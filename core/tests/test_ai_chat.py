"""
Testes para o sistema de chat com IA
"""
import pytest
from django.test import TestCase
from core.ai_chat import sanitize_input, detect_requires_human_attention


class TestAIChatSecurity(TestCase):
    """Testes de segurança para chat com IA"""
    
    def test_sanitize_input_removes_dangerous_chars(self):
        """Testa se caracteres perigosos são removidos"""
        dangerous_input = "<script>alert('xss')</script>"
        sanitized = sanitize_input(dangerous_input)
        
        self.assertNotIn('<', sanitized)
        self.assertNotIn('>', sanitized)
        self.assertNotIn('script', sanitized)
    
    def test_sanitize_input_limits_length(self):
        """Testa se tamanho máximo é respeitado"""
        long_input = "a" * 2000
        sanitized = sanitize_input(long_input, max_length=1000)
        
        self.assertEqual(len(sanitized), 1000)
    
    def test_sanitize_input_removes_quotes(self):
        """Testa se aspas são removidas"""
        input_with_quotes = 'Test "quoted" and \'single\' quotes'
        sanitized = sanitize_input(input_with_quotes)
        
        self.assertNotIn('"', sanitized)
        self.assertNotIn("'", sanitized)
    
    def test_detect_requires_human_attention_cancelamento(self):
        """Testa detecção de solicitação de cancelamento"""
        message = "Gostaria de cancelar meu agendamento"
        requires_attention = detect_requires_human_attention(message)
        
        self.assertTrue(requires_attention)
    
    def test_detect_requires_human_attention_reagendamento(self):
        """Testa detecção de solicitação de reagendamento"""
        message = "Preciso reagendar para outro dia"
        requires_attention = detect_requires_human_attention(message)
        
        self.assertTrue(requires_attention)
    
    def test_detect_requires_human_attention_reclamacao(self):
        """Testa detecção de reclamação"""
        message = "Tenho uma reclamação sobre o serviço"
        requires_attention = detect_requires_human_attention(message)
        
        self.assertTrue(requires_attention)
    
    def test_detect_requires_human_attention_normal_message(self):
        """Testa que mensagens normais não requerem atenção"""
        message = "Qual o horário de funcionamento?"
        requires_attention = detect_requires_human_attention(message)
        
        self.assertFalse(requires_attention)


class TestAIChatIntegration(TestCase):
    """Testes de integração do chat com IA"""
    
    def test_sanitize_preserves_valid_content(self):
        """Testa que conteúdo válido é preservado"""
        valid_input = "Olá! Gostaria de agendar um corte."
        sanitized = sanitize_input(valid_input)
        
        self.assertIn("Olá", sanitized)
        self.assertIn("agendar", sanitized)
        self.assertIn("corte", sanitized)
    
    def test_sanitize_handles_empty_input(self):
        """Testa tratamento de input vazio"""
        empty_input = ""
        sanitized = sanitize_input(empty_input)
        
        self.assertEqual(sanitized, "")
    
    def test_sanitize_handles_whitespace(self):
        """Testa remoção de espaços extras"""
        input_with_spaces = "Test    with     many    spaces"
        sanitized = sanitize_input(input_with_spaces)
        
        # Verifica que espaços múltiplos foram reduzidos
        self.assertNotIn("    ", sanitized)
    
    def test_sanitize_removes_carriage_returns(self):
        """Testa remoção de carriage returns"""
        input_with_cr = "Line1\r\nLine2\r\nLine3"
        sanitized = sanitize_input(input_with_cr)
        
        self.assertNotIn('\r', sanitized)
        # Newlines devem ser mantidos
        self.assertIn('\n', sanitized)


@pytest.mark.django_db
class TestAIChatPermissions:
    """Testes de permissões do chat"""
    
    def test_rate_limiting(self):
        """Testa rate limiting de mensagens"""
        # Este teste seria implementado com fixtures reais
        # Por enquanto é um placeholder
        assert True
    
    def test_message_validation(self):
        """Testa validação de tamanho de mensagem"""
        # Placeholder para teste futuro
        assert True

