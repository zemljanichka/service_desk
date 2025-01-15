FROM python:3.12
WORKDIR .
RUN pip install --upgrade pip
# Final container build. Uses pre-compiled dependencies and requirements.txt
# obtained in the previous steps
FROM python:3.12
WORKDIR /src
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN export SSL_CERT_FILE=$(python -m certifi)
COPY . /src