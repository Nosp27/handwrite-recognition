FROM python
COPY . /ml
RUN pip install -r /ml/requirements.txt
EXPOSE 8080
ENTRYPOINT ["python", "-m", "ml", "start"]
