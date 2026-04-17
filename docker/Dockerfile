FROM python:3.10-slim

WORKDIR /app

COPY . .

# 🔑 IMPORTANT
ENV PYTHONPATH=/app/src

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn httpx tenacity pandas scikit-learn requests

# ✅ Use your existing main.py
CMD ["uvicorn", "oxylabs_ai_studio.apps.main:app", "--host", "0.0.0.0", "--port", "8000"]