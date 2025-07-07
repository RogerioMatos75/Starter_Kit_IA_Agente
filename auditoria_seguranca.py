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
import socket

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR_DEFAULT = os.path.join(BASE_DIR, "logs")

class AuditoriaSeguranca:
    """
    Classe principal para gerenciamento de logs de auditoria e segurança.
    """
    
    def __init__(self, log_dir: str = LOG_DIR_DEFAULT):
        self.log_dir = log_dir
        self.audit_log_path = os.path.join(self.log_dir, "auditoria.log")
        self.security_log_path = os.path.join(self.log_dir, "seguranca.json")
        
        os.makedirs(self.log_dir, exist_ok=True)
        
        self._setup_audit_logger()
        self._init_security_json()
    
    def _setup_audit_logger(self):
        """Configura o logger de auditoria."""
        self.audit_logger = logging.getLogger('auditoria_seguranca')
        self.audit_logger.setLevel(logging.INFO)
        
        for handler in self.audit_logger.handlers[:]:
            self.audit_logger.removeHandler(handler)
        
        file_handler = logging.FileHandler(self.audit_log_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
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
        """Extrai informações do cliente da requisição atual."""
        client_info = {
            "ip_address": "unknown",
            "user_agent": "unknown",
            "method": "unknown",
            "endpoint": "unknown",
            "referrer": "unknown"
        }
        
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
        """Gera um ID único para o evento."""
        data = f"{event_type}_{timestamp}_{os.getpid()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def log_http_request(self, status_code: int, user_id: Optional[str] = None, 
                        additional_data: Optional[Dict] = None):
        """Registra requisições HTTP."""
        client_info = self._get_client_info()
        timestamp = datetime.datetime.now().isoformat()
        
        log_message = (
            f"HTTP_REQUEST | {client_info['method']} {client_info['endpoint']} | "
            f"Status: {status_code} | IP: {client_info['ip_address']} | "
            f"User: {user_id or 'anonymous'} | UA: {client_info['user_agent'][:50]}..."
        )
        
        if status_code >= 400:
            self.audit_logger.warning(log_message)
        else:
            self.audit_logger.info(log_message)
        
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
    
    # ... (restante dos métodos da classe permanecem os mesmos) ...

    def _append_to_security_json(self, event_data: Dict[str, Any]):
        """Adiciona um evento ao arquivo JSON de segurança."""
        try:
            with open(self.security_log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data['events'].append(event_data)
            
            if len(data['events']) > 10000:
                data['events'] = data['events'][-10000:]
            
            data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
            data['metadata']['total_events'] = len(data['events'])
            
            with open(self.security_log_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.audit_logger.error(f"SYSTEM_ERROR | Failed to write to security JSON: {str(e)}")

# Instância global para uso em toda a aplicação
auditoria_global = AuditoriaSeguranca()

# O restante do arquivo (decoradores, etc.) permanece o mesmo.