## Regras de Negócio
- Um cliente atual (Asegurado) pode indicar amigos e familiares (Potenciais Clientes).
- Cada indicação é rastreada pelo sistema.
- Ao aprovar uma indicação, o cliente que indicou e o indicado recebem descontos.
- O sistema envia notificações push para o cliente que indicou e para o indicado, informando sobre o status da indicação.
- Administradores da NCF têm acesso a um painel para monitorar o desempenho do programa de indicações, gerar relatórios e administrar o sistema.
- Os descontos aplicados são definidos pela NCF e podem variar.
- O sistema deve garantir a segurança e privacidade dos dados dos usuários.


## Requisitos Funcionais
- Cadastro e login de usuários (Asegurados e Administradores).
- Sistema de criação e rastreamento de indicações.
- Envio de notificações push para clientes que indicam e para os indicados.
- Painel administrativo para gerenciamento do sistema e geração de relatórios.
- Visualização de informações da apólice de seguro pelo Asegurado.
- Visualização de detalhes da indicação pelo Indicado.
- Aplicação de descontos para clientes que indicaram e para os indicados (após aprovação).
- Integração com sistema de apólices da NCF (se aplicável).


## Requisitos Não Funcionais
- Alta disponibilidade e performance do aplicativo.
- Segurança dos dados dos usuários, garantindo a confidencialidade, integridade e disponibilidade das informações.
- Interface intuitiva e amigável para todos os tipos de usuários.
- Escalabilidade para suportar um número crescente de usuários e indicações.
- Compatibilidade com diferentes dispositivos móveis (iOS e Android).
- Boas práticas de desenvolvimento de software, incluindo testes unitários, integração e sistema.
- Tempo de resposta aceitável para todas as operações do sistema.
- Design responsivo para diferentes tamanhos de tela.


## Personas de Usuário
- **Cliente Atual (Asegurado):** Usuário já cadastrado na NCF, com acesso ao aplicativo para indicar novos clientes e visualizar informações da sua apólice.
- **Potencial Cliente (Indicado):** Novo usuário indicado por um cliente atual, recebe informações sobre a indicação e o processo de adesão.
- **Administrador do Sistema NCF:** Usuário com permissões administrativas para monitorar o programa de indicações, gerar relatórios e administrar o sistema.


## Fluxos de Usuário
- **Fluxo de Indicação:**  O Asegurado acessa o aplicativo, indica um amigo ou familiar, fornecendo informações de contato. O sistema envia uma notificação para o Indicado com detalhes da indicação. O Indicado aceita ou rejeita a indicação.  Após a aprovação da indicação, o Asegurado e o Indicado recebem descontos e notificações push informando sobre a aprovação.
- **Fluxo de Administração:** O Administrador acessa o painel administrativo para monitorar as indicações, gerar relatórios, analisar o desempenho do programa e administrar usuários.
- **Fluxo de Login/Cadastro:**  Usuários (Asegurados e Administradores) realizam login ou se cadastram no aplicativo.
- **Fluxo de Visualização de Apólice:** O Asegurado visualiza as informações da sua apólice de seguro.
- **Fluxo de Visualização de Detalhes da Indicação:** O Indicado visualiza os detalhes da indicação, incluindo quem o indicou.

