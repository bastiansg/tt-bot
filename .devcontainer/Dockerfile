FROM tt-bot/core:latest

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    vim \
    htop \
    zsh \
    sudo \
    openssh-client \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/tmp/* /var/lib/apt/lists/*

ARG USER_NAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

RUN userdel ubuntu \
    && groupadd --gid $USER_GID $USER_NAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USER_NAME \
    && sudo usermod -aG sudo $USER_NAME \
    && sudo passwd -d $USER_NAME

ENV SHELL=/usr/bin/zsh
RUN chsh $USER_NAME -s $SHELL

WORKDIR /tmp

# Install dev packages
COPY .devcontainer/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install --break-system-packages -r requirements.txt

# Clean
RUN rm -rf /tmp/*

USER $USER_NAME

# Terminal with zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
