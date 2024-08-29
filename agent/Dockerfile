FROM python:3.10.10

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV PYTHONIOENCODING=UTF-8

# Create a user
RUN useradd -u 1000 -ms /bin/bash agent

# Install dependencies
RUN apt-get update \
    && apt-get install -yqq \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/

# Install specific pip version and virtualenv as root
RUN pip install pip==24.0 virtualenv

# Set the working directory
WORKDIR /home/agent

# Switch to the user
USER agent

RUN pip install pip==24.2

# Create a virtual environment
RUN python -m virtualenv /home/agent/venv

# Add the virtual environment's bin directory to PATH
ENV PATH="/home/agent/venv/bin:$PATH"

# Activate the virtual environment and install clearml-agent
RUN python3 -m pip install clearml-agent==1.9.0
RUN python3 -m pip install -U "cryptography>=2.9"

# Copy requirements.txt and install requirements in the virtual environment
# COPY requirements.txt /tmp/requirements.txt
# RUN pip install -q -r /tmp/requirements.txt

# Switch back to root to change permissions and ownership
USER root

# Copy entrypoint.sh, set permissions, and change ownership
ADD entrypoint.sh /home/agent/entrypoint.sh
RUN chmod +x /home/agent/entrypoint.sh
RUN chown agent:agent /home/agent/entrypoint.sh

# Switch back to the agent user
USER agent

# Set git config
RUN git config --global advice.detachedHead false

# Set CLEARML_AGENT_SKIP_PIP_VENV_INSTALL to point to the Python in the virtual environment
# ENV CLEARML_AGENT_SKIP_PIP_VENV_INSTALL="/home/agent/venv/bin/python"
ENV CLEARML_DOCKER_SKIP_GPUS_FLAG=1

# Set the entrypoint
CMD ["./entrypoint.sh"]

