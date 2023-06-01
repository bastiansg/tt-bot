ARG CORE_IMAGE

FROM ${CORE_IMAGE}

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    zsh \
    vim \
    htop \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/tmp/* /var/lib/apt/lists/*

WORKDIR /tmp

# Jupyter terminal with zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
ENV SHELL=/usr/bin/zsh
RUN chsh root -s $SHELL

# Jupyterlab dark theme
RUN mkdir -p ~/.jupyter/lab/user-settings/@jupyterlab/apputils-extension \
    && echo '{"theme": "JupyterLab Dark"}' > ~/.jupyter/lab/user-settings/@jupyterlab/apputils-extension/themes.jupyterlab-settings

# Therminal dark theme
RUN mkdir -p ~/.jupyter/lab/user-settings/@jupyterlab/terminal-extension \
    && echo '{"theme": "dark"}' > ~/.jupyter/lab/user-settings/@jupyterlab/terminal-extension/plugin.jupyterlab-settings

# Execution time & max number of outputs
RUN mkdir -p ~/.jupyter/lab/user-settings/@jupyterlab/notebook-extension \
    && echo '{"recordTiming": true, "maxNumberOutputs": 10000}' > ~/.jupyter/lab/user-settings/@jupyterlab/notebook-extension/tracker.jupyterlab-settings

# Install jupyter python packages
COPY ./build/jupyter/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install --break-system-packages -r requirements.txt

# Clean
RUN rm -rf /tmp/*

WORKDIR /notebooks

RUN jupyter labextension disable "@jupyterlab/apputils-extension:announcements"

COPY ./build/jupyter/entrypoint.sh /usr/bin/entrypoint.sh
ENTRYPOINT sh /usr/bin/entrypoint.sh
