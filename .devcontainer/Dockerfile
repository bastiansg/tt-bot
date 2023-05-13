FROM tt-bot/core:latest

WORKDIR /tmp

# Install dev packages
COPY .devcontainer/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install --break-system-packages -r requirements.txt

# Clean
RUN rm -rf /tmp/*
