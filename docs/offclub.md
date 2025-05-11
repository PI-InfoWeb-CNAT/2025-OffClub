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
| Visitante | Usuário sem cadastro; O usuário pode acessar a plataforma apenas para visualizar as informações sobre seu funcionamento. | Visualizar a descrição do serviço, acessar informações básicas sobre a plataforma, registrar-se ou entrar em conta existente. |
| Assinante | Usuário cadastrado e com assinatura ativa;  O usuário, após realizar seu cadastro no site e a assinatura, poderá aproveitar os descontos oferecidos. | Após a realização da inclusão de dados cadastrais tais como login, senha e endereço e a realização do pagamento da assinatura, o usuário passa a ser visto como assinante poderá consultar as ofertas e reservar os serviços e os produtos com desconto. O cliente deve ter acesso às seguintes funcionalidades no site: Alterar seus dados cadastrais; Visualizar seu histórico de reservas; Cancelar reserva; Avaliar os produtos adquiridos; Gerenciar assinatura. |
| Empresa | Gestor de empresa parceira comercial, com CNPJ registrado; Usuário responsável por publicar e gerenciar as ofertas de seus produtos e serviços. | Criar, editar e gerenciar ofertas e serviços; Acompanhar dados de vendas intermediadas pelo site (cupom) e reservas; Disponibilizar ou bloquear a apresentação de ofertas e serviços. |
| Administrador | Usuário responsável pela gestão da plataforma; será aquele que irá controlar o cadastro das empresas e dos clientes, bem como cuidar da manutenção do site. | Aprovar cadastros de empresas; supervisionar atividades na plataforma; gerenciar conteúdos; criar os "ramos das empresas" (categorias como: vestuário, alimentação, etc.) e as categorias para as ofertas (ex: alimentícia, esportivo, mercado, vestuário, etc.) e resolver inconsistências. |

## 4. Descrição do ambiente dos usuários
A plataforma será acessada através de ambiente web responsivo, disponível para computadores e dispositivos móveis, permitindo o uso em qualquer local com acesso à internet. Não haverá restrições quanto ao ambiente físico para Visitantes, Assinantes, Empresas ou Administradores, desde que a conexão esteja estável.

O usuário do tipo Visitante utilizará a plataforma para consultar informações básicas sobre o funcionamento do serviço, conhecer as ofertas disponíveis e, se desejar, realizar o cadastro para se tornar um assinante ou solicitar o cadastro da sua empresa. 

O Assinante, já cadastrado e com assinatura ativa, navegará pela plataforma para buscar, visualizar e reservar serviços ou produtos com desconto, os quais serão desbloqueadas dependendo do tipo de plano do assinante, bem como gerenciar seu perfil e sua assinatura. Além disso, após a reserva da oferta, será gerado um cupom com um código específico, criado pelo próprio sistema, e com um período de validade definido pela empresa, e também poderá avalia-la colocando uma descrição e classficando com estrelas. Esse tipo de usuário receberá ofertas personalizadas de acordo com seu histórico de consumo. 

As Empresas, após terem seu cadastro confirmado pelo administrador, acessarão o sistema para criar, editar e gerenciar suas ofertas, além de acompanhar dados de vendas e reservas. No comento do cadastro das ofertas, a empresa irá definir para qual tipo de plano de assinate ela poderá ser exibida, além do seu nome, descrição, imagem, categoria, valor, data de início e fim (após essa data, mesmo não tendo atingido o número máximo de cupons, a oferta deixará de ser exibida), quantidade máxima de cupons gerados (após essa quantidade ser atingida, a oferta deixará de ser exibida) e tempo de duração do cupom.

O Administrador poderá acessar o sistema a partir de uma autenticação restrita, realizando a gestão de cadastros, supervisão de atividades, criação das categoras das ofertas e ramos das empresas, resolução de inconsistências e manutenção do conteúdo da plataforma.

## 5. Principais necessidades dos usuários
- **Visitante**: Entendimento claro sobre o funcionamento da plataforma e interface atrativa para estimular o cadastro.
- **Assinante**: Interface amigável que permita obter informações sobre as ofertas; facilidade na busca, visualização e aquisição de descontos; simplicidade no gerenciamento da assinatura.  
- **Empresa**: Ferramentas para cadastro e gestão eficiente de suas ofertas, para o auxílio no aumento das venda nos períodos de baixa demanda; análise de desempenho das campanhas promocionais.
- **Administrador**: Acesso a um painel de gestão robusto que permita a administração eficaz dos usuários, parceiros e ofertas.

## 6. Alternativas concorrentes
### [<u>1. Prime Gourmet Club</u>](https://primegourmetclub.com.br/)
- Semelhanças: Oferece descontos por meio de assinatura, em parceria com diversos estabelecimentos.
- Diferencial: As ofertas são destinadas a turistas, tendo seus planos baseados em viagens.

### [<u>2. Clube Certo</u>](https://primegourmetclub.com.br/)
- Semelhanças: Tem como objetivo oferecer vantagem à base de clientes das empresas.
- Diferencial: Empresas são seus principais clientes, tendo a plataforma contratada por elas para depois repassar aos clientes finais.


## 7. Visão geral do produto
Clube do Sol será um sistema digital de adesão a descontos, focado em estabelecer uma rede de benefícios entre consumidores e empresas locais. A interface será simples e acessível, permitindo fácil navegação para todos os perfis de usuários. Para os consumidores, a plataforma oferecerá acesso a serviços e produtos com preços reduzidos. Para as empresas, será uma ferramenta de marketing e aumento de vendas em períodos de baixa demanda, além de um meio para evitar desperdício de produtos.

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
