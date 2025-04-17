# City Data Center
## Projeto de coleta e analise de dados das cidades do país
    Aqui encontramos um projeto open source que visa coletar informações das cidades ao redor do país, armazena-las, e gerar prospecções.
*   O Objetivo é gerar uma trasnparencia mais clara a respeito dos problemas encontrados nas Cidades, possibilitando assim a tomada de decisões a fim de resolver
*   O projeto consiste na reorganização de uma ideia original do TCC.
*   Inicialmente tem-se como objetivo coletar os dados a partir do fornecimento voluntario de informações publicas a respeito das cidades.

### As tecnologias utilizadas nesse projeto são:
*   Python
*   Flask
*   MySQL
*   Docker
*   Docker compose

Os dados são coletados de um google forms, tratados e enviados para o banco de dados.

## Para rodar o codigo na primeira vez:
```bash
docker compose up --build
```

## Caso ja tenha feito o build
```bash
docker compose up
```