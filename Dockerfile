FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip install numpy
RUN pip install -r requirements.txt

RUN python scripts/generators/generate_datasets.py
RUN python scripts/train/content_filtering.py
RUN python scripts/train/collaborative_filtering.py

COPY ./ml_models /app/ml_models

ENTRYPOINT ["python"]

CMD ["app.py"]
