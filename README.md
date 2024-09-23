# Monitoramento de Preço do Bitcoin 

Este projeto realiza o monitoramento do preço do Bitcoin utilizando a API CoinGecko e envia um alerta por e-mail quando o preço cai abaixo de um limite definido pelo usuário. O monitoramento é feito em intervalos de 10 minutos, e as notificações são enviadas para o e-mail informado.

## Funcionalidades

- Consulta o preço atual do Bitcoin em reais (BRL) através da API CoinGecko.
- Envia um e-mail de alerta quando o preço do Bitcoin cai abaixo do limite definido pelo usuário.
- Interface do terminal colorida com o uso de `colorama`.
- Contador de tempo até a próxima consulta.
- Configuração de e-mail segura utilizando variáveis de ambiente.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter o Python instalado. Você pode verificar isso executando:

```bash
python --version


