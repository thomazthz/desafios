# Desafios IDwall

Soluções para os desafios da IDwall.

Os desafios estão descritos nos seguintes documentos: [strings](idwall_tools/strings) e [crawlers](idwall_tools/crawlers)


## Como instalar/configurar

### Com Docker

Navegar até o diretório raiz do projeto, onde está localizado o Dockerfile, e executar o **build**

`$ docker build -t idwall_challenges .`


Executando os comandos do CLI com Docker (os comandos estão descritos na seção [Comandos](#comandos-cli)):

`$ docker run -it --rm --name idwall_challenges -v "$PWD":/usr/src/idwall -w /usr/src/idwall idwall_challenges idwall-tools <NOME_COMANDO> <ARGS>`


### Manual (sem Docker)

**Obs: utilizar Python 3.6 ou 3.7**

Criar e ativar um *virtualenv*

Instalar as dependências

`pip install -r requirements.txt`

Instalar o pacote em modo *editable* para facilitar o uso do CLI com script `idwall-tools`

`pip install -e .`

Executar comandos

`idwall-tools <NOME_COMANDO> <ARGS>`


### Comandos (CLI)

- [`textwrap`](#textwrap)
- [`scrape-reddit`](#scrape-reddit)
- [`wake-up-bot`](#wake-up-bot)

#### `textwrap`

```
Usage: idwall-tools textwrap [OPTIONS] TEXT

Options:
  -f, --force
  -j, --justified
  -c, --columns INTEGER
  --help                 Show this message and exit.
```

Exemplos:

`$ idwall-tools textwrap "In the beginning God created the heavens and the earth. Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters."`


```
In the beginning God created the heavens
and the earth. Now the earth was
formless and empty, darkness was over
the surface of the deep, and the Spirit
of God was hovering over the waters.
```


Quebrar o texto em `n=40` colunas (justificado):

`$ idwall-tools textwrap -j "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur dictum molestie elit."`

```
Lorem ipsum  dolor sit amet, consectetur
adipiscing   elit.    Curabitur   dictum
molestie                           elit.
```


Forçar a quebra de "textos" grandes

`$ idwall-tools textwrap -f "Exemplo com um 'texto' muito grande (https://www.urlgigante.que.possui.mais/que_40_colunas/) no meio da frase."`

```
Exemplo com um 'texto' muito grande
(https://www.urlgigante.que.possui.mais/
que_40_colunas/)
no meio da frase.
```


#### `scrape-reddit`

Lista as threads que estão bombando (>5k upvotes) nos Subreddits.

```
Usage: idwall-tools scrape-reddit [OPTIONS] SUBREDDITS

Options:
  --help  Show this message and exit.
```

Exemplos:

Apenas um subreddit:

`$ idwall-tools scrape-reddit cats`


Múltiplos subreddits:

`$ idwall-tools scrape-reddit "cats;dogs;brasil"`


#### `wake-up-bot`

**Obs: esse comando necessita que o token do bot esteja definido na variável de ambiente `TELEGRAM_BOT_TOKEN`**

Inicia o bot do Telegram que lista as threads do comando [`scrape-reddit`](#scrape-reddit) com o comando `/NadaPraFazer nome_subreddit1;nome_subreddit_2`


`$ idwall-tools wake-up-bot`


### Mais exemplos

Iniciando o bot pelo Docker

`$ docker run -it --rm --name idwall_challenges -v "$PWD":/usr/src/idwall -w /usr/src/idwall -e TELEGRAM_BOT_TOKEN=<TOKEN> idwall_challenges idwall-tools wake-up-bot`



### Testes

Na raiz do projeto, exportar o variável `PYTHONPATH`

`$ export PYTHONPATH=.`

`$ pytest`
