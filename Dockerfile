# === Builder stage ===
FROM python:3.13-slim AS builder

WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python packages
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the rest of the app source code
COPY . .

# === Final stage ===
FROM python:3.13-slim

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application source code from builder
COPY --from=builder /app /app

# Set PATH so the local pip installs are available
ENV PATH=/root/.local/bin:$PATH

# Expose the port your fastapi app listens on
EXPOSE 8082

# Run the fastapi app
CMD ["fastapi", "run", "app.py", "--port", "8082"]