```markdown
# 06_autenticacao_backend.md

### Fluxo de Autenticação

1. **Registro:** O usuário fornece um endereço de e-mail, senha e outros dados relevantes. A senha é criptografada usando um algoritmo seguro (como bcrypt) antes de ser armazenada no banco de dados. Um token de verificação de e-mail é enviado para o usuário para confirmar seu endereço.

2. **Login:** O usuário insere seu endereço de e-mail e senha. O sistema verifica se o endereço de e-mail existe e se a senha fornecida corresponde à senha criptografada armazenada.  Se a autenticação for bem-sucedida, um JWT (JSON Web Token) é gerado e retornado ao cliente.

3. **Recuperação de Senha:** O usuário fornece seu endereço de e-mail. O sistema verifica se o endereço de e-mail existe e envia um link para redefinição de senha para o endereço de e-mail registrado. Este link contém um token único que expira após um determinado período. O usuário pode usar esse token para definir uma nova senha.

4. **Autenticação JWT:**  Após o login bem-sucedido, o cliente enviará o JWT em cada solicitação subsequente, permitindo que o backend valide a identidade do usuário e autorize as ações. O JWT deve ser validado em cada solicitação para evitar acessos não autorizados.

5. **Logout:** O usuário solicita logout. O token JWT é invalidado no servidor.


### Tecnologias/Bibliotecas

* **JWT (JSON Web Tokens):** Para gerenciamento de sessões e autenticação sem estado.
* **bcrypt:** Para criptografia de senhas.
* **Node.js (ou similar):** Como backend para o servidor de autenticação. Express.js como framework.
* **Passport.js (ou similar):**  Para simplificar a implementação de estratégias de autenticação diferentes (local, social etc.).
* **Banco de dados relacional (PostgreSQL, MySQL ou similar):** para armazenar informações do usuário de forma segura.


### Considerações de Segurança

* **Hashing de senhas:** Utilizar um algoritmo de hashing seguro e de custo computacional elevado (bcrypt recomendado) para proteger as senhas armazenadas. Nunca armazenar senhas em texto simples.
* **Validação de entrada:** Validar todas as entradas do usuário para evitar injeções de SQL e outras vulnerabilidades.
* **Proteção contra CSRF (Cross-Site Request Forgery):** Implementar tokens CSRF para proteger contra ataques CSRF.  Utilizar tokens únicos para cada solicitação e verificá-los no servidor.
* **Limitação de tentativas de login:** Implementar um mecanismo para bloquear temporariamente contas após um número excessivo de tentativas de login inválidas.
* **HTTPS:** Garantir que todas as comunicações entre o cliente e o servidor sejam criptografadas usando HTTPS.
* **Gestão de tokens:** Implementar mecanismos para revogação e invalidação de tokens JWT, caso seja necessário.
* **Auditoria:** Registrar todas as tentativas de login, incluindo sucesso ou falha, para fins de auditoria e detecção de intrusões.
* **Segurança de armazenamento:** Utilizar práticas seguras de armazenamento de dados sensíveis, incluindo criptografia e controle de acesso.
* **Atualizações regulares:** Manter o software e as bibliotecas atualizadas para corrigir vulnerabilidades conhecidas.

```

<br>
<hr>
<br>

### 🧠 Instruções para o Agente de Desenvolvimento

**📝 Prompt Complementar:**
Este documento detalha o design do sistema de autenticação para nosso MicroSaaS, focando em segurança e usabilidade.  A próxima fase de desenvolvimento envolve validar este design através de testes com usuários reais do nosso público-alvo.  O feedback obtido será crucial para refinar a experiência de usuário e garantir que o sistema atenda às necessidades específicas do nosso nicho de mercado, antes de investir em uma implementação completa e em testes automatizados complexos.

**👍 Instruções Positivas:**
Teste manual com 5 a 10 usuários reais do seu nicho de mercado, representando diferentes perfis e níveis de familiaridade com tecnologia.  Concentre-se em avaliar a usabilidade do fluxo de registro, login, recuperação de senha e logout.  Colete feedback qualitativo através de entrevistas e observação direta, documentando detalhadamente as dificuldades encontradas pelos usuários e suas sugestões de melhoria.  Itere no design do sistema com base neste feedback, priorizando a simplificação do fluxo de autenticação e a melhoria da clareza das mensagens de erro.  Monitore as métricas de sucesso (taxa de conversão de registro, taxa de login bem-sucedido, etc.) e ajuste o sistema para otimizar a experiência do usuário.  Após a primeira rodada de testes, repita o processo com um novo grupo de usuários para validar as mudanças implementadas.  Documente todos os testes, feedback e iterações realizadas.  Priorize a qualidade da experiência do usuário acima da complexidade técnica.


**👎 Instruções Negativas:**
Não implemente testes automatizados extensivos para este módulo de autenticação até que o feedback dos testes com usuários reais tenha sido analisado e as iterações necessárias tenham sido concluídas. Evite a implementação de recursos complexos de autenticação (como autenticação multi-fator ou autenticação social) sem antes validar a necessidade e a usabilidade dos recursos básicos do sistema. Não se concentre em otimizações de performance antes de garantir a funcionalidade básica e a experiência do usuário.  Não assuma que você entende perfeitamente as necessidades do usuário; confie no feedback dos testes com usuários reais. Não negligencie a documentação das etapas de teste e feedback coletados.  Evitar a utilização de frameworks ou bibliotecas complexas desnecessárias que possam comprometer a segurança ou aumentar a complexidade desnecessariamente neste estágio.
