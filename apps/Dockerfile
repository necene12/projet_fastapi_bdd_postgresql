FROM python:3.9
RUN pip install --update py-pip && pip install uvicorn fastapi
COPY api_projet3.py .
EXPOSE 8000
CMD uvicorn api_projet3:api --host=0.0.0.0 --reload