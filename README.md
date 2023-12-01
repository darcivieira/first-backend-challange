# Backend API Challange

## [EN] Overview | [PT] Visão geral

#### [EN]

That was a challange published by a great brazilian's financial company for your candidates for a backend opportunity.
I know that I'm not participating in that job interview, but I saw an opportunity to show a little bit how I work.
So, I hope you can take a look at my experience level with python.

#### [PT]

Este foi um desafio publicado por uma grande empresa financeira brasileira à seus candidatos a uma oportunidade de
backend. Sei que não estou participando desta entrevista, mas vi uma oportunidade de mostrar um pouco como eu trabalho.
Então, espero que vocês possam dar uma olhada em meu nível de experiencia em python.




## [EN] The challange | [PT] O Desafio

#### [EN]

We've 2 types of users, the commons and the shopkeeper, both of them have a wallet with money and make transaction to 
each other. We should to focus only on the transaction flow.

Requirements:

* Both types of users have a complete name, CPF or CNPJ, e-mail and password. The CPF/CNPJ and e-mail should be a unique
value.
* Common users can send money to both type of users.
* Shopkeeper only can receive money.
* You must check if user has a positive balance before the transaction.
* You must check if the transaction was allow with the external service. Use this mock to simulate that 
(https://run.mocky.io/v3/5794d450-d2e2-4412-8131-73d0293ac1cc).
* The transaction should be like in real world and the money must return to the wallet in case of failure.
* You must report the receiver, by e-mail and phone message, when the transaction succeeded. Use this mock to simulate 
that (https://run.mocky.io/v3/54dc2cf1-3add-45b5-b5a9-6bf7e7f1f4a6).
* This must be a RESTFul.

#### [PT]

Temos 2 tipos de usuários, os comuns e lojistas, ambos têm carteira com dinheiro e realizam transferências entre eles. Vamos nos atentar somente ao fluxo de transferência entre dois usuários.

Requisitos:

* Para ambos tipos de usuário, precisamos do Nome Completo, CPF, e-mail e Senha. CPF/CNPJ e e-mails devem ser únicos no sistema. Sendo assim, seu sistema deve permitir apenas um cadastro com o mesmo CPF ou endereço de e-mail.

* Usuários podem enviar dinheiro (efetuar transferência) para lojistas e entre usuários.

* Lojistas só recebem transferências, não enviam dinheiro para ninguém.

* Validar se o usuário tem saldo antes da transferência.

* Antes de finalizar a transferência, deve-se consultar um serviço autorizador externo, use este mock para simular (https://run.mocky.io/v3/5794d450-d2e2-4412-8131-73d0293ac1cc).

* A operação de transferência deve ser uma transação (ou seja, revertida em qualquer caso de inconsistência) e o dinheiro deve voltar para a carteira do usuário que envia.

* No recebimento de pagamento, o usuário ou lojista precisa receber notificação (envio de email, sms) enviada por um serviço de terceiro e eventualmente este serviço pode estar indisponível/instável. Use este mock para simular o envio (https://run.mocky.io/v3/54dc2cf1-3add-45b5-b5a9-6bf7e7f1f4a6).

* Este serviço deve ser RESTFul.
