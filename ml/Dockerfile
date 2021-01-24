FROM python
COPY . /ml
RUN pip install -r /ml/requirements.txt && \
    mkdir /logs
EXPOSE 1234
ENTRYPOINT ["python", "-m", "ml", "start"]
