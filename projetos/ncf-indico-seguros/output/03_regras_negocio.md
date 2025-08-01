# 03_regras_negocio.md

## Regras de Negócio

1. **Cadastro e Login:**  Usuários (Asegurados e Administradores) devem se cadastrar fornecendo informações completas e válidas.  O login será realizado via credenciais (usuário e senha) ou método de autenticação seguro (ex: login com Google/Facebook - a ser definido).  Senhas devem atender a critérios de complexidade (a ser definido).

2. **Criar Indicação:** Um Cliente Atual (Asegurado) pode indicar um Potencial Cliente (Indicado) fornecendo seu nome e contato (e-mail ou telefone).  Cada indicação deve ser única e rastreada pelo sistema.  Limites para o número de indicações por Asegurado podem ser implementados (a ser definido).

3. **Notificações Push:**  Notificações Push serão enviadas ao Cliente Atual (Asegurado) confirmando a criação da indicação e ao Potencial Cliente (Indicado) convidando-o a concluir o processo de adesão.  O tipo e a frequência das notificações devem ser configuráveis.

4. **Gerenciamento do Sistema (Administrador):**  Administradores têm acesso a um painel para monitorar o desempenho do programa de indicações, gerar relatórios (número de indicações, conversões, descontos aplicados etc.), gerenciar usuários e configurar parâmetros do sistema (ex: valores de desconto).

5. **Visualização de Informações da Apólice:** Clientes Atuais (Asegurados) podem visualizar informações sobre suas apólices de seguro diretamente no aplicativo.

6. **Visualização de Detalhes da Indicação (Indicado):**  Potenciais Clientes (Indicados) podem visualizar detalhes da indicação recebida, incluindo o nome do Asegurado que os indicou e as instruções para prosseguir com o processo de adesão.

7. **Aplicação de Desconto:**  Descontos serão aplicados ao Cliente Atual (Asegurado) e ao Potencial Cliente (Indicado) após a aprovação da adesão do Indicado e a confirmação do pagamento da apólice do Indicado.  Os valores dos descontos serão definidos e configurados pelos administradores.  Condições para aplicação de desconto (ex: tempo mínimo de segurado, tipo de apólice) devem ser definidas e configuradas.

8. **Integração com Sistema de Seguros:**  O aplicativo deve integrar-se com o sistema de seguros da NCF para acesso às informações da apólice e para a atualização do status das indicações.


## Restrições

1. Orçamento limitado de R$ 1.500,00 para desenvolvimento.
2. Cronograma de desenvolvimento de 1 mês.


## Exceções

1. **Indicação Inválida:** Se o Potencial Cliente (Indicado) já for um cliente da NCF, a indicação será rejeitada e o Cliente Atual (Asegurado) será notificado.
2. **Falha no envio de Notificação Push:**  O sistema deve registrar a tentativa de envio e notificar o administrador em caso de falha recorrente.
3. **Dados Incompletos:** O sistema deve validar os dados de cadastro e indicação, impedindo a criação de registros incompletos ou inválidos e notificando o usuário sobre as inconsistências.


## Decisões

1.  A plataforma escolhida para o desenvolvimento será nativa (iOS e Android) ou híbrida (a ser definido com base no orçamento e cronograma).
2.  O método de autenticação a ser utilizado será definido após análise de segurança e viabilidade.
3.  A complexidade da senha será definida posteriormente, considerando as melhores práticas de segurança.
4.  Os valores de desconto serão definidos em conjunto com a NCF.
5.  O detalhamento dos relatórios disponíveis para o administrador será definido em conjunto com a NCF.

