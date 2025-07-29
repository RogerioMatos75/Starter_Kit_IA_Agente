# 04_fluxos_usuario.md

## Fluxos de Usuário:

**1. Fluxo de Indicador:**

* **Indicar Seguro:**
    1. Indicador acessa o aplicativo e seleciona a opção "Indicar Seguro".
    2. Seleciona o tipo de seguro a ser indicado.
    3. Preenche os dados do indicado (nome, telefone, email).  Opcionalmente, pode selecionar o indicado de uma lista de contatos previamente cadastrados.
    4. Confirma a indicação.
    5. Recebe confirmação da indicação com um ID único para acompanhamento.
    6. Monitora o status da indicação (pendente, aprovado, rejeitado) através da aba "Minhas Indicações".
    7. Caso aprovado, recebe notificação push de parabéns.

* **Gerenciar Indicações:**
    1. Indicador acessa a aba "Minhas Indicações".
    2. Visualiza lista de indicações com status, data e informações do indicado.
    3. Pode filtrar e ordenar a lista por status e data.
    4. Pode visualizar detalhes de cada indicação.
    5. Acompanha as recompensas/gamificação associadas às indicações aprovadas.


**2. Fluxo de Indicado:**

* **Receber Indicação:**
    1. Indicado recebe notificação push informando sobre uma indicação de seguro.
    2. Acessa o aplicativo e visualiza os detalhes da indicação, incluindo o nome do indicador.
    3. Pode visualizar informações sobre o seguro indicado.
    4. Pode entrar em contato com o indicador (opcional).
    5. Após aprovação da seguradora, recebe notificação com detalhes do desconto.
    6. Pode visualizar e resgatar o desconto na compra do seguro.

* **Resgatar Desconto:**
    1. Indicado acessa a aba "Meus Descontos".
    2. Seleciona o desconto disponível.
    3. Aplica o código promocional gerado pelo sistema ao finalizar a compra do seguro.


**3. Fluxo de Administrador:**

* **Gerenciamento de Usuários:**
    1. Acesso ao painel administrativo.
    2. Visualiza lista de usuários (indicadores e indicados).
    3. Pode filtrar e pesquisar usuários.
    4. Pode gerenciar contas de usuários (bloqueio, desbloqueio, etc).

* **Gerenciamento de Indicações:**
    1. Acesso à aba "Indicações".
    2. Visualiza todas as indicações (aprovadas, pendentes, rejeitadas).
    3. Pode aprovar ou rejeitar indicações.
    4. Gera relatórios sobre as indicações.

* **Gerenciamento de Seguros:**
    1. Acesso à aba "Seguros".
    2. Visualiza lista de seguros disponíveis para indicação.
    3. Pode adicionar novos seguros.
    4. Pode editar informações de seguros existentes.


## Navegação:

A navegação será intuitiva, com menus de fácil acesso e uma interface limpa e organizada. Serão utilizados menus de navegação inferior (para ações principais) e menus de navegação lateral (para configurações e informações adicionais).  Cada fluxo de usuário terá uma rota específica e clara. Exemplo:

* **Indicador:** Tela inicial -> Indicar Seguro -> Minhas Indicações -> Perfil
* **Indicado:** Tela inicial -> Meus Descontos -> Notificações -> Perfil


## Interações:

As interações serão otimizadas para garantir uma experiência fluida e agradável.  Utilizaremos botões claros e concisos, formulários fáceis de preencher e mensagens de confirmação para todas as ações.  Notificações push serão usadas para alertas importantes, como confirmação de indicações e disponibilidade de descontos. Exemplos:

* **Botões:** "Indicar Seguro", "Confirmar", "Cancelar", "Visualizar Detalhes", "Resgatar Desconto".
* **Mensagens:** "Indicação enviada com sucesso", "Sua indicação foi aprovada!", "Desconto resgatado com sucesso".
* **Notificações Push:** "Parabéns! Sua indicação foi aprovada!", "Você recebeu uma indicação de seguro!", "Seu desconto está disponível!".

O aplicativo terá um sistema de ajuda integrado para auxiliar os usuários em caso de dúvidas.
