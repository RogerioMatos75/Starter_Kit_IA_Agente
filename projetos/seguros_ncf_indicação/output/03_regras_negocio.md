## Regras de Negócio

* **Cadastro e Login:** Usuários (assegurados e administradores) devem realizar cadastro com informações completas e válidas.  O login será realizado por meio de credenciais (usuário e senha).  A senha deverá atender a critérios de segurança mínimos (tamanho, caracteres especiais, etc.).
* **Indicação:** Um usuário (assegurado) pode indicar um número ilimitado de potenciais clientes.  Cada indicação deve conter informações mínimas do indicado (nome, telefone e e-mail).  A indicação é rastreada pelo sistema, associada ao usuário que indicou.
* **Aprovação da Indicação:** A indicação só é considerada válida após a aprovação do potencial cliente pela NCF.
* **Notificações Push:** Ao aprovar a indicação, o usuário que indicou recebe uma notificação push parabenizando-o pela indicação. O indicado recebe uma notificação push com informações sobre quem o indicou e um aviso de que um consultor entrará em contato.
* **Desconto:**  Ao aprovar a indicação, tanto o usuário que indicou quanto o indicado receberão um desconto predefinido na apólice de seguro. O valor do desconto será definido pela NCF.
* **Administrador:** O administrador tem acesso a um painel com relatórios completos sobre o programa de indicações, incluindo o número de indicações, aprovações, descontos aplicados e outras métricas relevantes. O administrador pode gerenciar usuários e aprovar/rejeitar indicações.
* **Apólice de Seguro:** As informações da apólice de seguro estarão disponíveis para o segurado no aplicativo.


## Restrições

* O sistema deve ser escalável para suportar um número crescente de usuários e indicações.
* O sistema deve ser seguro, protegendo as informações dos usuários e garantindo a confidencialidade dos dados.
* O tempo de resposta do aplicativo deve ser otimizado para garantir uma boa experiência do usuário.
* A integração com os sistemas existentes da NCF deve ser eficiente e sem falhas.


## Exceções

* **Indicação Rejeitada:** Se a indicação for rejeitada, tanto o usuário que indicou quanto o indicado receberão uma notificação push explicando o motivo da rejeição.
* **Falha no envio de notificação Push:** Em caso de falha no envio da notificação push, o sistema registrará o erro e tentará reenviá-la posteriormente.  Um alerta será exibido ao administrador sobre as falhas de envio.
* **Dados Incompletos:** Caso o usuário não preencha todos os campos obrigatórios no cadastro ou na criação de uma indicação, o sistema apresentará uma mensagem de erro indicando os campos faltantes.


## Decisões

* Foi decidido utilizar notificações push como o principal meio de comunicação com os usuários.
* Foi definido que o desconto será aplicado após a aprovação da indicação pelo administrador.
* A plataforma de desenvolvimento será escolhida com base em critérios de escalabilidade, segurança e custo.
*  A interface do usuário será desenvolvida com foco na usabilidade e simplicidade.
