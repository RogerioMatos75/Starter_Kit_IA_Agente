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


<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento detalha os requisitos para um sistema MicroSaaS de indicação de clientes, focado em gerar receita adicional para a NCF através de um programa de incentivos. A próxima fase de desenvolvimento deve priorizar a construção de um MVP (Minimum Viable Product) que valide o core do programa de indicações com um grupo reduzido de usuários, focando nas funcionalidades essenciais de cadastro, indicação, rastreamento e aplicação de descontos.  A arquitetura deve ser escalável, porém inicialmente simples, priorizando a estabilidade e a entrega rápida de valor.

**👍 Instruções Positivas:**
Mapeie o problema específico de baixa aquisição de novos clientes da NCF.  Valide a dor com um pequeno grupo de asegurados, focando em funcionalidades essenciais como o cadastro de indicações, o envio de notificações (push ou email - escolha a mais simples para o MVP), e a visualização do status das indicações tanto pelo asegurador quanto pelo indicado.  Priorize a integração com o sistema de apólices da NCF apenas se este passo for crucial para a validação do MVP.  Implemente testes unitários e de integração para garantir a qualidade do código. Foque na criação de um fluxo de indicação simples e intuitivo.  Desenvolva um painel administrativo básico para monitoramento das indicações e gerenciamento de descontos. A implementação de relatórios completos pode ser adiada para fases posteriores.

**👎 Instruções Negativas:**
Evite implementar funcionalidades complexas de relatórios, dashboards avançados ou integrações desnecessárias.  Não desenvolva o sistema para todas as personas simultaneamente.  Priorize a validação do programa de indicações com um público-alvo reduzido antes de expandir para novas funcionalidades.  Não implemente recursos de segurança avançados desnecessários para o MVP.  Não se preocupe com a otimização de performance em escala até que o MVP esteja validado e a escalabilidade se torne um gargalo.  Evite o desenvolvimento de funcionalidades que não contribuam diretamente para a validação do core do programa de indicações, como a visualização completa de apólices de seguro no MVP.


--- REFINAMENTO DO ARCHON AI ---

**Checklist de Requisitos MVP - Programa de Indicação NCF:**

* **Funcionalidades Essenciais:**
    * [ ] Cadastro de Asegurados (simplificado).
    * [ ] Fluxo de Indicação (simplificado).
    * [ ] Notificações (Push ou Email - escolher a mais simples).
    * [ ] Visualização de Status da Indicação (Asegurado e Indicado).
    * [ ] Aplicação de Descontos (simplificada).
    * [ ] Painel Administrativo Básico (monitoramento e gestão de descontos).
    * [ ] Testes Unitários e de Integração.

* **Integrações:**
    * [ ] Integração com Sistema de Apólices (somente se crucial para validação do MVP).

* **Requisitos Não Funcionais (MVP):**
    * [ ] Estabilidade do sistema.
    * [ ] Interface intuitiva (foco no fluxo principal).


* **Itens a serem adiados para futuras iterações:**
    * [ ] Cadastro de Administradores.
    * [ ] Relatórios completos.
    * [ ] Dashboards avançados.
    * [ ] Segurança avançada.
    * [ ] Escalabilidade completa.
    * [ ] Visualização completa de apólices.
    * [ ] Suporte a múltiplos dispositivos (foco em um inicialmente).

* **Validação:**
    * [ ] Teste com grupo reduzido de asegurados para validação do core do programa.
