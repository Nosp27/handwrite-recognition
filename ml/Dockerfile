FROM python
COPY . /ml
RUN pip install -r /ml/requirements.txt && \
    mkdir /logs && \
    apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y libtesseract-dev
EXPOSE 1234
ENTRYPOINT ["python", "-m", "ml", "start", "--model", "TesseractModel"]
