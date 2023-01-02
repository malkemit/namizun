FROM python:3.10-slim-buster

WORKDIR /var/www/

RUN mkdir namizun

COPY . ./namizun

WORKDIR /var/www/namizun

RUN pip3 install virtualenv

RUN useradd -m foo \
    && chown -R foo:foo /home/foo \
    && chown -R foo:foo /var/www/namizun
USER foo

RUN python3 -m venv venv \
    && /var/www/namizun/venv/bin/pip3 install -r requirements.txt
#RUN /var/www/namizun/venv/bin/pip3 install wheel
#RUN /var/www/namizun/venv/bin/pip3 install namizun_core/ namizun_menu/

USER root
RUN ln -s /var/www/namizun/else/namizun /usr/local/bin/ \
    && chmod +x /usr/local/bin/namizun
    
CMD [ "/var/www/namizun/venv/bin/python3", "uploader.py"]

