# Avaliar cupom

Status: Versão final
Última edição: 29 de setembro de 2025 14:38
CDU: 12
Responsável: Clara Teodósio de Morais

## Histórico de Revisões

| Data | Versão | Descrição | Autor |
| :--: | :----: | :-------: | :---: |
| 29/09 | 1.0 | Versão final | Clara Teodósio |

## 1. Resumo

O assinante pode fazer uma avaliação do cupom o qual ele resgatou, atribuindo uma nota (de 1 a 5 estrelas) e podendo fazer um comentário.

## 2. Atores

- Principal: Assinante

## 3. Pré-condições

- Usuário devidamente cadastrado
- Oferta devidamente cadastrada
- Cupom devidamente resgatado pelo usuário

## 4. Pós-condições

- Avaliação devidamente registrada

## 5. Fluxos de Eventos

### 5.1 Fluxo Principal

| Ator | Sistema |
| :--: | :-----: |
| 0. Assinante clica em avaliar cupom (botão presente na página de histórico) | - |
| - | 1. O sistema exibe o modal de avaliação  |
| 2. O assinante preenche os campos atribuindo uma nota e comentário e clica em confirmar | - |
| - | 3. O sistema persiste as informações e fecha o modal |

### 5.2 Fluxos de Exceção

#### 5.2.1 Campo não preenchido

| Ator | Sistema |
| :--: | :-----: |
| - | 3.1 O usuário não selecionou uma estrela (nota) e o sistema pede para preencher o campo |
|  | (retorna ao passo 2) |

### 5.3 Fluxos Alternativos

#### 5.3.1 Avaliação cancelada

| Ator | Sistema |
| :--: | :-----: |
| 2.1 O assinante clica em “Cancelar” | - |
|  | (retorna a página de histórico) |