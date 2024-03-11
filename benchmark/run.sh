# Poetry install and setup
poetry:		# Poetry is a dependency management tool for Python.
	poetry install	# This command installs the dependencies specified in the pyproject.toml file.
	poetry config virtualenvs.create false	# This command disables the creation of a virtual environment for Poetry.
	poetry shell	# This command activates the Poetry shell.

.env:		# This target copies the .env.example file to .env.
	cp .env.example $@

openai-key: .env	# This target sets the OpenAI key environment variable.
	@echo "Please fill out the OpenAI Key in the .env file."

# Backend setup
backend:	# This target sets up the backend of the application.
	cd backend && pip install -r requirement.txt	# This command installs the required Python packages for the backend.

run-backend: backend openai-key	# This target runs the backend of the application.
	cd backend && uvicorn main:app --reload	# This command starts the backend server using Uvicorn and enables automatic reloading.

# Frontend setup
frontend:	# This target sets up the frontend of the application.
	cd frontend && npm install	# This command installs the required Node.js packages for the frontend.

dev-frontend: frontend	# This target runs the frontend of the application in development mode.
	cd frontend && npm run dev

# Main targets
.PHONY: all	# This target is the default target and runs both the backend and frontend.
all: run-backend dev-frontend

.PHONY: clean	# This target removes unnecessary files and directories.
clean:
	find . -name '*.pyc' -type f -delete
	find . -name '__pycache__' -type d -delete
	cd backend && rm -rf __pycache__/
	cd frontend && rm -rf node_modules/ dist/
