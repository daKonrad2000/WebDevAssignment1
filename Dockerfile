FROM python:latest
WORKDIR /src
COPY . .
RUN pip install requests
RUN pip install analysis
CMD python server.py