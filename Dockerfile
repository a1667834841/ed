FROM joyzoursky/python-chromedriver:3.7-selenium


RUN mkdir /usr/share/fonts/chinese
COPY ./songti.ttf /usr/share/fonts/chinese/
RUN fc-cache -fv

RUN mkdir /opt/py
WORKDIR /opt/py
RUN ls /usr/local/bin
COPY requirements.txt ./
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=60 --no-cache-dir -r requirements.txt
COPY . /opt/py/
EXPOSE 5000

VOLUME /opt/py/resources

CMD [ "python", "/opt/py/app.py" ]
