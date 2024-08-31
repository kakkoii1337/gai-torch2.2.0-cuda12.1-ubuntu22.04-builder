FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-devel AS build
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
ENV TORCH_CUDA_ARCH_LIST="7.5 8.0 8.6+PTX"
