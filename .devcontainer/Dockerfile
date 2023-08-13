FROM tt-bot/core:latest

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    vim \
    htop \
    zsh \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/tmp/* /var/lib/apt/lists/*

WORKDIR /tmp

# Jupyter terminal with zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
ENV SHELL=/usr/bin/zsh
RUN chsh root -s $SHELL

# Install dev packages
COPY .devcontainer/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install --break-system-packages -r requirements.txt

# Clean
RUN rm -rf /tmp/*
