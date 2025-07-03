# Sistema de Auditoria de Segurança - Archon AI

## Visão Geral

O sistema de auditoria de segurança do Archon AI foi projetado para fornecer logs detalhados de todas as atividades críticas do sistema, garantindo conformidade com normas de segurança (LGPD, GDPR, ISO) e facilitando auditorias e investigações.

## Características Principais

### 🔒 Logging Automático
- **Requisições HTTP**: Todas as requisições são automaticamente registradas
- **Eventos de API Keys**: Criação, modificação e remoção de chaves de API
- **Acessos a Arquivos**: Operações em arquivos sensíveis (.env, configs)
- **Ações Administrativas**: Reset de projetos, alterações críticas
- **Erros e Exceções**: Falhas do sistema com contexto detalhado

### 📊 Formatos de Log
- **Texto Legível**: Arquivo `logs/auditoria.log` para leitura humana
- **JSON Estruturado**: Arquivo `logs/seguranca.json` para análise automatizada
- **Relatórios**: Geração de relatórios em TXT e JSON

### 🚨 Detecção de Atividades Suspeitas
- Múltiplas falhas de autenticação do mesmo IP
- Alto volume de requisições (possível DoS)
- Tentativas de acesso a arquivos sensíveis
- Padrões anômalos de comportamento

## Estrutura dos Logs

### Log de Auditoria (auditoria.log)
```
2025-01-07 19:30:15 | INFO | HTTP_REQUEST | GET /api/status | Status: 200 | IP: 127.0.0.1 | User: anonymous
2025-01-07 19:30:20 | WARNING | API_KEY_CREATE | SUCCESS | Provider: gemini | User: system | IP: 127.0.0.1
2025-01-07 19:30:25 | ERROR | ERROR | VALIDATION | Message: API Key vazia... | User: system | IP: 127.0.0.1
```

### Log Estruturado (seguranca.json)
```json
{
  "metadata": {
    "created_at": "2025-01-07T19:30:00",
    "version": "1.0",
    "description": "Log de segurança estruturado - Archon AI",
    "last_updated": "2025-01-07T19:35:00",
    "total_events": 150
  },
  "events": [
    {
      "event_id": "a1b2c3d4e5f6",
      "timestamp": "2025-01-07T19:30:15",
      "event_type": "http_request",
      "severity": "info",
      "client_info": {
        "ip_address": "127.0.0.1",
        "user_agent": "Mozilla/5.0...",
        "method": "GET",
        "endpoint": "/api/status",
        "referrer": "direct"
      },
      "response": {
        "status_code": 200
      },
      "user": {
        "user_id": null,
        "authenticated": false
      },
      "additional_data": {
        "response_size": 1024,
        "processing_time_ms": 45.2
      }
    }
  ]
}
```

## API Endpoints de Segurança

### 1. Resumo de Segurança
```http
GET /api/security/summary?hours=24
```

**Resposta:**
```json
{
  "period_hours": 24,
  "total_events": 150,
  "events_by_type": {
    "http_request": 120,
    "api_key_management": 5,
    "file_access": 10,
    "system_error": 3
  },
  "events_by_severity": {
    "info": 130,
    "warning": 15,
    "error": 3,
    "critical": 2
  },
  "failed_authentications": 0,
  "error_events": 3,
  "admin_actions": 2,
  "unique_ips": ["127.0.0.1", "192.168.1.100"],
  "top_endpoints": {
    "/api/status": 45,
    "/dashboard": 30,
    "/api/logs": 20
  },
  "suspicious_activity": []
}
```

### 2. Logs de Segurança
```http
GET /api/security/logs?limit=100
```

**Resposta:**
```json
{
  "metadata": {
    "created_at": "2025-01-07T19:30:00",
    "version": "1.0",
    "total_events": 150
  },
  "events": [...],
  "total_events": 150,
  "returned_events": 100
}
```

### 3. Geração de Relatórios
```http
POST /api/security/report
Content-Type: application/json

{
  "hours": 24,
  "format": "json"
}
```

**Parâmetros:**
- `hours`: Período para análise (padrão: 24)
- `format`: "json" ou "txt"

## Tipos de Eventos Registrados

### 1. Requisições HTTP (`http_request`)
- Método, endpoint, status code
- IP do cliente, User-Agent
- Tempo de processamento
- Tamanho da resposta

### 2. Autenticação (`authentication_*`)
- Login, logout, falhas de autenticação
- ID do usuário, motivo da falha
- IP de origem

