FROM ubuntu:22.04 AS base

ENV APP_ROOT="/company"

# Create a dedicated group and user (non-root)
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} appgroup && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash appuser

# Install OS dependencies required for building Python and running apps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    ca-certificates \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    liblzma-dev \
    make \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_ROOT}

# Install pyenv
ENV PYENV_ROOT="${APP_ROOT}/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
RUN git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT}

# Install and activate Python version
ARG PYTHON_VERSION=3.13.3
RUN pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir --upgrade pip build wheel setuptools virtualenv

COPY --chown=appuser:appgroup pyproject.toml ${APP_ROOT}/

FROM base AS builder

# Install Poetry
ENV POETRY_HOME="${APP_ROOT}/.poetry"
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache
ENV PATH="${POETRY_HOME}/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY --chown=appuser:appgroup poetry.lock ${APP_ROOT}/

RUN mount=type=ssh poetry install --no-root --only main -vvv

FROM base AS runtime

ENV VIRTUAL_ENV="${APP_ROOT}/.venv"
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY --from=builder --chown=appuser:appgroup ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=appuser:appgroup app/ ${APP_ROOT}/app/

USER appuser

CMD ["uvicorn", "app:api:app"]
