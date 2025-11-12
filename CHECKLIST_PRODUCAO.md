# ✅ Checklist de Produção - Barbearia Django

## 🔒 SEGURANÇA

### Configurações Básicas
- [ ] `DEBUG = False` em settings_prod.py
- [ ] `SECRET_KEY` única e forte (50+ caracteres)
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] Senhas fortes em todos os serviços
- [ ] `.env` não commitado no Git

### HTTPS e SSL
- [ ] Certificado SSL configurado
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] HSTS headers configurados

### Proteções Adicionais
- [ ] Firewall configurado (UFW)
- [ ] Fail2Ban instalado e ativo
- [ ] Rate limiting ativo
- [ ] CORS configurado corretamente
- [ ] X-Frame-Options = DENY

---

## 🗄️ BANCO DE DADOS

### PostgreSQL
- [ ] PostgreSQL instalado
- [ ] Banco de dados criado
- [ ] Usuário com permissões corretas
- [ ] Conexão testada
- [ ] Backup automático configurado
- [ ] Índices criados
- [ ] VACUUM configurado

### Migrações
- [ ] Todas as migrações aplicadas
- [ ] Sem migrações pendentes
- [ ] Dados iniciais populados
- [ ] Superusuário criado

---

## 📦 ARQUIVOS E MÍDIA

### Arquivos Estáticos
- [ ] `collectstatic` executado
- [ ] WhiteNoise configurado
- [ ] Nginx servindo estáticos
- [ ] Compressão Gzip ativa
- [ ] Cache headers configurados

### Arquivos de Media
- [ ] Diretório media/ criado
- [ ] Permissões corretas
- [ ] Nginx servindo media
- [ ] Backup de media configurado

---

## 🔧 SERVIÇOS

### Django (Gunicorn)
- [ ] Gunicorn instalado
- [ ] Workers configurados (CPU * 2 + 1)
- [ ] Timeout ajustado
- [ ] Logs configurados
- [ ] Supervisor gerenciando processo
- [ ] Reinício automático ativo

### Nginx
- [ ] Nginx instalado e rodando
- [ ] Configuração testada (`nginx -t`)
- [ ] Proxy pass configurado
- [ ] Gzip compression ativa
- [ ] Security headers adicionados
- [ ] Rate limiting configurado

### Redis
- [ ] Redis instalado e rodando
- [ ] Persistência configurada
- [ ] Senha configurada (se necessário)
- [ ] Cache Django funcionando
- [ ] Celery conectando

### Celery
- [ ] Celery Worker rodando
- [ ] Celery Beat rodando
- [ ] Tarefas periódicas agendadas
- [ ] Supervisor gerenciando processos
- [ ] Logs separados
- [ ] Flower instalado (opcional)

---

## 🔌 APIs EXTERNAS

### Google Gemini AI
- [ ] API Key obtida
- [ ] Quota verificada
- [ ] GEMINI_API_KEY configurada
- [ ] Testes realizados
- [ ] Fallback implementado

### Twilio WhatsApp
- [ ] Conta criada
- [ ] Número WhatsApp configurado
- [ ] TWILIO_ACCOUNT_SID configurada
- [ ] TWILIO_AUTH_TOKEN configurada
- [ ] Sandbox testado (dev)
- [ ] Número aprovado (prod)
- [ ] Créditos verificados

### Sentry (Monitoramento)
- [ ] Projeto criado
- [ ] DSN configurada
- [ ] Integração testada
- [ ] Alertas configurados

---

## 📊 MONITORAMENTO

### Logs
- [ ] Diretório logs/ criado
- [ ] Log rotation configurado
- [ ] Níveis de log corretos
- [ ] Logs centralizados
- [ ] Retenção de 30 dias

### Backups
- [ ] Script de backup criado
- [ ] Backup automático (cron)
- [ ] Backup do banco funcionando
- [ ] Backup de media funcionando
- [ ] Retenção de 30 dias
- [ ] Testes de restauração

### Health Checks
- [ ] Endpoint /health/ criado
- [ ] Database check
- [ ] Redis check
- [ ] Celery check
- [ ] Monitoramento ativo

---

## 🌐 DOMÍNIO E DNS

### Configuração
- [ ] Domínio registrado
- [ ] DNS apontando para servidor
- [ ] A record configurado
- [ ] CNAME www configurado
- [ ] Propagação DNS verificada

### SSL/TLS
- [ ] Certbot instalado
- [ ] Certificado obtido
- [ ] Renovação automática configurada
- [ ] Redirect HTTP → HTTPS ativo
- [ ] Teste SSL (ssllabs.com)

---

## 🧪 TESTES EM PRODUÇÃO

### Funcionalidades
- [ ] Login/logout funcionando
- [ ] Cadastro de usuários
- [ ] CRUD de agendamentos
- [ ] CRUD de barbeiros
- [ ] CRUD de serviços
- [ ] Sistema de cupons
- [ ] Chat com IA respondendo
- [ ] Notificações WhatsApp enviando

### Performance
- [ ] Páginas carregando < 2s
- [ ] APIs respondendo < 500ms
- [ ] Queries otimizadas (Django Debug Toolbar)
- [ ] Cache funcionando
- [ ] Gzip ativo

