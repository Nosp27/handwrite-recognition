FROM python
COPY . /backend
RUN pip install -r /backend/requirements.txt && \
    mkdir /logs
EXPOSE 8080
ENTRYPOINT ["python", "-m", "backend", "start"]
