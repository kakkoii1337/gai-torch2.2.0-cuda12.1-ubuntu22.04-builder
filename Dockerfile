FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-devel

# Create virtual env even though its root for consistency in troubleshooting
ENV HOME_PATH="/home/$USERNAME"
ENV PACKAGES_PATH="${HOME_PATH}/.venv/lib/${PYTHON_VERSION}/site-packages"
RUN python -m venv ${HOME_PATH}/.venv
SHELL ["/bin/bash","-c"]
ENV PATH="${HOME_PATH}/.venv/bin:${PATH}"

ENTRYPOINT ["tail", "-f", "/dev/null"]
