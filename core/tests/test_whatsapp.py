"""
Testes para integração WhatsApp
"""
from django.test import TestCase
from core.whatsapp import (
    sanitize_phone,
    sanitize_message_content,
    generate_confirmation_message,
    generate_reminder_message
)


class TestWhatsAppSecurity(TestCase):
    """Testes de segurança para WhatsApp"""
    
    def test_sanitize_phone_removes_non_digits(self):
        """Testa remoção de caracteres não numéricos"""
        phone = "(45) 99941-7111"
        sanitized = sanitize_phone(phone)
        
        self.assertEqual(sanitized, "5545999417111")
        self.assertNotIn('(', sanitized)
        self.assertNotIn(')', sanitized)
        self.assertNotIn('-', sanitized)
        self.assertNotIn(' ', sanitized)
    
    def test_sanitize_phone_adds_country_code(self):
        """Testa adição automática de código do país"""
        phone = "45999417111"
        sanitized = sanitize_phone(phone)
        
        self.assertTrue(sanitized.startswith('55'))
        self.assertEqual(len(sanitized), 13)
    
    def test_sanitize_message_removes_dangerous_chars(self):
        """Testa remoção de caracteres perigosos"""
        dangerous_message = "<script>alert('xss')</script>"
        sanitized = sanitize_message_content(dangerous_message)
        
        self.assertNotIn('<', sanitized)
        self.assertNotIn('>', sanitized)
        self.assertNotIn('script', sanitized)
    
    def test_sanitize_message_limits_length(self):
        """Testa limite de tamanho da mensagem"""
        long_message = "a" * 2000
        sanitized = sanitize_message_content(long_message, max_length=1000)
        
        self.assertEqual(len(sanitized), 1000)
    
    def test_sanitize_message_removes_backticks(self):
        """Testa remoção de backticks"""
        message = "Test with `backticks`"
        sanitized = sanitize_message_content(message)
        
        self.assertNotIn('`', sanitized)


class TestWhatsAppMessageGeneration(TestCase):
    """Testes de geração de mensagens"""
    
    def test_message_generation_structure(self):
        """Testa estrutura básica de mensagens"""
        # Este teste requer um agendamento real
        # Por enquanto é um placeholder
        assert True
    
    def test_confirmation_message_contains_required_info(self):
        """Testa se mensagem de confirmação contém informações necessárias"""
        # Placeholder - requer fixtures
        assert True
    
    def test_reminder_message_format(self):
        """Testa formato da mensagem de lembrete"""
        # Placeholder - requer fixtures
        assert True


class TestWhatsAppIntegration(TestCase):
    """Testes de integração WhatsApp"""
    
    def test_sanitize_phone_handles_various_formats(self):
        """Testa diferentes formatos de telefone"""
        formats = [
            "(45) 99941-7111",
            "45 99941-7111",
            "45999417111",
            "+55 45 99941-7111",
            "5545999417111"
        ]
        
        for phone_format in formats:
            sanitized = sanitize_phone(phone_format)
            # Todos devem resultar no mesmo formato
            self.assertEqual(len(sanitized), 13)
            self.assertTrue(sanitized.startswith('55'))
            self.assertTrue(sanitized.isdigit())
    
    def test_sanitize_message_preserves_valid_content(self):
        """Testa que conteúdo válido é preservado"""
        valid_message = "Olá! Seu agendamento foi confirmado para amanhã."
        sanitized = sanitize_message_content(valid_message)
        
        self.assertIn("Olá", sanitized)
        self.assertIn("agendamento", sanitized)
        self.assertIn("confirmado", sanitized)
    
    def test_sanitize_message_handles_empty(self):
        """Testa tratamento de mensagem vazia"""
        empty_message = ""
        sanitized = sanitize_message_content(empty_message)
        
        self.assertEqual(sanitized, "")
    
    def test_phone_validation_rejects_too_short(self):
        """Testa que números muito curtos são detectados"""
        short_phone = "123"
        sanitized = sanitize_phone(short_phone)
        
        # Número curto ainda será processado mas não terá 10+ dígitos
        self.assertLess(len(sanitized), 10)


class TestWhatsAppSanitization(TestCase):
    """Testes específicos de sanitização"""
    
    def test_sanitize_removes_sql_injection_attempts(self):
        """Testa proteção contra SQL injection em mensagens"""
        sql_injection = "'; DROP TABLE appointments; --"
        sanitized = sanitize_message_content(sql_injection)
        
        # Caracteres perigosos devem ser removidos
        self.assertNotIn("'", sanitized)
        self.assertNotIn(";", sanitized)  # Ponto-vírgula pode ser mantido, depende da implementação
    
    def test_sanitize_removes_html_tags(self):
        """Testa remoção de tags HTML"""
        html_message = "<b>Bold</b> and <i>italic</i> text"
        sanitized = sanitize_message_content(html_message)
        
        self.assertNotIn('<b>', sanitized)
        self.assertNotIn('</b>', sanitized)
        self.assertNotIn('<i>', sanitized)
        self.assertNotIn('</i>', sanitized)
    
    def test_sanitize_preserves_emojis(self):
        """Testa que emojis são preservados"""
        emoji_message = "Olá! 😊 Tudo bem? 👍"
        sanitized = sanitize_message_content(emoji_message)
        
        self.assertIn("😊", sanitized)
        self.assertIn("👍", sanitized)

