# 03_regras_negocio.md

## Regras de Negócio

1. **Indicação:** Um usuário (Indicador) pode indicar um seguro para outro usuário (Indicado) através do aplicativo. A indicação deve conter informações essenciais como o nome do Indicador e o tipo de seguro indicado.

2. **Aprovação da Indicação:**  A indicação precisa ser aprovada pela seguradora para que o Indicador e o Indicado recebam os benefícios. A aprovação será verificada pela integração com o sistema da seguradora (se aplicável).

3. **Notificações Push:** Ao aprovar uma indicação, o Indicador receberá uma notificação push parabenizando-o pela indicação bem-sucedida. O Indicado receberá uma notificação push informando sobre a indicação, quem o indicou e que um consultor entrará em contato.

4. **Desconto:**  Após a aprovação da indicação, o Indicado receberá um desconto no seguro indicado, conforme as regras definidas pela seguradora.

5. **Gamificação:** O aplicativo poderá incluir um sistema de gamificação para recompensar os Indicadores com base no número de indicações aprovadas.

6. **Gerenciamento de Indicações:**  Tanto o Indicador quanto o Indicado poderão visualizar o histórico de suas indicações, incluindo status (pendente, aprovado, rejeitado) e descontos aplicados.

7. **Cadastro de Usuários:** Indicadores e Indicados devem se cadastrar no aplicativo, fornecendo as informações necessárias para identificação e contato.

8. **Resgate de Desconto:** O Indicado precisa resgatar seu desconto durante o processo de compra do seguro.  O sistema deve garantir que o desconto seja aplicado corretamente.


## Restrições

1. **Integração com Seguradora:** A integração com o sistema da seguradora para verificação de aprovação e aplicação de descontos pode apresentar limitações dependendo da API disponibilizada pela seguradora.

2. **Disponibilidade de Notificações Push:** A funcionalidade de notificações push depende da permissão do usuário e da disponibilidade de conexão com a internet.

3. **Limites de Descontos:** A seguradora poderá estabelecer limites para o valor ou número de descontos oferecidos.


## Exceções

1. **Indicação Rejeitada:** Se a indicação for rejeitada pela seguradora, o Indicador e o Indicado serão notificados sobre a rejeição, e o desconto não será aplicado.

2. **Falha na Notificação Push:** Em caso de falha no envio da notificação push, um mecanismo de fallback (ex: e-mail) deve ser considerado.

3. **Usuário sem conexão:** Em caso de ausência de conexão com a internet, o sistema deve garantir a persistência dos dados e o envio das notificações quando a conexão for restabelecida.


## Decisões

1. **Plataforma:** A decisão sobre a plataforma de desenvolvimento (nativo, híbrido, web) será tomada após a análise de viabilidade e recursos.

2. **Gamificação:** A implementação do sistema de gamificação será avaliada posteriormente, podendo ser implementada em fases.

3. **Segurança:** A segurança dos dados dos usuários será priorizada, implementando medidas para proteger as informações sensíveis.

4. **Integração com APIs externas:** A integração com APIs externas (seguradoras) será feita de maneira modular e escalável, permitindo a inclusão de novas seguradoras no futuro.
