# 🔧 Guia de Solução - Erros de Conectividade

## Problema Identificado

Se você está vendo os seguintes erros:

- `Erro ao verificar a chave da API: TypeError: Failed to fetch`
- `Could not fetch project status: TypeError: Failed to fetch`
- `Erro ao carregar API Keys: TypeError: Failed to fetch`

**Causa:** O servidor Flask não está rodando ou não está acessível.

## ✅ Solução Rápida

### 1. Iniciar o Servidor Flask

#### Opção A: Script Automatizado (Recomendado)

```bash
python start_server.py
```

#### Opção B: Comando Direto

```bash
python app.py
```

### 2. Verificar se o Servidor Está Funcionando

Após iniciar o servidor, acesse:

- **URL Principal:** http://localhost:5001
- **Dashboard:** http://localhost:5001/dashboard
- **Teste de API:** http://localhost:5001/api/status

## 🔍 Diagnóstico Detalhado

### Verificar Dependências

```bash
pip install -r requirements.txt
```

### Verificar Porta 5001

Se a porta 5001 estiver ocupada, você pode:

#### Windows:

```cmd
netstat -ano | findstr :5001
```

#### Linux/Mac:

```bash
lsof -i :5001
```

### Verificar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
GEMINI_API_KEY=sua_chave_aqui
FLASK_SECRET_KEY=sua_chave_secreta
STRIPE_SECRET_KEY=sua_chave_stripe (opcional)
STRIPE_PUBLIC_KEY=sua_chave_publica_stripe (opcional)
```

## 🆘 Troubleshooting Avançado

### Erro: "Módulo não encontrado"

```bash
pip install flask flask-cors python-dotenv google-generativeai
```

### Erro: "Porta já está em uso"

Edite o arquivo `app.py` linha 579:

```python
app.run(debug=True, port=5002)  # Mude para porta 5002
```

### Erro: "CORS Policy"

O projeto já tem CORS configurado. Se ainda houver problemas:

1. Verifique se `Flask-Cors` está instalado
2. Reinicie o servidor
3. Limpe o cache do navegador

### Erro: "Arquivo workflow.json não encontrado"

```bash
# Verifique se o arquivo existe
ls workflow.json

# Se não existir, restaure do backup ou repositório
```

## 🔄 Reinicialização Completa

Se nada funcionar, tente uma reinicialização completa:

```bash
# 1. Pare o servidor (Ctrl+C se estiver rodando)

# 2. Reinstale dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# 3. Reinicie o servidor
python start_server.py
```

## 📞 Suporte

Se o problema persistir:

1. Verifique se todas as dependências estão instaladas
2. Confirme que está no diretório correto do projeto
3. Verifique as permissões de arquivo
4. Teste em um ambiente virtual Python limpo

## 🎯 Verificação de Sucesso

Quando tudo estiver funcionando:

- ✅ Servidor rodando na porta 5001
- ✅ Dashboard acessível
- ✅ API respondendo corretamente
- ✅ Sem erros "Failed to fetch" no console
- ✅ Banner de conectividade removido da interface
