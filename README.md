# 2026_MLOps_ShapeInspection_Tossy
Computer vision API and MLOps prototype built with Python and Docker

# NEGI MLOps Project

MLOps / 推論API プロジェクトです。

## Run

```bash
pip install -r requirements.txt
python main.py
```

# Vision MLOps Prototype

A Python-based prototype for computer vision inference, dataset handling, and containerized API deployment.

## Overview

This repository is a prototype project for building a lightweight vision-oriented ML workflow.  
It focuses on organizing inference logic, API structure, data output, and reproducible local execution using Docker.

The project is designed as a practical foundation for:

- image-based inference workflows
- structured dataset export
- modular backend development
- local MLOps experimentation
- containerized deployment and testing

## Goals

The main goals of this repository are:

- provide a clean Python project structure for vision-related inference
- separate routing, service logic, runtime logic, and schema definitions
- support reusable data export for later training / evaluation workflows
- make local setup reproducible through Docker and dependency control
- serve as a base for future expansion into training, evaluation, and model versioning

## Project Structure

```text
.
├── app/
│   ├── data/
│   ├── routers/
│   ├── services/
│   ├── dataset_writer.py
│   ├── inference.py
│   ├── model_runtime.py
│   ├── schemas.py
│   └── settings.py
├── testdata/
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## Architecture

### This repository follows a simple modular structure:

main.py
Application entry point
app/routers/
API route definitions
app/services/
Service-layer logic and reusable processing flows
app/inference.py
Core inference-related processing
app/model_runtime.py
Runtime integration for model execution
app/dataset_writer.py
Structured export of inference-related outputs for downstream use
app/schemas.py
Request / response and internal data schemas
app/settings.py
Environment and configuration management

## Tech Stack
Python
Docker / Docker Compose
API-oriented backend structure
Schema-based request / response design
Dataset export pipeline concepts
Local development workflow for ML-related services

## Local Setup
### 1. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```
On Windows:
```bash
.venv\Scripts\activate
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the application
```bash
python main.py
```

If the project uses an ASGI server such as Uvicorn, it may also be started with:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
## Docker Usage
### Build
```bash
docker compose build
```
### Run
```bash
docker compose up
```

### Run in background
```bash
docker compose up -d
```
### Stop
```bash
docker compose down
```

### Configuration

Environment-specific values should be managed through a local .env file or application settings.

Typical examples include:

application environment
port number
model path
input / output directories
optional runtime settings

A sample file such as .env.example can be added if needed.

### Data Handling

This repository is designed with dataset-oriented workflows in mind.

Typical responsibilities include:

receiving inference inputs
running prediction logic
organizing structured outputs
saving reusable records for later review, analysis, or model improvement

Large datasets, generated files, secrets, and environment-specific artifacts should be excluded from version control.

### What This Repository Demonstrates

This project is intended to highlight practical engineering areas such as:

modular Python backend organization
vision inference workflow design
runtime abstraction for model execution
structured data export for ML workflows
Docker-based reproducible development environments
maintainable project layout for future MLOps expansion

### Roadmap
Possible future improvements include:

evaluation pipeline integration
model version management
experiment tracking
automated dataset validation
CI/CD integration
container-based deployment refinement

### Notes
This repository is shared as a technical prototype and learning-oriented implementation.
It avoids domain-specific business details and focuses on reusable engineering patterns.

### Author
Personal development / prototype repository
