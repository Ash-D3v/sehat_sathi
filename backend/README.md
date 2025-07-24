# Health Chatbot Backend

## Docker Usage

### Build the Docker image
```sh
cd app/health_chatbot_backend
# Build the Docker image (replace 'health-backend' with your preferred image name)
docker build -t health-backend .
```

### Run the Docker container
```sh
# Run the container, mapping port 5000 to your host (for frontend access)
docker run -p 5000:5000 health-backend
```

The backend API will be available at `http://localhost:5000` for your frontend to consume. 