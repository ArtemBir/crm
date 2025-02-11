# Use Debian as the base image
FROM debian:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv curl git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create virtual environment and install Poetry
RUN python3 -m venv $VIRTUAL_ENV \
    && $VIRTUAL_ENV/bin/pip install poetry \
    && ln -s $VIRTUAL_ENV/bin/poetry /usr/local/bin/poetry

# Set work directory inside the container
WORKDIR /app

# Copy everything into the container
COPY . .

# Tell Poetry to use the correct Python interpreter
RUN poetry env use $VIRTUAL_ENV/bin/python

# Install project dependencies
RUN poetry install --no-root --no-interaction --no-ansi --no-cache

# Expose Django port
EXPOSE 8000

# Start the Django server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
