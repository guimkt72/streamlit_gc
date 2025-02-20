FROM python:3.10-slim

RUN pip install streamlit pandas openpyxl

COPY ./src/main.py /src/main.py

WORKDIR /src 

ENTRYPOINT [ "streamlit", "run", "main.py" ]