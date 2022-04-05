

## DISC - Biopark


### Setup de Ambiente DEV

> Requisitos: Python V3


#### Passo 1 - Criando virtual env (raiz do projeto clonado)
```bash
python3 -m venv .venv
```
Ativando o virtual env

```
.venv\Script\activate
```

#### Passo 2 - Instalando Requisitos

```
pip install -r requirements.txt
```


#### Passo 3 - Carregando Fixtures

```
python manage.py loaddata disc_website\fixtures\initial_data.json
```

#### Passo 4 - Criando superusuário

```
python manage.py createsuperuser
```


#### Passo 5 - Rodando Server

```
python manage.py runserver
```

Aponte seu navegador para [Link](http://localhost:8000/)