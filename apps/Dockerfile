FROM python:3.9

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
# RUN pip install --update py-pip && pip install uvicorn fastapi
COPY api_projet3.py .
EXPOSE 8000
CMD uvicorn api_projet3:api --host=0.0.0.0 --reload