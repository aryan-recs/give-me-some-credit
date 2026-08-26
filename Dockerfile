FROM python:3.11-slim

WORKDIR /project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY model ./model
COPY src ./src

ENV PYTHONPATH="/project:/project/src"

EXPOSE 8501

CMD ["sh", "-c", "uvicorn app.app:app --host 127.0.0.1 --port 8000 & streamlit run app/frontend.py --server.port=8501 --server.address=0.0.0.0"]