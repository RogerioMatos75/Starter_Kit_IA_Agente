# 04_fluxos_usuario.md

## Fluxos de Usuário

### Fluxo de Cadastro e Login (Cliente Atual/Asegurado)

1. **Usuário abre o aplicativo:** Tela inicial com opção de "Cadastro" e "Login".
2. **Cadastro:** Preenche formulário com informações pessoais, contato e dados da apólice (se aplicável).  O sistema valida os dados. Em caso de erro, exibe mensagens de erro.  Sucesso: redireciona para tela de login.
3. **Login:** Insere credenciais (email/telefone e senha).  O sistema valida as credenciais. Em caso de erro, exibe mensagem de erro. Sucesso: redireciona para tela principal do usuário.
4. **Tela principal:** Exibe informações da apólice, saldo de descontos por indicações, e botão para "Criar Indicação".

### Fluxo de Criação de Indicação (Cliente Atual/Asegurado)

1. **Usuário acessa a tela de "Criar Indicação":**  Inicia o processo.
2. **Preenche informações do indicado:** Insere nome, telefone e email do indicado. O sistema valida se o indicado já está cadastrado.
3. **Envia a indicação:** O sistema envia uma notificação push para o indicado com um link para o aplicativo e informações sobre a indicação. O usuário recebe confirmação da indicação com um ID de rastreamento.
4. **Monitoramento da indicação:** O usuário pode acompanhar o status da sua indicação na tela principal.

### Fluxo de Aceitação da Indicação (Potencial Cliente/Indicado)

1. **Indicado recebe notificação push:**  Abre o link da notificação.
2. **Indicado é redirecionado para o aplicativo (ou tela de cadastro/login):** Se não estiver logado, precisa criar uma conta ou logar.
3. **Indicado visualiza informações da indicação:** Nome do cliente que o indicou e os benefícios.
4. **Indicado completa o cadastro (se necessário) e adquire o seguro:**  Após concluir o processo de aquisição, o sistema registra a indicação como concluída.

### Fluxo de Administração (Administrador do Sistema)

1. **Administrador acessa o painel administrativo:**  Login com credenciais específicas.
2. **Monitoramento do sistema:** Visualiza relatórios de indicações, número de novos clientes, descontos aplicados, etc.
3. **Gerenciamento de usuários:**  Pode visualizar informações de todos os usuários e seus respectivos status.
4. **Gerenciamento de descontos:** Aprova ou rejeita aplicações de descontos.


## Navegação

* **Tela Inicial:** Cadastro, Login.
* **Tela de Usuário (Cliente Atual):**  Informações da apólice, saldo de descontos, criar indicação, histórico de indicações.
* **Tela de Criar Indicação:** Formulário para inserir informações do indicado.
* **Tela de Detalhes da Indicação (Usuário):**  ID de rastreamento, status da indicação.
* **Tela de Detalhes da Indicação (Indicado):** Informações sobre quem indicou e instruções para prosseguir.
* **Tela de Administração:** Dashboard com métricas, gerenciamento de usuários e descontos.
* **Tela de Cadastro:** Formulário de cadastro de usuário (cliente atual e potencial).
* **Tela de Login:** Formulário de login para clientes e administrador.


## Interações

* **Cadastro:** Preencher formulários, validação de dados, mensagens de erro.
* **Login:** Inserir credenciais, validação de credenciais, mensagens de erro.
* **Criar Indicação:** Inserir informações do indicado, enviar solicitação, confirmação do envio, notificação push para o indicado.
* **Notificação Push:**  Clique para abrir o app ou website, redirecionamento para telas relevantes.
* **Visualizar informações da apólice:** Exibição de dados da apólice do usuário.
* **Visualizar detalhes da indicação:** Exibição do status da indicação e informações relevantes.
* **Aprovação de desconto:**  Administrador aprova ou rejeita descontos, atualização de status do desconto.

