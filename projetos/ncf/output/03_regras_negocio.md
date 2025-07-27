# 03_regras_negocio.md

## Regras de Negócio

1. **Indicação de Seguro:** Um usuário (Indicador) pode indicar um seguro para outro usuário (Indicado) através do aplicativo.  A indicação deve conter informações mínimas: nome do Indicador, dados de contato do Indicado, tipo de seguro e, opcionalmente, outras informações relevantes.

2. **Aprovação da Indicação:** A indicação só será considerada válida após a aprovação do Indicado e a contratação do seguro.  A aprovação será confirmada por meio do sistema e poderá envolver a verificação de dados e/ou etapas adicionais.

3. **Notificações Push:** Ao ser aprovada a indicação, o Indicador receberá uma notificação push parabenizando-o pela indicação bem-sucedida. O Indicado também receberá uma notificação push contendo as informações do Indicador e informando que um consultor entrará em contato.

4. **Desconto para o Indicado:** O Indicado receberá um desconto no seguro contratado, conforme a política de descontos definida pela empresa.  O valor do desconto deve ser claramente exibido ao Indicado antes da contratação.

5. **Gamificação:**  O aplicativo poderá incluir um sistema de gamificação para recompensar os Indicadores por suas indicações bem sucedidas.  A mecânica da gamificação deverá ser definida separadamente.

6. **Gerenciamento de Indicações:** Tanto o Indicador quanto o Indicado poderão visualizar o histórico de suas indicações, o status de cada indicação (pendente, aprovada, rejeitada) e os descontos obtidos.

7. **Cadastro de Usuários:**  Para usar o aplicativo, usuários (Indicadores e Indicados) precisam se cadastrar, fornecendo informações necessárias (nome, e-mail, telefone, etc.).


## Restrições

1. **Integração com APIs de Seguros:** A integração com APIs externas de seguradoras dependerá de disponibilidade e contratos.  

2. **Plataformas:** O escopo inicial deve focar em aplicativo mobile (Android e iOS).  A versão web pode ser considerada em etapas posteriores.

3. **Limites de Indicações:** Poderá haver um limite no número de indicações permitidas por usuário em um determinado período.

4. **Validação de Dados:**  O aplicativo deve realizar validação de dados em todas as entradas de usuários, garantindo a integridade dos dados.


## Exceções

1. **Indicação Rejeitada:** Se uma indicação for rejeitada, ambos os usuários serão notificados com o motivo da rejeição.

2. **Falha na Notificação Push:** Em caso de falha no envio da notificação push, um mecanismo de fallback deve ser implementado (ex: envio de e-mail).

3. **Erro na Aplicação:**  Mecanismos de tratamento de erros e logs devem ser implementados para facilitar a manutenção e solução de problemas.


## Decisões

1. **Tecnologia:**  As tecnologias de desenvolvimento (linguagens de programação, frameworks, banco de dados) serão definidas em etapa posterior, após análise de viabilidade e recursos.

2. **Sistema de Gamificação:** A implementação do sistema de gamificação será avaliada em fases posteriores do projeto, dependendo da priorização e recursos disponíveis.

3. **Integração com APIs:** A prioridade será dada a uma solução que seja independente de APIs externas de seguradoras inicialmente, com a integração como melhoria futura.
