ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN conda init zsh

RUN python -m pip install --upgrade pip

RUN pip install --upgrade \
    ipympl \
    tensorflow \
    torch \
    torchvision \
    boto3 \
    sagemaker \
    uv \
    openai \
    anthropic \
    "anthropic[bedrock]" \
    mcp
