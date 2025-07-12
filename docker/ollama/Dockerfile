FROM docker.io/ollama/ollama:0.9.5

ARG APP_HOME=/ollama
ARG MODEL_NAME=gemma3:1b

WORKDIR $APP_HOME

RUN addgroup --system app && adduser --system --group app
USER app

RUN ollama serve & \
    sleep 5 && \
    ollama pull $MODEL_NAME && \
    pkill ollama

EXPOSE 11434
