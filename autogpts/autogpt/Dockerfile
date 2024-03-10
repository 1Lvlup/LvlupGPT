# 'dev' or 'release' container build
ARG BUILD_TYPE=dev

# Use an official Python base image from the Docker Hub
FROM python:3.10-slim AS autogpt-base

# Install browsers and necessary utilities
RUN apt-get update && apt-get install -y \
    chromium-driver ca-certificates gcc curl jq wget git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_PATH="/venv" \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_NO_INTERACTION=1

# Install and configure Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN poetry config installer.max-workers 10

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Install dependencies for dev and release
RUN case "${BUILD_TYPE}" in
    dev)
        poetry install --no-cache --no-root
        ;;
    release)
        poetry install --no-cache --no-root --without dev
        ;;
    *)
        echo "Invalid build type: ${BUILD_TYPE}"
        exit 1
        ;;
esac
RUN rm -rf $(poetry env info --path)/src

# Copy files based on the build type
COPY --from=build-context ${BUILD_TYPE} ./

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "autogpt"]
CMD []

# Create a separate stage for building the final image
FROM autogpt-base AS build-context
ONBUILD COPY . ./
