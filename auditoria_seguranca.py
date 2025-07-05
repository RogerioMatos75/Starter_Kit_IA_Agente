"""
Módulo de Auditoria de Segurança - Archon AI
Sistema completo de logs de segurança para rastreamento, auditoria e conformidade.
"""

import os
import json
import logging
import datetime
from functools import wraps
from flask import request, g
from typing import Dict, Any, Optional
import hashlib
import hashlib
import socket

class AuditoriaSeguranca:
    """
    Classe principal para gerenciamento de logs de auditoria e segurança.
    Implementa logging estruturado em JSON e texto legível.
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.audit_log_path = os.path.join(log_dir, "auditoria.log")
        self.security_log_path = os.path.join(log_dir, "seguranca.json")
        
        # Cria o diretório de logs se não existir
        os.makedirs(log_dir, exist_ok=True)
        
        # Configura o logger de auditoria
        self._setup_audit_logger()
        
        # Inicializa arquivo JSON de segurança se não existir
        self._init_security_json()
    
    def _setup_audit_logger(self):
        """Configura o logger de auditoria com formatação personalizada."""
        self.audit_logger = logging.getLogger('auditoria_seguranca')
        self.audit_logger.setLevel(logging.INFO)
        
        # Remove handlers existentes para evitar duplicação
        for handler in self.audit_logger.handlers[:]:
            self.audit_logger.removeHandler(handler)
        
        # Handler para arquivo de auditoria
        file_handler = logging.FileHandler(self.audit_log_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Formato detalhado para logs de auditoria
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self.audit_logger.addHandler(file_handler)
        self.audit_logger.propagate = False
    
    def _init_security_json(self):
        """Inicializa o arquivo JSON de segurança se não existir."""
        if not os.path.exists(self.security_log_path):
            initial_data = {
                "metadata": {
                    "created_at": datetime.datetime.now().isoformat(),
                    "version": "1.0",
                    "description": "Log de segurança estruturado - Archon AI"
                },
                "events": []
            }
            with open(self.security_log_path, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2, ensure_ascii=False)
    
    def _get_client_info(self) -> Dict[str, Any]:
        """Extrai informações do cliente da requisição atual, se disponível."""
        client_info = {
            "ip_address": "unknown",
            "user_agent": "unknown",
            "method": "unknown",
            "endpoint": "unknown",
            "referrer": "unknown"
        }
        
        # Verifica se há um contexto de requisição Flask ativo
        if request and hasattr(request, 'remote_addr'):
            client_info.update({
                "ip_address": request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
                "user_agent": request.headers.get('User-Agent', 'unknown'),
                "method": request.method,
                "endpoint": request.endpoint or request.path,
                "referrer": request.headers.get('Referer', 'direct')
            })
        
        return client_info
    
    def _generate_event_id(self, event_type: str, timestamp: str) -> str:
        """Gera um ID único para o evento baseado no tipo e timestamp."""
        data = f"{event_type}_{timestamp}_{os.getpid()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def log_http_request(self, status_code: int, user_id: Optional[str] = None, 
                        additional_data: Optional[Dict] = None):
        """
        Registra requisições HTTP com detalhes de segurança.
        
        Args:
            status_code: Código de status HTTP da resposta
            user_id: ID do usuário autenticado (se aplicável)
            additional_data: Dados adicionais para o log
        """
        client_info = self._get_client_info()
        timestamp = datetime.datetime.now().isoformat()
        
        # Log em formato legível
        log_message = (
            f"HTTP_REQUEST | {client_info['method']} {client_info['endpoint']} | "
            f"Status: {status_code} | IP: {client_info['ip_address']} | "
            f"User: {user_id or 'anonymous'} | UA: {client_info['user_agent'][:50]}..."
        )
        
        if status_code >= 400:
            self.audit_logger.warning(log_message)
        else:
            self.audit_logger.info(log_message)
        
        # Log estruturado em JSON
        event_data = {
            "event_id": self._generate_event_id("http_request", timestamp),
            "timestamp": timestamp,
            "event_type": "http_request",
            "severity": "warning" if status_code >= 400 else "info",
            "client_info": client_info,
            "response": {
                "status_code": status_code
            },
            "user": {
                "user_id": user_id,
                "authenticated": bool(user_id)
            },
            "additional_data": additional_data or {}
        }
        
        self._append_to_security_json(event_data)
    
    def log_authentication_event(self, event_type: str, user_id: Optional[str] = None, 
                                success: bool = True, reason: Optional[str] = None):
        """
        Registra eventos de autenticação.
        
        Args:
            event_type: Tipo do evento (login, logout, failed_login, etc.)
            user_id: ID do usuário
            success: Se a autenticação foi bem-sucedida
            reason: Motivo da falha (se aplicável)
        """
        client_info = self._get_client_info()
        timestamp = datetime.datetime.now().isoformat()
        
        # Log em formato legível
        status = "SUCCESS" if success else "FAILED"
        log_message = (
            f"AUTH_{event_type.upper()} | {status} | "
            f"User: {user_id or 'unknown'} | IP: {client_info['ip_address']}"
        )
        
        if reason:
            log_message += f" | Reason: {reason}"
        
        if success:
            self.audit_logger.info(log_message)
        else:
            self.audit_logger.warning(log_message)
        
        # Log estruturado em JSON
        event_data = {
            "event_id": self._generate_event_id("auth", timestamp),
            "timestamp": timestamp,
            "event_type": f"authentication_{event_type}",
            "severity": "info" if success else "warning",
            "client_info": client_info,
            "authentication": {
                "user_id": user_id,
                "success": success,
                "reason": reason,
                "event_subtype": event_type
            }
        }
        
        self._append_to_security_json(event_data)
    
    def log_file_access(self, file_path: str, operation: str, user_id: Optional[str] = None,
                       success: bool = True, reason: Optional[str] = None):
        """
        Registra acessos a arquivos sensíveis.
        
        Args:
            file_path: Caminho do arquivo acessado
            operation: Tipo de operação (read, write, delete, etc.)
            user_id: ID do usuário que realizou a operação
            success: Se a operação foi bem-sucedida
            reason: Motivo da falha (se aplicável)
        """
        client_info = self._get_client_info()
        timestamp = datetime.datetime.now().isoformat()
        
        # Log em formato legível
        status = "SUCCESS" if success else "FAILED"
        log_message = (
            f"FILE_ACCESS | {operation.upper()} | {status} | "
            f"File: {file_path} | User: {user_id or 'system'} | "
            f"IP: {client_info['ip_address']}"
        )
        
        if reason:
            log_message += f" | Reason: {reason}"
        
        if success:
            self.audit_logger.info(log_message)
        else:
            self.audit_logger.warning(log_message)
        
        # Log estruturado em JSON
        event_data = {
            "event_id": self._generate_event_id("file_access", timestamp),
            "timestamp": timestamp,
            "event_type": "file_access",
            "severity": "info" if success else "warning",
            "client_info": client_info,
            "file_operation": {
                "file_path": file_path,
                "operation": operation,
                "success": success,
                "reason": reason
            },
            "user": {
                "user_id": user_id
            }
        }
        
        self._append_to_security_json(event_data)
    
    def log_api_key_event(self, operation: str, provider: str, user_id: Optional[str] = None,
                         success: bool = True, reason: Optional[str] = None):
        """
        Registra eventos relacionados a API keys.
        
        Args:
            operation: Operação realizada (create, update, delete, test)
            provider: Provedor da API key (gemini, openai, etc.)
            user_id: ID do usuário que realizou a operação
            success: Se a operação foi bem-sucedida
            reason: Motivo da falha (se aplicável)
        """
        client_info = self._get_client_info()
        timestamp = datetime.datetime.now().isoformat()
        
        # Log em formato legível
        status = "SUCCESS" if success else "FAILED"
        log_message = (
            f"API_KEY_{operation.upper()} | {status} | "
            f"Provider: {provider} | User: {user_id or 'system'} | "
            f"IP: {client_info['ip_address']}"
        )
        
        if reason:
            log_message += f" | Reason: {reason}"
        
        # API keys são sempre eventos críticos
        self.audit_logger.warning(log_message)
        
        # Log estruturado em JSON
        event_data = {
            "event_id": self._generate_event_id("api_key", timestamp),
            "timestamp": timestamp,
            "event_type": "api_key_management",
            "severity": "critical",
            "client_info": client_info,
            "api_key_operation": {
                "operation": operation,
                "provider": provider,
                "success": success,
                "reason": reason
            },
            "user": {
                "user_id": user_id
            }
        }
        
        self._append_to_security_json(event_data)
    
    def log_error_event(self, error_type: str, error_message: str, 
                       user_id: Optional[str] = None, additional_data: Optional[Dict] = None):
        """
        Registra erros e exceções do sistema.
        
        Args:
            error_type: Tipo do erro (validation, database, api, etc.)
            error_message: Mensagem de erro
            user_id: ID do usuário relacionado ao erro
            additional_data: Dados adicionais sobre o erro
        """
        client_info = self._get_client_info()
        timestamp = datetime.datetime.now().isoformat()
        
        # Log em formato legível
        log_message = (
            f"ERROR | {error_type.upper()} | "
            f"Message: {error_message[:100]}... | "
            f"User: {user_id or 'system'} | IP: {client_info['ip_address']}"
        )
        
        self.audit_logger.error(log_message)
        
        # Log estruturado em JSON
        event_data = {
            "event_id": self._generate_event_id("error", timestamp),
            "timestamp": timestamp,
            "event_type": "system_error",
            "severity": "error",
            "client_info": client_info,
            "error": {
                "error_type": error_type,
                "message": error_message,
                "additional_data": additional_data or {}
            },
            "user": {
                "user_id": user_id
            }
        }
        
        self._append_to_security_json(event_data)
    
    def log_admin_action(self, action: str, target: str, user_id: str,
                        success: bool = True, reason: Optional[str] = None):
        """
        Registra ações administrativas críticas.
        
        Args:
            action: Ação realizada (reset_project, change_config, etc.)
            target: Alvo da ação (project, user, system, etc.)
            user_id: ID do usuário administrador
            success: Se a ação foi bem-sucedida
            reason: Motivo da falha (se aplicável)
        """
        client_info = self._get_client_info()
        timestamp = datetime.datetime.now().isoformat()
        
        # Log em formato legível
        status = "SUCCESS" if success else "FAILED"
        log_message = (
            f"ADMIN_ACTION | {action.upper()} | {status} | "
            f"Target: {target} | Admin: {user_id} | "
            f"IP: {client_info['ip_address']}"
        )
        
        if reason:
            log_message += f" | Reason: {reason}"
        
        # Ações administrativas são sempre críticas
        self.audit_logger.warning(log_message)
        
        # Log estruturado em JSON
        event_data = {
            "event_id": self._generate_event_id("admin", timestamp),
            "timestamp": timestamp,
            "event_type": "administrative_action",
            "severity": "critical",
            "client_info": client_info,
            "admin_action": {
                "action": action,
                "target": target,
                "success": success,
                "reason": reason
            },
            "user": {
                "user_id": user_id,
                "role": "admin"
            }
        }
        
        self._append_to_security_json(event_data)

    def log_artefacto_gerado(self, project_name: str, file_path: str, file_content: str):
        """
        Registra a criação de um artefato de código ou documento pela IA.
        Inclui um hash do conteúdo para verificação de integridade.

        Args:
            project_name: Nome do projeto ao qual o artefato pertence.
            file_path: Caminho completo do arquivo gerado.
            file_content: Conteúdo do arquivo para gerar o hash.
        """
        client_info = self._get_client_info()
        timestamp = datetime.datetime.now().isoformat()

        # Calcula o hash SHA-256 do conteúdo do arquivo
        content_hash = hashlib.sha256(file_content.encode('utf-8')).hexdigest()

        # Log em formato legível
        log_message = (
            f"ARTEFACT_GENERATED | Project: {project_name} | "
            f"File: {file_path} | Size: {len(file_content)} bytes | "
            f"Hash: {content_hash[:12]}..."
        )
        self.audit_logger.info(log_message)

        # Log estruturado em JSON para o "SpyNice"
        event_data = {
            "event_id": self._generate_event_id("artefact_generation", timestamp),
            "timestamp": timestamp,
            "event_type": "artefact_generation",
            "severity": "info",
            "client_info": client_info,
            "artefact_details": {
                "project_name": project_name,
                "file_path": file_path,
                "file_size_bytes": len(file_content),
                "content_hash_sha256": content_hash,
                "generated_by": "Archon AI FSM"
            },
            "user": {
                "user_id": getattr(g, 'user_id', 'system')
            }
        }

        self._append_to_security_json(event_data)


    
    def _append_to_security_json(self, event_data: Dict[str, Any]):
        """Adiciona um evento ao arquivo JSON de segurança."""
        try:
            # Lê o arquivo atual
            with open(self.security_log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Adiciona o novo evento
            data['events'].append(event_data)
            
            # Mantém apenas os últimos 10000 eventos para evitar arquivos muito grandes
            if len(data['events']) > 10000:
                data['events'] = data['events'][-10000:]
            
            # Atualiza metadata
            data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
            data['metadata']['total_events'] = len(data['events'])
            
            # Salva o arquivo
            with open(self.security_log_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            # Se falhar ao escrever no JSON, pelo menos registra no log de auditoria
            self.audit_logger.error(f"SYSTEM_ERROR | Failed to write to security JSON: {str(e)}")
    
    def get_security_summary(self, hours: int = 24) -> Dict[str, Any]:
        """
        Retorna um resumo dos eventos de segurança das últimas N horas.
        
        Args:
            hours: Número de horas para análise (padrão: 24)
            
        Returns:
            Dicionário com estatísticas de segurança
        """
        try:
            with open(self.security_log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Calcula o timestamp de corte
            cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
            cutoff_iso = cutoff_time.isoformat()
            
            # Filtra eventos recentes
            recent_events = [
                event for event in data['events']
                if event['timestamp'] >= cutoff_iso
            ]
            
            # Calcula estatísticas
            summary = {
                "period_hours": hours,
                "total_events": len(recent_events),
                "events_by_type": {},
                "events_by_severity": {},
                "failed_authentications": 0,
                "error_events": 0,
                "admin_actions": 0,
                "unique_ips": set(),
                "top_endpoints": {},
                "suspicious_activity": []
            }
            
            for event in recent_events:
                # Contagem por tipo
                event_type = event.get('event_type', 'unknown')
                summary['events_by_type'][event_type] = summary['events_by_type'].get(event_type, 0) + 1
                
                # Contagem por severidade
                severity = event.get('severity', 'unknown')
                summary['events_by_severity'][severity] = summary['events_by_severity'].get(severity, 0) + 1
                
                # Estatísticas específicas
                if event_type.startswith('authentication') and not event.get('authentication', {}).get('success', True):
                    summary['failed_authentications'] += 1
                
                if severity == 'error':
                    summary['error_events'] += 1
                
                if event_type == 'administrative_action':
                    summary['admin_actions'] += 1
                
                # IPs únicos
                ip = event.get('client_info', {}).get('ip_address')
                if ip:
                    summary['unique_ips'].add(ip)
                
                # Endpoints mais acessados
                endpoint = event.get('client_info', {}).get('endpoint')
                if endpoint:
                    summary['top_endpoints'][endpoint] = summary['top_endpoints'].get(endpoint, 0) + 1
            
            # Converte set para lista para serialização JSON
            summary['unique_ips'] = list(summary['unique_ips'])
            
            # Ordena endpoints por frequência
            summary['top_endpoints'] = dict(sorted(
                summary['top_endpoints'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10])  # Top 10 endpoints
            
            # Detecta atividade suspeita
            summary['suspicious_activity'] = self._detect_suspicious_activity(recent_events)
            
            return summary
            
        except Exception as e:
            return {
                "error": f"Falha ao gerar resumo de segurança: {str(e)}",
                "period_hours": hours,
                "total_events": 0
            }
    
    def _detect_suspicious_activity(self, events: list) -> list:
        """
        Detecta padrões suspeitos nos eventos de segurança.
        
        Args:
            events: Lista de eventos para análise
            
        Returns:
            Lista de atividades suspeitas detectadas
        """
        suspicious = []
        
        # Agrupa eventos por IP
        ip_events = {}
        for event in events:
            ip = event.get('client_info', {}).get('ip_address', 'unknown')
            if ip not in ip_events:
                ip_events[ip] = []
            ip_events[ip].append(event)
        
        # Detecta múltiplas falhas de autenticação do mesmo IP
        for ip, ip_event_list in ip_events.items():
            failed_auths = [
                e for e in ip_event_list 
                if e.get('event_type', '').startswith('authentication') 
                and not e.get('authentication', {}).get('success', True)
            ]
            
            if len(failed_auths) >= 5:
                suspicious.append({
                    "type": "multiple_failed_authentications",
                    "description": f"IP {ip} teve {len(failed_auths)} falhas de autenticação",
                    "severity": "high",
                    "ip_address": ip,
                    "count": len(failed_auths)
                })
            
            # Detecta muitas requisições do mesmo IP (possível DoS)
            if len(ip_event_list) >= 100:
                suspicious.append({
                    "type": "high_request_volume",
                    "description": f"IP {ip} fez {len(ip_event_list)} requisições",
                    "severity": "medium",
                    "ip_address": ip,
                    "count": len(ip_event_list)
                })
        
        # Detecta tentativas de acesso a arquivos sensíveis
        sensitive_files = ['.env', 'config', 'password', 'key', 'secret']
        for event in events:
            if event.get('event_type') == 'file_access':
                file_path = event.get('file_operation', {}).get('file_path', '').lower()
                if any(sensitive in file_path for sensitive in sensitive_files):
                    suspicious.append({
                        "type": "sensitive_file_access",
                        "description": f"Acesso a arquivo sensível: {file_path}",
                        "severity": "high",
                        "file_path": file_path,
                        "ip_address": event.get('client_info', {}).get('ip_address')
                    })
        
        return suspicious
    
    def export_security_report(self, hours: int = 24, format: str = 'json') -> str:
        """
        Exporta um relatório de segurança completo.
        
        Args:
            hours: Período para análise em horas
            format: Formato do relatório ('json' ou 'txt')
            
        Returns:
            Caminho do arquivo gerado
        """
        summary = self.get_security_summary(hours)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format.lower() == 'json':
            filename = f"relatorio_seguranca_{timestamp}.json"
            filepath = os.path.join(self.log_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
                
        else:  # formato txt
            filename = f"relatorio_seguranca_{timestamp}.txt"
            filepath = os.path.join(self.log_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("RELATÓRIO DE SEGURANÇA - ARCHON AI\n")
                f.write("=" * 60 + "\n")
                f.write(f"Período: Últimas {hours} horas\n")
                f.write(f"Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                f.write("RESUMO GERAL:\n")
                f.write(f"- Total de eventos: {summary.get('total_events', 0)}\n")
                f.write(f"- IPs únicos: {len(summary.get('unique_ips', []))}\n")
                f.write(f"- Falhas de autenticação: {summary.get('failed_authentications', 0)}\n")
                f.write(f"- Eventos de erro: {summary.get('error_events', 0)}\n")
                f.write(f"- Ações administrativas: {summary.get('admin_actions', 0)}\n\n")
                
                f.write("EVENTOS POR TIPO:\n")
                for event_type, count in summary.get('events_by_type', {}).items():
                    f.write(f"- {event_type}: {count}\n")
                f.write("\n")
                
                f.write("EVENTOS POR SEVERIDADE:\n")
                for severity, count in summary.get('events_by_severity', {}).items():
                    f.write(f"- {severity.upper()}: {count}\n")
                f.write("\n")
                
                f.write("TOP ENDPOINTS ACESSADOS:\n")
                for endpoint, count in summary.get('top_endpoints', {}).items():
                    f.write(f"- {endpoint}: {count} acessos\n")
                f.write("\n")
                
                suspicious = summary.get('suspicious_activity', [])
                if suspicious:
                    f.write("ATIVIDADES SUSPEITAS DETECTADAS:\n")
                    for activity in suspicious:
                        f.write(f"- [{activity['severity'].upper()}] {activity['description']}\n")
                else:
                    f.write("ATIVIDADES SUSPEITAS: Nenhuma detectada\n")
        
        return filepath


# Decorador para logging automático de requisições HTTP
def log_http_request(auditoria: AuditoriaSeguranca):
    """
    Decorador para logging automático de requisições HTTP.
    
    Args:
        auditoria: Instância da classe AuditoriaSeguranca
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Executa a função original
                result = f(*args, **kwargs)
                
                # Determina o status code
                if hasattr(result, 'status_code'):
                    status_code = result.status_code
                elif isinstance(result, tuple) and len(result) > 1:
                    status_code = result[1]
                else:
                    status_code = 200
                
                # Log da requisição
                auditoria.log_http_request(
                    status_code=status_code,
                    user_id=getattr(g, 'user_id', None)
                )
                
                return result
                
            except Exception as e:
                # Log do erro
                auditoria.log_error_event(
                    error_type="request_handler",
                    error_message=str(e),
                    user_id=getattr(g, 'user_id', None)
                )
                raise
                
        return decorated_function
    return decorator


# Instância global para uso em toda a aplicação
auditoria_global = AuditoriaSeguranca()
