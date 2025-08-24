## Fluxos de Usuário

**Fluxo 1: Usuário indica um amigo (Assegurado)**

1. Usuário acessa a seção "Indique um Amigo" no aplicativo.
2. Usuário insere os dados do amigo (nome, telefone, email).
3. Usuário confirma a indicação.
4. Sistema envia notificação push para o usuário confirmando o recebimento da indicação.
5. Sistema envia notificação push para o amigo indicado com os dados do usuário que o indicou e a informação de que um consultor entrará em contato.
6. Consultor entra em contato com o amigo indicado.
7. Se o amigo indicado for aprovado, o usuário recebe uma notificação push de recompensa.


**Fluxo 2: Amigo Indicado (Novo Usuário)**

1. Amigo indicado recebe notificação push com os dados do usuário que o indicou.
2. Amigo indicado acessa o aplicativo através do link na notificação push ou diretamente.
3. Amigo indicado preenche o formulário de cadastro.
4. Amigo indicado conclui o processo de cadastro e aprovação do seguro.

**Fluxo 3: Administrador**

1. Administrador acessa o painel administrativo.
2. Administrador visualiza relatórios de indicações.
3. Administrador gerencia usuários.
4. Administrador monitora o processo de aprovação de novos usuários.
5. Administrador configura as campanhas de incentivo.



## Navegação

**Assegurado:**

* Tela inicial
* Seção "Indique um Amigo"
* Tela de inserção de dados do indicado
* Tela de confirmação de indicação
* Notificações Push

**Indicado:**

* Tela inicial (após clicar no link da notificação)
* Tela de cadastro
* Tela de aprovação do seguro

**Administrador:**

* Tela de login
* Painel administrativo (dashboard)
* Relatórios de indicações
* Gerenciamento de usuários
* Configuração de campanhas


## Interações

**Assegurado:**

* **Ação:** Clicar em "Indique um Amigo".
* **Resposta:** Abre a tela de inserção de dados do indicado.
* **Ação:** Inserir dados do amigo.
* **Resposta:** Validação dos dados.
* **Ação:** Confirmar indicação.
* **Resposta:** Notificação push de confirmação e envio de notificação para o indicado.

**Indicado:**

* **Ação:** Clicar no link da notificação.
* **Resposta:** Abre a tela inicial do aplicativo.
* **Ação:** Preencher o formulário de cadastro.
* **Resposta:** Validação dos dados.
* **Ação:** Enviar formulário.
* **Resposta:** Notificação de aprovação ou rejeição.

**Administrador:**

* **Ação:** Acessar o painel administrativo.
* **Resposta:** Dashboard com métricas.
* **Ação:** Visualizar relatórios.
* **Resposta:** Exibição de relatórios detalhados.
* **Ação:** Gerenciar usuários.
* **Resposta:** Acesso às informações e ações sobre os usuários.

