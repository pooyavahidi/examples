ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN conda init zsh

RUN python -m pip install --upgrade pip

RUN pip install --upgrade \
    uv \
    boto3 \
    anthropic \
    "anthropic[bedrock]" \
    mcp
