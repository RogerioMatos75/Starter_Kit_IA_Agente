## Regras de Negócio

* **Indicação:**  Um cliente (Indicação) pode indicar outro cliente (Indicado) para adquirir um seguro.
* **Aprovação:** A indicação precisa ser aprovada pela NCF Indicação Seguros para que o cliente que indicou e o indicado recebam os benefícios.  A aprovação envolve a verificação dos dados do indicado e a efetiva contratação do seguro pelo indicado.
* **Desconto:**  Tanto o cliente que indicou (Indicação) quanto o indicado recebem um desconto no seguro. A porcentagem do desconto deve ser definida e configurada na plataforma.
* **Notificação:** Ao aprovar a indicação, tanto a Indicação quanto o Indicado recebem uma notificação push. A notificação para a Indicação parabeniza pela indicação bem-sucedida. A notificação para o Indicado inclui informações sobre quem o indicou e a promessa de contato de um consultor.
* **Consultor:** Após a aprovação da indicação, um consultor da NCF Indicação Seguros deve entrar em contato com o Indicado.
* **Cadastro:** O indicado precisa ter um cadastro completo e aprovado na plataforma.
* **Limite de Indicações:**  Pode haver um limite de indicações por cliente (Indicação) em um determinado período, este limite deve ser configurado na plataforma.
* **Identificação:**  A plataforma deve manter um registro claro da relação entre Indicação e Indicado, com a data da indicação e o status da aprovação.


## Restrições

* **Dados do Indicado:**  A informação fornecida pelo Indicado na indicação deve ser precisa e validada pela NCF Indicação Seguros. Dados inconsistentes ou inválidos podem impedir a aprovação da indicação.
* **Validação de Cadastro:** O cadastro do indicado deve atender a todos os requisitos definidos pela NCF Indicação Seguros.
* **Integração com Sistema de Seguros:** A plataforma precisa se integrar com o sistema de seguros da NCF para processar as informações de contratação e aplicar os descontos.
* **Disponibilidade do Consultor:** A garantia de um retorno do consultor ao indicado dentro de um tempo hábil deve ser considerada.

## Exceções

* **Indicação Rejeitada:** Caso a indicação seja rejeitada, tanto a Indicação quanto o Indicado devem ser notificados com o motivo da rejeição.
* **Erro na Notificação:**  O sistema deve ter mecanismos de tratamento de erros para garantir que as notificações push sejam entregues corretamente. Caso contrário, deve existir um mecanismo de reenvio.
* **Falha na Integração:**  Se houver falha na integração com o sistema de seguros, a indicação deve ser colocada em um estado de pendência, e um alerta deve ser gerado para a equipe de administração.
* **Consultor Indisponível:**  Deve haver um protocolo para lidar com situações onde o consultor não consegue entrar em contato com o indicado dentro do prazo estabelecido.

## Decisões

* **Tecnologia:** A tecnologia para desenvolvimento do aplicativo será definida em outra etapa do projeto.
* **Design da Interface:** O design da interface do usuário será definido após a aprovação das regras de negócio.
* **Metodologia de Desenvolvimento:** A metodologia de desenvolvimento será definida em outra etapa do projeto.
* **Sistema de Notificações:** O sistema de notificações push será integrado com um provedor externo.
* **Plataforma de Administração:** Uma plataforma de administração será desenvolvida para monitorar as indicações, aprovações, descontos e relatórios.

