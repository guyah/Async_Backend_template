# Async_Backend_template

## Description

This project serves as a template to quickly start building applications that utilize asynchronous workers. It provides a pre-configured setup with a database and backend already in place. The high-level overview of the services and their purpose within the project are:

1. PostgreSQL: It is built from the Dockerfile.db located in the api directory. The environment variables POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB define the database credentials and name. The data is persisted using a volume named postgres-data, and the service is accessible on port 5432.

2. Node.js Application: The node-app service is built from the Dockerfile located in the gui directory. It represents a simple Node.js application with an express server.

3. Caddy: Caddy is used as reverse-proxy and is configured using the Caddyfile located in the caddy directory. The Caddy service listens on ports 80 and 443 and redirects incoming requests to the corresponding services.

4. RabbitMQ: The RabbitMQ message broker with management capabilities uses several ports. The service is configured with environment variables specifying credentials, virtual hosts, and other settings that could be modified.

5. API: The api service represents the FastAPI-based API application. It is built from the Dockerfile located in the api directory. The container runs the api.sh script as the command. The service exposes port 8000 on the host and depends on the RabbitMQ service.

6. Worker: The worker service is responsible for running the asynchronous workers. It is also built from the Dockerfile in the api directory. The container executes the worker.sh script as the command.

## Structure

This repository contains the following files and directories:

- `api`: This directory contains the FastAPI-based API application that utilizes Celery, RabbitMQ, Socket.IO, and Tortoise ORM. It is an asynchronous application that integrates Sentry for error monitoring.

- `caddy`: This directory contains the Caddyfile configuration used as a reverse proxy for the GUI, API, and RabbitMQ.

- `gui`: This directory contains a simple Node.js application with an `express` server. The server listens on port 3000 and responds with "Hello world!" for the root endpoint.

- `.gitignore`: This file specifies patterns to be ignored by Git.

- `deploy.sh`: This script builds the Docker Compose file for deployment.

- `docker-compose.yml`: This file defines the Docker Compose services and their configurations. It includes services for PostgreSQL, the Node.js application, Caddy as a reverse proxy, RabbitMQ, the API, and a worker. Each service is defined with its respective image, build context, ports, volumes, environment variables, and dependencies.

## Usage

To use this repository, follow these steps:

1. Clone the repository:

    ```bash
   git clone <repository_url>
    ```
2. Set up the required environment variables. Depending on your environment, you may need to create an `.env` file from the `.env.template` located in the api directory.
3. Build and start the docker-hosted services:
    ``` bash
    ./deploy.sh
    ```
4. Access the application:
    - GUI: Open your browser and navigate to http://localhost to see the "Hello world!" message.
    - API: The Swagger api is accessible at http://api.localhost/docs. You can make API requests to this endpoint.
5. Stop the services:
    ```bash
    docker-compose down
    ```
## Configuration
- `api/.env`: This file contains environment variables used by the API and worker services.
- `caddy/Caddyfile`: This file is the configuration file for the Caddy reverse proxy service. Modify this file to add or customize proxy rules.

## Dependencies
The repository requires the following dependencies:
- `Docker`
- `Docker Compose`
Ensure that these dependencies are installed and properly configured on your system before using this repository.

