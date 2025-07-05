# Regras de Negócio

* Cada indicação válida gera 1% de desconto para o usuário que indicou.
* Uma contratação do indicado por um usuário gera mais 1% de desconto adicional para o usuário que indicou.
* O desconto máximo acumulativo é de 10% ao ano na apólice.
* Um usuário só pode receber o desconto referente a uma mesma indicação uma única vez.
* O administrador pode confirmar ou rejeitar uma indicação.
* Uma indicação só pode ser confirmada uma vez.
* Apenas administradores podem acessar o painel administrativo.


# Restrições

* O sistema deve ser capaz de lidar com um grande número de indicações simultaneamente.
* Os dados dos usuários devem ser protegidos.
* O aplicativo deve ser responsivo e funcionar em diferentes dispositivos.

# Exceções

* Indicações com dados inválidos serão rejeitadas.
* Se o sistema estiver indisponível, as indicações serão processadas assim que o sistema estiver online.

# Decisões

* Foi escolhido o React para o frontend devido a sua popularidade, facilidade de uso e grande comunidade.
* Foi escolhido o Node.js com Express para o backend devido à sua eficiência e facilidade de integração com o React.
* Foi escolhido o PostgreSQL por ser um banco de dados robusto e escalável.
* Foi escolhido o FCM para notificações push devido à sua integração com o Firebase e sua facilidade de uso.