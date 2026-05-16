FROM python:3.13-slim
COPY pip.txt .
RUN pip install --no-cache-dir -r pip.txt && rm pip.txt
COPY . .
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]