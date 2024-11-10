FROM python:3.12

RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install -y iputils-ping \
    && apt-get install -y dos2unix \
    && apt-get clean -y

WORKDIR /code

COPY add_host.sh /usr/local/bin/add_host.sh
RUN dos2unix /usr/local/bin/add_host.sh
RUN chmod +x /usr/local/bin/add_host.sh

ENTRYPOINT ["/usr/local/bin/add_host.sh"]
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/code/app
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]