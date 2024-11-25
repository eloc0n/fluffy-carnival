# Stage 1: Build stage
FROM python:3.11-slim AS build

WORKDIR /app
# Install dependencies
COPY requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt
# Copy the application code
COPY . .
# Stage 2: Runtime stage
FROM python:3.11-slim
WORKDIR /app
# Copy the virtual environment and application code
COPY --from=build /app /app
# Set the PATH to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"
# Run the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]