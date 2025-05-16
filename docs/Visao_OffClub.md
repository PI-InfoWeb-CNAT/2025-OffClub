# Documento de Visão

## Serviço - Clube de Descontos

### Histórico da Revisão 
| Data | Versão | Descrição | 
|:----|:------|:----------|
| 05/05/2025 | **1.1** | Versão Inicial |

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
- Semelhanças: Oferece descontos por meio de assinatura, em parceria com diversos estabelecimentos de segmentos variados, como o OffClub.
- Diferencial: As ofertas são destinadas a turistas, tendo seus planos baseados em viagens. Além disso, é uma plataforma de âmbito nacional, que atende a empresas de diversos estados de diferentes regiões do nosso país, enquanto que o OffClub visa alcançar o comércio potiguar, principalmente na Região Metropolitana de Natal. O Prime Gourmet oferece uma assinatura anual, porém o OffClub funciona à base de uma assinatura tanto anual quanto mensal.

### [<u>2. Clube Certo</u>](https://clubecerto.com.br/)
- Semelhanças: Tem como objetivo oferecer vantagem à base de clientes das empresas, sendo essas de variados segmentos, assim como nossa plataforma.
- Diferencial: Empresas são seus principais clientes, tendo a plataforma contratada por elas para depois repassar aos clientes finais. Já a nossa empresa busca obter receita por meio das assinaturas dos usuários clientes de tais empresas. Alcança todo o Brasil, que nem o Prime Gourmet. Entretanto, nosso site será realizado com o intuito de atingir o comércio local.

### [<u>3. Food To Save</u>](https://foodtosave.com.br/)
- Semelhanças: É um software no qual empresas gastronômicas se cadastram para anunciar grandes descontos aos seus clientes, cativando e atraindo-os, o que evita o decaimento brusco das vendas pelo seu aumento.
- Diferencial: A Food To Save é uma empresa que engloba apenas alimentos como produtos comercializados. Também se diferencia porque procura não apenas o lucro das suas vendas, mas tem como visão macro o desenvolvimento sustentável, já que coloca em promoção alimentos que estão próximos ao vencimento, evitando o desperdício, e como consequência, há menos emissão de dióxido de carbono por meio das vendas de suas "Sacolas Surpresa", nas quais há alimentos provenientes de suas empresas parceiras. É majoritariamente presente na região Sudeste e Sul do Brasil, ao passo que o OffClub se faz presente apenas no Rio Grande do Norte. Além disso, não funciona por assinatura, as compras realizadas nele são realizadas de forma avulsa.

### [<u>4. Méliuz</u>](https://www.meliuz.com.br/)
- Semelhanças: É uma empresa que fornece cupons/vouchers de descontos para serem utilizados em diversas lojas de variados segmentos. Sua versão Méliuz Prime funciona com assinatura mensal, assim como o OffClub.
- Diferencial: A Méliuz é uma empresa de alcance nacional. Também se destaca porque há dois modos de utilização da plataforma: o Méliuz regular e o Méliuz Prime. No Méliuz regular, os usuários conseguem acessar os cupons de desconto de forma gratuita. Já no Méliuz Prime, os usuários pagam pela assinatura mensal. No OffClub, os clientes terão que obrigatoriamente assinar algum plano para ter acesso às promoções propostas.

## 7. Visão geral do produto
OffClub será um sistema digital de adesão a descontos, focado em estabelecer uma rede de benefícios entre consumidores e empresas locais para fortalecer a economia regional. Esse fornecimento de descontos ocorrerá por meio da assinatura de algum plano pelos nossos clientes que, por sua vez, terão as ofertas do nosso sistema desbloqueadas de acordo com o tipo de assinatura escolhida por eles. A interface será simples e acessível, permitindo fácil e intuitiva navegação para todos os perfis de usuários. Para os consumidores, a plataforma oferecerá acesso a serviços e produtos com preços reduzidos ou promoções do tipo "Pague um e leve dois" propostas por empresas parceiras, e ao acessar uma oferta, os assinantes poderão ver as informações gerais dela, tendo a possibilidade de emitir um cupom para utilizar no empreendimento fornecedor dessa campanha promocional. Para as empresas, será uma ferramenta de marketing e aumento de vendas em períodos de baixa demanda, sendo essencial para manter o fluxo financeiro ativo e consistente, além de um meio para evitar desperdício de produtos.

## 8. Requisitos Funcionais

### 8.1. Gestão de Usuários e Autenticação

| Código | Nome                         | Descrição                                                                                         |
|--------|------------------------------|---------------------------------------------------------------------------------------------------|
| RF001  | Cadastro de Assinante        | Permite que visitantes criem uma conta com nome completo, e-mail, CPF, senha e telefone, com verificação por e-mail ou através de login social (Google). |
| RF002  | Login/Logout                 | Disponibiliza autenticação segura para todos os perfis, com expiração de sessão e bloqueio após múltiplas tentativas falhas. |
| RF003  | Recuperação de Senha         | Possibilita redefinir a senha via e-mail, utilizando token temporário com validade limitada. |
| RF004  | Cadastro de Empresa          | Executa o registro de empresas mediante CNPJ válido, envio de documentos e submissão à aprovação administrativa. |
| RF005  | Edição de Perfil             | Permite a atualização de dados pessoais, exigindo reautenticação para alterações sensíveis. |

