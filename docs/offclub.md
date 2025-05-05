# Documento de Visão

## Serviço - Clube de Descontos

### Histórico da Revisão 
| Data | Versão | Descrição | 
|:----|:------|:----------|
| 28/04/2025 | **1.0** | Versão Inicial |

## 1. Objetivo do Projeto 
O projeto visa desenvolver uma plataforma que, por meio de descontos, fornece aos usuários oportunidade de economia de tempo e dinheiro, e às empresas locais parceiras, permite evitar desperdício de produtos e aumentar a rotatividade de clientes em horários de baixa demanda.

## 2. Descrição do problema 
| | |
|:-|:-|
| **_O problema_** | Baixa demanda de serviços em determinados dias e/ou horários e descarte/desuso desnecessário de produtos próximos à validade. |
| **_Consequências_** | Desperdício de produtos e horários ociosos na agenda dos serviços. |
| **_Quem é impactado_** | Prestadores de serviço, comércios e clientes/consumidores. |
| **_Proposta de Solução_** | Ofertar descontos aos clientes nesses cenários, para que incentive o consumo e o agendamento de um horário. |
| | |

## 3. Descrição dos usuários
| Nome | Descrição | Ações |
|:-|:-|:-|
| Visitante | Usuário sem cadastro, que acessa a plataforma apenas para visualizar informações sobre seu funcionamento. | Visualizar a descrição do serviço, acessar informações básicas sobre a plataforma, registrar-se ou entrar em conta existente. |
| Assinante | Cliente com cadastro e assinatura ativa, que pode aproveitar os descontos oferecidos. | Consultar ofertas, reservar serviços e produtos com desconto, gerenciar assinatura. |
| Empresa | Parceiro comercial com CNPJ registrado, que publica ofertas de seus produtos e serviços. | Criar, editar e gerenciar ofertas; acompanhar dados de vendas e reservas. |
| Administrador | Responsável pela manutenção e gestão da plataforma, incluindo controle de usuários e parceiros. | Aprovar cadastros de empresas, supervisionar atividades na plataforma, gerenciar conteúdos e resolver inconsistências. |

## 4. Descrição do ambiente dos usuários
A plataforma será acessada através de ambiente web responsivo, disponível para computadores e dispositivos móveis, permitindo o uso em qualquer local com acesso à internet. Não haverá restrições quanto ao ambiente físico para Visitantes, Usuários, Empresas ou Administradores, desde que a conexão esteja estável.

O Visitante utilizará a plataforma para consultar informações básicas sobre o funcionamento do serviço, conhecer as ofertas disponíveis e, se desejar, realizar o cadastro para se tornar um Usuário. O Usuário, já cadastrado e com assinatura ativa, navegará pela plataforma para buscar, visualizar e reservar serviços ou produtos com desconto. As Empresas acessarão o sistema para cadastrar, editar e gerenciar suas ofertas, além de acompanhar dados de vendas e reservas. O Administrador poderá acessar o sistema a partir de uma autenticação restrita, realizando a gestão de cadastros, supervisão de atividades, resolução de inconsistências e manutenção do conteúdo da plataforma.

## 5. Principais necessidades dos usuários
- **Visitante**: Entendimento claro sobre o funcionamento da plataforma para estimular o cadastro.
- **Assinante**: Facilidade na busca, visualização e aquisição de descontos; simplicidade no gerenciamento da assinatura.
- **Empresa**: Ferramentas para cadastro e gestão eficiente de suas ofertas; análise de desempenho das campanhas promocionais.
- **Administrador**: Acesso a um painel de gestão robusto que permita a administração eficaz dos usuários, parceiros e ofertas.

