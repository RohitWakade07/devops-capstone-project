FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service/ ./service/
COPY wsgi.py .

RUN useradd --uid 1000 theia && mkdir -p /app/instance && chown -R theia /app
# OpenShift runs containers as a random uid in group 0, so make /app group-writable
RUN chgrp -R 0 /app && chmod -R g=u /app
USER theia

EXPOSE 8080
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "wsgi:app"]
