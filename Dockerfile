FROM python:3.10-slim

RUN pip install streamlit pandas openpyxl

WORKDIR /src 

COPY . /src

ENTRYPOINT ["streamlit", "run", "main.py"]