## 6. Alternativas concorrentes
### [<u>1. Prime Gourmet Club</u>](https://primegourmetclub.com.br/)
- Semelhanças: Oferece descontos por meio de assinatura, em parceria com diversos estabelecimentos de segmentos variados, igual ao OffClub.
- Diferencial: As ofertas são destinadas a turistas, tendo seus planos baseados em viagens. Além disso, é uma plataforma de âmbito nacional, que atende a empresas de diversos estados de diferentes regiões do nosso país, enquanto que o OffClub visa alcançar o comércio potiguar, principalmente na Região Metropolitana de Natal. O Prime Gourmet oferece uma assinatura anual, porém o OffClub funciona à base de uma assinatura mensal.

### [<u>2. Clube Certo</u>](https://clubecerto.com.br/)
- Semelhanças: Tem como objetivo oferecer vantagem à base de clientes das empresas, sendo essas de variados segmentos, assim como nossa plataforma. O Clube Certo também é uma aplicação que trabalha com a assinatura mensal, tal qual o nosso software.
- Diferencial: Empresas são seus principais clientes, tendo a plataforma contratada por elas para depois repassar aos clientes finais. Já a nossa empresa busca obter receita por meio das assinaturas dos usuários clientes de tais empresas. Alcança todo o Brasil, que nem o Prime Gourmet. Entretanto, nosso site será realizado com o intuito de atingir o comércio local.


## 7. Visão geral do produto
OffClub será um sistema digital de adesão a descontos, focado em estabelecer uma rede de benefícios entre consumidores e empresas locais para fortalecer a economia regional. A interface será simples e acessível, permitindo fácil e intuitiva navegação para todos os perfis de usuários. Para os consumidores, a plataforma oferecerá acesso a serviços e produtos com preços reduzidos ou promoções do tipo "Pague um e leve dois". Para as empresas, será uma ferramenta de marketing e aumento de vendas em períodos de baixa demanda, sendo essencial para manter o fluxo financeiro ativo e consistente, além de um meio para evitar desperdício de produtos.

## 8. Requisitos funcionais
| Código | Nome | Descrição |
|:---|:---|:---|
| F01 | Cadastro e autenticação de usuários | Permitir o registro de visitantes como usuários assinantes e que suas credenciais fiquem salvas para acessar o sistema posteriormente, além de possibilitar a recuperação de dados. |
| F02 | Cadastro de empresas | Permitir que empresas realizem cadastro e tenha seus dados armazenados. |
| F03 | Publicação de ofertas | Empresas cadastradas poderão publicar ofertas a respeito de seus serviços e produtos, informando o desconto, data e horário. |
| F04 | Visualização de ofertas | Assinantes visualizarão as ofertas publicadas por meio de uma interface. |
| F05 | Assinatura do serviço | Gerenciar planos de assinatura dos usuários, incluindo pagamento e renovação e cancelamento de assinatura. |
| F06 | Aprovação de cadastros | Permitir que administradores validem o cadastro de novas empresas. |
| F07 | Painel do administrador | Disponibilizar funcionalidades administrativas para gestão do sistema. |  
| F08 | Notificações | Enviar alertas sobre novas ofertas, promoções relâmpago ou status de reservas através do E-mail ou outra forma de contato disponibilizada. |
| F08 | Avaliações e comentários | Permitir que assinantes avaliem e comentem sobre as ofertas e estabelecimentos. |

## 9. Requisitos não-funcionais
| Código | Nome | Descrição | Categoria | Classificação |
|:---|:---|:---|:---|:---|
| NF01 | Responsividade | A plataforma deverá adaptar-se automaticamente a diferentes tamanhos de tela e dispositivos. | Usabilidade | Obrigatório |
| NF02 | Segurança de dados | Implementar protocolos de segurança para proteger informações pessoais e comerciais. | Segurança | Obrigatório |
| NF03 | Compatibilidade | A plataforma deverá ser compatível com os navegadores modernos mais utilizados. | Usabilidade | Obrigatório |
| NF04   | Acessibilidade | O sistema deve garantir acessibilidade a pessoas com deficiência visual ou motora, seguindo diretrizes reconhecidas como WCAG 2.1.     |        Usabilidade           | Obrigatório    |
