# Definindo uma variável de argumento para a versão do Python
ARG PYTHON_VERSION=3.10-slim-bullseye

# Cria uma imagem base do python com a versão especificada
FROM python:${PYTHON_VERSION} as python

# Cria um novo estagio de construção chamado 'python-build-stage'
FROM python as python-build-stage

# Define um argumento para o ambiente de produção 
ARG BUILD_ENVIRONMENT=requirements

# Atualizando o sistema  e instalando pacotes necessarios para a compilação
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    git \
    libpq-dev

# Copiando o arquivo de requisitos para o contexto do build
COPY ./requirements.txt .

# Gerando pacotes wheels para dependencias do projeto 
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Criando um novo estágio  de execução chamado 'python-run-stage'
FROM python as python-run-stage

# Configurando argumentos e variaveis de ambiente
ARG BUILD_ENVIRONMENT=requirements
ARG APP_HOME=/home/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWHITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# Definindo o diretorio de trabalho dentro do container
WORKDIR ${APP_HOME}

# Criando um grupo e um usuario especifico para a aplicação
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Instalando dependencias do sistema necessárias para a execução
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copiando os pacotes  wheels gerados no estagio de constução para o container
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Instalando as dependencias do projeto a partir dos pacotes wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# Instalando uma dependência adicional (drf_yasg)
RUN pip install drf_yasg


# Copiando o script de inicialização para o contêiner
COPY --chown=django:django ./compose/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Copiando o restante do codigo fonte para o diretorio de trabalho no container
COPY --chown=django:django . ${APP_HOME}

# Configurando as permissoes do diretorio de trabalho
RUN chown django:django ${APP_HOME}


# RUN mkdir django:django ${APP_HOME}/staticfiles
RUN mkdir -p ${APP_HOME}/static
RUN chown django:django ${APP_HOME}/static


# Definindo o diretório de trabalho final
WORKDIR ${APP_HOME}