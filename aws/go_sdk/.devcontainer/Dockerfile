ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# Add the root directory to git safe directories.
RUN git config --global --add safe.directory '/workspace'

# Install golang packages.
ENV GOPROXY="direct"
RUN go install -v golang.org/x/tools/gopls@latest
RUN go install -v honnef.co/go/tools/cmd/staticcheck@latest
RUN go install -v github.com/go-delve/delve/cmd/dlv@latest