### Celery Tasks
- [ ] Lembretes sendo enviados
- [ ] Agendamentos recorrentes gerando
- [ ] Limpeza de dados funcionando
- [ ] Retry de falhas ativo

---

## 📱 COMPONENTES UI

### Verificação
- [ ] CSS carregando sem erros
- [ ] JavaScript funcionando
- [ ] Componentes renderizando
- [ ] Animações suaves
- [ ] Responsivo em mobile
- [ ] Acessibilidade OK

### Showcase
- [ ] Página /showcase/ acessível
- [ ] Todos componentes visíveis
- [ ] Interatividade funcionando
- [ ] Toasts aparecendo
- [ ] Modais abrindo/fechando

---

## 🎯 PERFORMANCE

### Django
- [ ] Connection pooling ativo
- [ ] Query optimization
- [ ] Select related usado
- [ ] Prefetch related usado
- [ ] Cache em views pesadas

### Servidor
- [ ] CPU < 70% uso médio
- [ ] RAM < 80% uso médio
- [ ] Disk I/O otimizado
- [ ] Network OK

### Banco de Dados
- [ ] Índices criados
- [ ] Queries lentas identificadas
- [ ] EXPLAIN ANALYZE usado
- [ ] Vacuum automático

---

## 📧 NOTIFICAÇÕES

### Email
- [ ] SMTP configurado
- [ ] Email de teste enviado
- [ ] Templates customizados
- [ ] Unsubscribe link

### WhatsApp
- [ ] Twilio funcionando
- [ ] Mensagens chegando
- [ ] Fallback wa.me testado
- [ ] Templates aprovados

---

## 👥 USUÁRIOS E PERMISSÕES

### Setup Inicial
- [ ] Superusuário admin criado
- [ ] Barbeiros cadastrados
- [ ] Roles configuradas
- [ ] Permissões testadas
- [ ] IA configurada por barbeiro

---

## 📈 ANALYTICS (Opcional)

### Google Analytics
- [ ] GA4 configurado
- [ ] Tag instalada
- [ ] Events configurados
- [ ] Conversões rastreadas

### Métricas Customizadas
- [ ] Agendamentos por dia
- [ ] Taxa de cancelamento
- [ ] Tempo médio de resposta
- [ ] Satisfação dos clientes

---

## 🔄 CI/CD (Opcional)

### GitHub Actions
- [ ] Workflow criado
- [ ] Testes automatizados
- [ ] Deploy automático
- [ ] Notificações configuradas

---

## ✅ VALIDAÇÃO FINAL

### Testes Funcionais
```bash
# Testar endpoint
curl https://seu-dominio.com

# Testar API
curl https://seu-dominio.com/api/ai/stats/

# Testar health
curl https://seu-dominio.com/health/

# Testar admin
# Abrir: https://seu-dominio.com/admin-painel/dashboard/
```

### Testes de Carga
```bash
# Apache Bench
ab -n 1000 -c 10 https://seu-dominio.com/

# OU Locust
pip install locust
locust -f locustfile.py
```

### Testes de Segurança
```bash
# SSL Test
curl https://www.ssllabs.com/ssltest/analyze.html?d=seu-dominio.com

# Headers
curl -I https://seu-dominio.com

# OWASP ZAP scan (opcional)
```

---

## 📞 PÓS-DEPLOY

### Primeiras 24 Horas
- [ ] Monitorar logs constantemente
- [ ] Verificar uso de recursos
- [ ] Testar todas funcionalidades
- [ ] Verificar envio de notificações
- [ ] Responder a alertas do Sentry

### Primeira Semana
- [ ] Revisar logs diariamente
- [ ] Otimizar queries lentas
- [ ] Ajustar workers se necessário
- [ ] Verificar backups
- [ ] Coletar feedback usuários

### Manutenção Contínua
- [ ] Backup semanal manual
- [ ] Atualização mensal de dependências
- [ ] Review de segurança trimestral
- [ ] Otimização de performance

---

## 📋 COMANDOS ÚTEIS

### Ver Status
```bash
sudo supervisorctl status
sudo systemctl status nginx
sudo systemctl status redis
sudo systemctl status postgresql
```

### Ver Logs
```bash
tail -f logs/django.log
tail -f logs/celery.log
tail -f logs/gunicorn_error.log
sudo tail -f /var/log/nginx/error.log
```

### Reiniciar Serviços
```bash
sudo supervisorctl restart all
sudo systemctl restart nginx
sudo systemctl restart redis
```

### Verificar Recursos
```bash
htop  # CPU e RAM
df -h  # Disco
free -h  # Memória
netstat -tuln  # Portas
```

---

## 🆘 ROLLBACK

### Se algo der errado:

```bash
# 1. Parar serviços
sudo supervisorctl stop all

# 2. Restaurar backup do banco
gunzip < backups/db_YYYYMMDD.sql.gz | psql -U barbearia_user barbearia_prod

# 3. Voltar para versão anterior
git checkout <commit-hash>

# 4. Reinstalar dependências
pip install -r requirements.txt

# 5. Iniciar serviços
sudo supervisorctl start all
```

---

## 🎉 DEPLOY COMPLETO!

Quando todos os checkboxes estiverem marcados:

✅ **SISTEMA EM PRODUÇÃO!** 🚀

Monitorar primeiras 24h e aproveitar!

