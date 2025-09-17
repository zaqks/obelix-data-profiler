FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies globally
RUN pip install --no-cache-dir --ignore-requires-python -r requirements.txt

# Copy remaining sources
COPY . .

# Give execution permission on build.sh and run it

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
