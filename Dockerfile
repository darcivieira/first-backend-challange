FROM python:3.10

RUN apt-get update && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/* && \
    localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8

ENV LANG pt_BR.UTF-8

ENV LC_ALL pt_BR.UTF-8

RUN mkdir /src

ENV PYTHONUNBUFFERED=1

RUN cat /etc/issue

WORKDIR /src

COPY . .

CMD bash start_project.sh