### 3. Acesso a Arquivos (`file_access`)
- Operações em arquivos sensíveis
- Caminho do arquivo, tipo de operação
- Sucesso/falha da operação

### 4. Gerenciamento de API Keys (`api_key_management`)
- Criação, modificação, remoção
- Provedor da API key
- Sempre marcado como crítico

### 5. Erros do Sistema (`system_error`)
- Exceções não tratadas
- Falhas de validação
- Erros de conectividade

### 6. Ações Administrativas (`administrative_action`)
- Reset de projetos
- Alterações de configuração
- Sempre marcado como crítico

## Detecção de Atividades Suspeitas

### Múltiplas Falhas de Autenticação
```json
{
  "type": "multiple_failed_authentications",
  "description": "IP 192.168.1.100 teve 5 falhas de autenticação",
  "severity": "high",
  "ip_address": "192.168.1.100",
  "count": 5
}
```

### Alto Volume de Requisições
```json
{
  "type": "high_request_volume",
  "description": "IP 192.168.1.100 fez 150 requisições",
  "severity": "medium",
  "ip_address": "192.168.1.100",
  "count": 150
}
```

### Acesso a Arquivos Sensíveis
```json
{
  "type": "sensitive_file_access",
  "description": "Acesso a arquivo sensível: .env",
  "severity": "high",
  "file_path": ".env",
  "ip_address": "192.168.1.100"
}
```

## Configuração e Uso

### 1. Inicialização Automática
O sistema é inicializado automaticamente quando a aplicação Flask é iniciada:

```python
from auditoria_seguranca import auditoria_global

# Instância global já configurada e pronta para uso
```

### 2. Logging Manual
```python
# Log de evento de autenticação
auditoria_global.log_authentication_event(
    event_type="login",
    user_id="user123",
    success=True
)

# Log de acesso a arquivo
auditoria_global.log_file_access(
    file_path="/path/to/sensitive/file",
    operation="read",
    user_id="user123",
    success=True
)

# Log de erro
auditoria_global.log_error_event(
    error_type="validation",
    error_message="Dados inválidos fornecidos",
    user_id="user123"
)
```

### 3. Geração de Relatórios Programática
```python
# Gerar relatório em JSON
report_path = auditoria_global.export_security_report(hours=24, format='json')

# Gerar relatório em TXT
report_path = auditoria_global.export_security_report(hours=24, format='txt')
```

## Conformidade e Boas Práticas

### LGPD/GDPR
- ✅ Logs não armazenam dados pessoais sensíveis
- ✅ IPs são registrados para fins de segurança legítima
- ✅ Retenção limitada (10.000 eventos máximo)
- ✅ Possibilidade de exportação para auditoria

### ISO 27001
- ✅ Rastreabilidade completa de ações
- ✅ Detecção automática de incidentes
- ✅ Logs estruturados para análise
- ✅ Integridade dos logs protegida

### Boas Práticas
- ✅ Logs não quebram a aplicação em caso de falha
- ✅ Performance otimizada (logging assíncrono)
- ✅ Rotação automática de logs
- ✅ Múltiplos formatos para diferentes necessidades

## Monitoramento e Alertas

### Integração com Ferramentas Externas
Os logs em formato JSON podem ser facilmente integrados com:

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **Grafana + Loki**
- **Azure Monitor**
- **AWS CloudWatch**

### Exemplo de Query Elasticsearch
```json
{
  "query": {
    "bool": {
      "must": [
        {"term": {"severity": "critical"}},
        {"range": {"timestamp": {"gte": "now-1h"}}}
      ]
    }
  }
}
```

## Troubleshooting

### Logs Não Sendo Gerados
1. Verificar permissões do diretório `logs/`
2. Verificar espaço em disco
3. Verificar logs de erro da aplicação

### Performance Impact
- O sistema é otimizado para baixo impacto
- Em caso de alta carga, considerar logging assíncrono
- Monitorar tamanho dos arquivos de log

### Arquivo JSON Corrompido
```python
# Reinicializar arquivo de segurança
auditoria_global._init_security_json()
```

## Roadmap

### Próximas Funcionalidades
- [ ] Alertas em tempo real via webhook
- [ ] Dashboard web para visualização
- [ ] Integração com SIEM
- [ ] Análise de comportamento com ML
- [ ] Exportação para formatos adicionais (CSV, XML)
- [ ] Compressão automática de logs antigos

---

**Nota**: Este sistema foi projetado para ser extensível e pode ser facilmente adaptado para requisitos específicos de conformidade da sua organização.
