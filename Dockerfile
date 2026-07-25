FROM python:3.10-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

COPY requirements-dev.txt ./
COPY chapter4/requirements.txt chapter4/requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

ENV PYTHONPATH=/workspace
ENV NODE_ENV=development

CMD ["sleep", "infinity"]
