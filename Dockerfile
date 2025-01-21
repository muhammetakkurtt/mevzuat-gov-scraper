# Use Python 3.11.11 as the base image
FROM python:3.11.11-bullseye

# Set environment variables for Poetry
ENV POETRY_VERSION=1.7.0 \
    POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

# Add Poetry to the PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies, Chromium, and ChromiumDriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    zlib1g-dev \
    tcl-dev \
    tk-dev \
    wget \
    unzip \
    chromium \
    chromium-driver \
    gnupg \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Chromium environment variables
ENV CHROME_BIN=/usr/bin/chromium \
    CHROME_DRIVER=/usr/bin/chromedriver

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true

# Set the working directory inside the container
WORKDIR /app

# Copy project dependency files
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Set the default command to run your application
CMD ["poetry", "run", "python", "main.py"]