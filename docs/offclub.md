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
- Semelhanças: Oferece descontos por meio de assinatura, em parceria com diversos estabelecimentos.
- Diferencial: As ofertas são destinadas a turistas, tendo seus planos baseados em viagens.

### [<u>2. Clube Certo</u>](https://primegourmetclub.com.br/)
- Semelhanças: Tem como objetivo oferecer vantagem à base de clientes das empresas.
- Diferencial: Empresas são seus principais clientes, tendo a plataforma contratada por elas para depois repassar aos clientes finais.


## 7. Visão geral do produto
Clube do Sol será um sistema digital de adesão a descontos, focado em estabelecer uma rede de benefícios entre consumidores e empresas locais. A interface será simples e acessível, permitindo fácil navegação para todos os perfis de usuários. Para os consumidores, a plataforma oferecerá acesso a serviços e produtos com preços reduzidos. Para as empresas, será uma ferramenta de marketing e aumento de vendas em períodos de baixa demanda, além de um meio para evitar desperdício de produtos.

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