### 8.2. Gestão de Ofertas e Cupons

| Código | Nome                         | Descrição                                                                                         |
|--------|------------------------------|---------------------------------------------------------------------------------------------------|
| RF006  | Criação de Ofertas           | Permite que empresas publiquem promoções com nome, descrição, imagens, categoria, desconto, validade e número máximo de cupons disponibilizados. |
| RF007  | Edição de Ofertas            | Autoriza alterações em ofertas ainda não resgatadas, mantendo controle de versões. |
| RF008  | Geração de Cupons            | Gera códigos únicos no momento da reserva, com validade, rastreável e que permitirá o resgate da oferta. |
| RF009  | Filtros de Busca             | Disponibiliza mecanismos de filtragem por localização, categoria, preço, avaliação e ordenação. |
| RF010  | Ofertas Personalizadas       | Exibe recomendações com base no perfil de consumo, tipo de assinatura e histórico de resgates. |

### 8.3. Assinaturas e Pagamentos

| Código | Nome                         | Descrição                                                                                         |
|--------|------------------------------|---------------------------------------------------------------------------------------------------|
| RF011  | Planos de Assinatura         | Apresenta diferentes opções de planos com variação nos percentuais de desconto e limites mensais. |
| RF012  | Gerenciamento de Pagamentos  | Permite cadastrar, atualizar e remover formas de pagamento, com suporte a cartão e Pix. |
| RF013  | Cancelamento de Assinatura   | Oferece cancelamento autônomo com proposta de retenção e manutenção dos benefícios até o fim do ciclo. |

### 8.4. Módulo Administrativo

| Código | Nome                         | Descrição                                                                                         |
|--------|------------------------------|---------------------------------------------------------------------------------------------------|
| RF014  | Validação de Empresas        | Permite que administradores aprovem ou rejeitem cadastros mediante análise documental. |
| RF015  | Moderação de Conteúdo        | Fornece ferramentas para edição, remoção e auditoria de conteúdos inadequados ou denunciados. |
| RF016  | Painel de Acompanhamento     | Apresenta visualmente informações essenciais como número de usuários cadastrados, quantidade de ofertas ativas, cupons gerados e empresas parceiras aprovadas. |

### 8.5. Engajamento e Relacionamento

| Código | Nome                         | Descrição                                                                                         |
|--------|------------------------------|---------------------------------------------------------------------------------------------------|
| RF017  | Sistema de Avaliações        | Permite que assinantes atribuam notas de 1 a 5 estrelas e escrevam comentários sobre empresas, com moderação posterior. |
| RF018  | Notificações Inteligentes    | Envia alertas sobre ofertas personalizadas, cupons próximos do vencimento e novidades, com preferências configuráveis. |
| RF019  | Histórico de Consumo         | Exibe todas as ofertas resgatadas, status de uso, empresas favoritas e permite filtragens avançadas. |

### 8.6. Funcionalidades Adicionais

| Código | Nome                         | Descrição                                                                                         |
|--------|------------------------------|---------------------------------------------------------------------------------------------------|
| RF020  | Integração com Mapa          | Apresenta localização geográfica das empresas parceiras com visualização em mapa interativo e rotas. |
| RF021  | Programa de Indicação        | Permite envio de convites por link ou código exclusivo, com concessão de benefícios após conversão do indicado. |
| RF022  | Limites e Alertas de Uso     | Informa o assinante sobre a proximidade ou atingimento do limite de cupons mensais conforme o plano vigente. |
| RF023  | Favoritos e Lista de Desejos | Permite que assinantes salvem ofertas de interesse para acesso rápido posterior, mesmo antes do resgate. |
| RF024  | Estatísticas para empresas | Oferece visualização simples de desempenho: número de cupons gerados, resgatados, média de avaliação e favoritos. |
| RF025  | Chat com empresa | Habilita um canal de mensagem entre assinante e empresa a respeito do resgate ou uso da oferta. |
| RF026  | Agendamento de ofertas | Permite que o assinante, ao resgatar uma oferta de serviço (ex: salão, clínica, oficina), selecione data e horário conforme disponibilidade da empresa. |

## 9. Requisitos não-funcionais
| Código | Nome | Descrição | Categoria | Classificação |
|:---|:---|:---|:---|:---|
| NF01 | Responsividade | A plataforma deverá adaptar-se automaticamente a diferentes tamanhos de tela e dispositivos. | Usabilidade | Obrigatório |
| NF02 | Segurança de dados | Implementar protocolos de segurança para proteger informações pessoais e comerciais. | Segurança | Obrigatório |
| NF03 | Compatibilidade | A plataforma deverá ser compatível com os navegadores modernos mais utilizados. | Usabilidade | Obrigatório |
| NF04   | Acessibilidade | O sistema deve garantir acessibilidade a pessoas com deficiência visual ou motora, seguindo diretrizes reconhecidas como WCAG 2.1.     |        Usabilidade           | Obrigatório    |
