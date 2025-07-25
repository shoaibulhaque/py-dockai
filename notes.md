# Docker Revision Notes

## 🐳 What is Docker?

Docker creates **separate computers** (containers) inside your computer. Each container has:
- Its own operating system (usually Linux)
- Its own files and folders  
- Its own Python/packages
- **Nothing affects your real computer!**

---

## 🔍 Proof: Containers are Separate

### Quick Tests You Can Run:

```bash
# Test 1: Different OS
docker run -it python:3.13.4-slim-bullseye cat /etc/os-release
# Shows "Debian" (even if your computer is Ubuntu/Windows/Mac)

# Test 2: Different Python location
docker run -it python:3.13.4-slim-bullseye which python
# Shows /usr/local/bin/python (different from your computer)

# Test 3: Install package in container only
docker run -it python:3.13.4-slim-bullseye bash
pip install requests
python -c "import requests"  # Works
exit
# Now try on your computer:
python -c "import requests"  # Fails! Not installed locally
```

**Remember**: `pip install` in container = only in container, never on your computer!

---

## 📁 Dockerfile Basics

### Essential Instructions:

```dockerfile
FROM python:3.13.4-slim-bullseye    # Choose base OS + Python
RUN python -m venv /opt/venv/        # Create virtual environment  
ENV PATH=/opt/venv/bin:$PATH         # Use virtual environment
WORKDIR /app                         # Set working folder
COPY requirements.txt /tmp/requirements.txt  # Copy dependency list
RUN pip install -r /tmp/requirements.txt     # Install packages
COPY ./src .                         # Copy your code
CMD ["python", "-m", "http.server", "8000"]  # Start command
```

### What Each Does:
- **FROM**: Pick starting point (OS + Python already installed)
- **RUN**: Run commands while building (like installing packages)
- **ENV**: Set environment variables (like PATH)
- **WORKDIR**: Set current folder (like `cd /app`)
- **COPY**: Copy files from your computer to container
- **CMD**: What runs when container starts

### File Locations in Container:
```
Container /
├── opt/venv/          # Virtual environment
│   ├── bin/python     # Python executable
│   └── lib/           # Installed packages
├── app/               # Your code (WORKDIR)
│   ├── main.py
│   └── other files
└── tmp/
    └── requirements.txt  # Temporary file
```

---

## 🐍 Why Virtual Environment in Container?

Even though container is isolated, virtual environment is still useful:

**Without virtual env**: Your packages mix with base image packages
```bash
pip install flask  # Goes to system Python folder
```

**With virtual env**: Your packages stay separate and clean
```bash
python -m venv /opt/venv  # Create clean environment
pip install flask         # Goes to /opt/venv folder only
```

**Benefits**: 
- Cleaner package management
- Easy to remove all packages (delete /opt/venv folder)
- Same practice as local development

---

## 🏗️ Docker Commands

### Build and Run:
```bash
# Build image
docker build -t myapp .

# Run container
docker run -it -p 8080:8000 myapp

# Run with terminal access
docker run -it myapp bash
```

### Docker Compose:
```bash
# Start all services
docker compose up

# Build and start
docker compose up --build

# Stop everything
docker compose down

# View logs
docker compose logs
```

---

## 📋 Docker Compose Features

### Basic Structure:
```yaml
services:
  backend:
    build:
      context: ./backend      # Folder with Dockerfile
      dockerfile: Dockerfile  # Dockerfile name
    ports:
      - 8080:8000            # host_port:container_port
    command: uvicorn main:app --host 0.0.0.0 --port 8000
```

### Advanced Features:

#### Volumes (File Sharing):
```yaml
volumes:
  - ./backend/src:/app  # Share local folder with container
```
- **Two-way sync**: Changes in container appear on your computer and vice versa
- **Live updates**: Edit files locally, see changes in container immediately
- **Ignores .dockerignore**: Mounts everything in the folder

#### Development Mode:
```yaml
develop:
  watch:
    - action: rebuild      # Rebuild image when these change
      path: backend/requirements.txt
    - action: restart      # Restart container when code changes  
      path: backend/src/
```

**Actions**:
- **rebuild**: Recreate entire image (slow, for major changes)
- **restart**: Restart container (fast, for code changes)
- **sync**: Copy files (fastest, for small changes)

#### Multiple Port Mappings:
```yaml
ports:
  - 8000:8000  # Access via localhost:8000
  - 3000:8000  # Also access via localhost:3000 (same service)
```

---

## 🔧 Common Issues & Fixes

### Container Exits Immediately
**Problem**: Container starts then stops right away
**Fix**: Make sure CMD runs a long-running process
```dockerfile
CMD ["python", "-m", "http.server", "8000"]  # Good - stays running
CMD ["echo", "hello"]                         # Bad - exits immediately
```

### File Not Found During COPY
**Problem**: `COPY ./src .` fails
**Fix**: Make sure `src` folder exists next to Dockerfile

### Typos in File Names
**Problem**: `COPY requirements.txt /tmp/requirments.txt` (missing 'i')
**Fix**: Check spelling carefully - container names must match exactly

### Port Already in Use
**Problem**: "Port 8000 already in use"
**Fix**: Use different host port: `8001:8000` instead of `8000:8000`

---

## 🎯 Key Points to Remember

### Container = Separate Computer
- Has its own OS (usually Linux)
- Has its own files (completely separate from yours)
- Has its own Python and packages
- **Nothing you do in container affects your real computer**

### File Locations Matter
- `/opt/venv` = virtual environment in container
- `/app` = your code in container (set by WORKDIR)
- `./src` = your local folder on your computer

### Two Types of Isolation
1. **Container isolation**: Container vs your computer
2. **Virtual environment isolation**: Your packages vs base image packages

### Volume vs COPY
- **COPY**: Copies files during build (permanent in image)
- **Volume**: Shares files during run (live sync, temporary)

---

## ⚡ Quick Commands for Testing

```bash
# Test container isolation
docker run -it python:3.13.4-slim-bullseye bash
pip install requests
python -c "import requests; print('Only in container!')"
exit

# Check what's running
docker ps

# Get into running container
docker exec -it <container-name> bash

# Clean up everything
docker system prune
```

---

## 📝 Revision Checklist

✅ **Understand**: Container = separate computer with its own OS
✅ **Remember**: `pip install` in container ≠ pip install on your computer  
✅ **Know**: WORKDIR sets current folder in container
✅ **Know**: Volumes share files between your computer and container
✅ **Practice**: Build → Run → Test → Debug cycle
✅ **Remember**: Virtual env in container = extra cleanliness
