# Projeto FastAPI

Este projeto tem como objetivo criar uma API simples utilizando o FastAPI e
entender um pouco melhor sobre o ecossistema de Python.

## Tecnologias

- Python
- FastAPI
- Uvicorn
- Docker
- Docker Compose

## Baixe o arquivo Yolov3 Weights

Para executar o código será necessário este arquivo, após clonar o repositório execute este comando na raiz do projeto.

```shell
wget https://pjreddie.com/media/files/yolov3.weights
```

## Como rodar o projeto.

1 - Clone este projeto

```shell
git@github.com:NicolasPereira/fastapi-object-recognition.git
```

2 - Execute o build do Docker

```shell
docker-compose build
```

3 - Suba o serviço

```shell
docker-compose up -d
```

4 - Acesse o serviço

```shell
http://localhost:8000/
```

5 - A documentação se encontra em

```shell
http://localhost:8000/docs
```

Made with 💜 by [@devnic\_](https://twitter.com/devnic_)
