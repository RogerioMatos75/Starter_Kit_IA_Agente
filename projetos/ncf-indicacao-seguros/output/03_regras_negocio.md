## Regras de Negócio

* **Indicação:** Um usuário (assegurado) pode indicar amigos e parentes para contratar seguros.  A indicação deve incluir nome, telefone e e-mail do indicado. O sistema deve verificar se o indicado já é cliente.
* **Desconto:**  Por cada indicação válida (indicado aprovado e contatado), o usuário que indicou recebe 1% de desconto na sua apólice.  Se o indicado contratar o seguro, o usuário ganha mais 1% de desconto adicional. O desconto máximo acumulativo é de 10% ao ano na apólice.  O desconto é aplicado anualmente e não é cumulativo entre anos.
* **Aprovação:** As indicações ficam pendentes até serem aprovadas por um administrador.  Após a aprovação, o usuário que indicou recebe uma notificação push. O indicado recebe uma notificação com os dados de quem o indicou e a informação que será contatado por um consultor.
* **Notificações Push:** Notificações push são enviadas ao administrador para novas indicações e ao usuário que indicou após a confirmação da indicação e concessão do desconto.
* **Administrador:** O administrador pode visualizar as indicações, aprovar/rejeitar indicações, enviar link da proposta ao indicado e registrar a contratação do seguro pelo indicado.  O administrador também pode gerar relatórios sobre indicações, conversões e descontos.
* **Autenticação:** O sistema utiliza autenticação segura para usuários (assegurados) e administrador, com logins separados.


## Restrições

* **Desconto Máximo:** O desconto máximo acumulado é de 10% ao ano na apólice, independente do número de indicações bem sucedidas.
* **Validação de Dados:**  Todos os dados de indicação (nome, email, telefone) devem ser validados para garantir a integridade dos dados.  O email do indicado deve ser único.
* **Integração Externa:** A integração com outros sistemas (CRM da seguradora) deve ser definida e especificada em separado.  Dependências externas podem impactar os prazos e funcionalidades.
* **Plataforma:** O aplicativo será um PWA (Progressive Web App), com foco em compatibilidade e performance em diferentes dispositivos.

## Exceções

* **Indicação Inválida:** Se o indicado já for cliente, a indicação é considerada inválida e não gera desconto. Uma mensagem de erro deve ser exibida ao usuário.
* **Indicação Rejeitada:**  O administrador pode rejeitar uma indicação.  Neste caso, o usuário que indicou não recebe desconto e não recebe notificação de confirmação.  O indicado não recebe uma notificação.
* **Falha na Notificação Push:**  Em caso de falha no envio de notificações push, o sistema deve registrar o erro e tentar novamente mais tarde. O administrador deve ser notificado sobre as falhas.
* **Erro de processamento:** Em caso de erros de processamento, o sistema deve exibir mensagens de erro claras para o usuário e registrar os logs para posterior análise.

## Decisões

* **Tecnologia Frontend:** React foi escolhido pelo seu ecossistema robusto, facilidade de componentização e larga utilização para PWA.
* **Tecnologia Backend:** Node.js com Express foi escolhido pela consistência com a tecnologia frontend (JavaScript) e pela sua leveza e flexibilidade.
* **Banco de Dados:** PostgreSQL foi selecionado pela sua confiabilidade e escalabilidade para o armazenamento de dados estruturados.
* **Notificações Push:** Firebase Cloud Messaging (FCM) será usado por sua integração facilitada e confiabilidade.
* **Autenticação:** JWT (JSON Web Tokens) será utilizado para autenticação e autorização seguras.
* **Estratégia de Cache:** Cache-First para assets estáticos e Network-First para dados dinâmicos serão utilizados.