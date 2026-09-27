FROM docker.io/tensorflow/tensorflow:2.20.0

WORKDIR /work

COPY convert_and_infer.py .

ENV OUTPUT_DIR=/output

ENTRYPOINT ["python", "convert_and_infer.py"]
