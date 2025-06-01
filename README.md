# City Data Center
## Projeto de coleta e analise de dados das cidades do país
Aqui encontramos um projeto open source que visa coletar informações das cidades ao redor do país, armazena-las, e gerar prospecções.
O Objetivo é gerar uma trasnparencia a respeito dos problemas encontrados nas Cidades, possibilitando assim a tomada de decisões

### As tecnologias utilizadas nesse projeto são:
*   Python
*   Flask
*   MySQL
*   Docker
*   Docker compose

## Rodando o codigo usando Docker
Obviamente precisa ter o Docker e o Docker Compose instalados!

### Execute na primeira vez que rodar:
```bash
docker compose up --build
```

### Após a primeira vez, para subir tudo rode:
```bash
docker compose up
```

## Para rodar o projeto sem ser pelo Docker
### NECESSARIO TER O MYSQL E O MONGO INSTALADO (RECOMENDO TAMBEM A INSTALAÇÃO DO MONGO COMPASS)
*   Caso abra em uma IDE que nao crie um ambiente virtual (VS Code)
```bash
python -m venv venv
```
*   Ative o ambiente virtual (Windows):
```bash
./venv/scripts/activate
```   
*   Ative o ambiente virtual (Linux):
```bash
./venv/bin/activate
``` 
*   Instale os recursos listados no requirements.txt
```bash
pip install -r requirements.txt
```
*   Para rodar o projeto, antes deve iniciar o MySQL assim como o Mongo. No Windows basta abrir o Workbench e entrar em algum servidor. No Linux ou Max, abra o terminal e digite (esse processo tambem funciona no Windows, caso tenha configurado as variaveis de ambiente):
```bash
mysql -u seu_nome_de_usuario -p
``` 
Em seguida execute:
```bash
flask db init
```
Por fim:
```bash
flask db migrate -m "Init"
```
*   Após isso, rode o projeto
* IMPORTANTE: antes de Executar, crie uma conexao nova com os dados no dev_configuration.py, ou entao altere os dados para permitir a conexão local **ISSO É TEMPORARIO E TEM QUE SER TRATADO**
```bash
flask run
```