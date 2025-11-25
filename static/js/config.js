/**
 * CONFIGURAÇÕES GLOBAIS DA APLICAÇÃO
 * Este arquivo deve ser carregado ANTES de qualquer outro JavaScript
 */

// Configuração da API
if (typeof window.API_BASE === 'undefined') {
    window.API_BASE = '/api';
}

// Configurações globais
window.APP_CONFIG = {
    API_BASE: window.API_BASE,
    DEBUG: false
};

