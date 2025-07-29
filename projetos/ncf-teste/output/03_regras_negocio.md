# 03_regras_negocio.md

## Regras de Negócio

1. **Indicação:** Um usuário (Indicador) pode indicar um seguro para outro usuário (Indicado) através do aplicativo.  A indicação deve conter informações sobre o seguro e os dados do Indicador.

2. **Aprovação da Indicação:** A indicação somente será considerada válida após a aprovação do seguro pelo Indicado.  Essa aprovação será registrada no sistema.

3. **Notificação Push:** Após a aprovação do seguro, o Indicador receberá uma notificação push parabenizando-o pela indicação bem sucedida. O Indicado receberá uma notificação push contendo os dados do Indicador e informando que um consultor entrará em contato.

4. **Desconto:**  O Indicado receberá um desconto no seguro aprovado como recompensa pela indicação. O valor do desconto deve ser previamente definido e configurado pelo administrador do sistema.

5. **Gerenciamento de Indicações:**  Tanto o Indicador quanto o Indicado podem acessar e gerenciar suas indicações através do aplicativo, visualizando o status de cada indicação (pendente, aprovada, rejeitada) e os descontos obtidos.

6. **Cadastro de Usuários:**  O aplicativo deve permitir o cadastro e autenticação de usuários (Indicadores e Indicados).  Os dados dos usuários devem ser armazenados de forma segura e em conformidade com as leis de privacidade.

7. **Cadastro de Seguros:** O administrador do sistema deve poder cadastrar e gerenciar os tipos de seguros oferecidos, incluindo o valor do desconto para cada seguro.

8. **Sistema de Gamificação (opcional):**  Um sistema de gamificação pode ser implementado para incentivar a indicação de seguros, por exemplo, através de pontuações e recompensas adicionais.

9. **Painel Administrativo:**  Um painel administrativo deve permitir ao administrador gerenciar usuários, seguros, indicações, notificações e o sistema de gamificação (se implementado).


## Restrições

1. **Integração com APIs de Seguros:**  A integração com APIs de terceiros para obter informações sobre os seguros poderá ser necessária e afetará o cronograma e custo do projeto.

2. **Plataformas:**  A definição precisa das plataformas de destino (iOS, Android, Web) impactará o escopo do desenvolvimento e os recursos necessários.

3. **Segurança de Dados:**  A segurança dos dados dos usuários é uma restrição crítica e deve ser atendida com rigor, seguindo as melhores práticas de segurança.


## Exceções

1. **Indicação Rejeitada:**  Se o Indicado rejeitar o seguro, a indicação será marcada como rejeitada e nenhuma notificação de sucesso será enviada ao Indicador.  Nenhum desconto será aplicado.

2. **Falha na Notificação Push:**  Em caso de falha na entrega da notificação push, um mecanismo de reenvio ou registro de erro deve ser implementado.

3. **Usuário Inexistente:**  Tentativas de indicar um usuário inexistente devem ser tratadas com uma mensagem de erro adequada.


## Decisões

1. **Plataforma:**  A decisão sobre as plataformas de desenvolvimento (iOS, Android, Web) será tomada após análise mais aprofundada das necessidades do cliente e recursos disponíveis.

2. **Sistema de Gamificação:** A implementação do sistema de gamificação será avaliada posteriormente, dependendo dos recursos e do orçamento disponíveis.

3. **Integração com APIs externas:**  A necessidade de integração com APIs externas será definida em fase de Discovery, após análise detalhada dos requisitos.
