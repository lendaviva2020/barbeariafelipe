/**
 * CONFIGURAÇÕES GLOBAIS DA APLICAÇÃO
 * Este arquivo deve ser carregado ANTES de qualquer outro JavaScript
 * 
 * IMPORTANTE: Este arquivo define window.API_BASE globalmente
 * Outros arquivos devem usar window.API_BASE, não redeclarar const API_BASE
 */

(function() {
    'use strict';
    
    // Evitar redeclaração - usar IIFE para escopo isolado
    if (typeof window.API_BASE === 'undefined') {
        Object.defineProperty(window, 'API_BASE', {
            value: '/api',
            writable: false,
            configurable: false,
            enumerable: true
        });
    }
    
    // Configurações globais
    if (typeof window.APP_CONFIG === 'undefined') {
        window.APP_CONFIG = {
            API_BASE: window.API_BASE,
            DEBUG: false
        };
    }
})();

