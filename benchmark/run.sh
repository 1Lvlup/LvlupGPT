# Poetry install and setup
poetry:
	poetry install
	poetry config virtualenvs.create false
	poetry shell

.env:
	cp .env.example $@

openai-key: .env
	@echo "Please fill out the OpenAI Key in the .env file."

# Backend setup
backend:
	cd backend && pip install -r requirement.txt

run-backend: backend openai-key
	cd backend && uvicorn main:app --reload

# Frontend setup
frontend:
	cd frontend && npm install

dev-frontend: frontend
	cd frontend && npm run dev

# Main targets
.PHONY: all
all: run-backend dev-frontend

.PHONY: clean
clean:
	find . -name '*.pyc' -type f -delete
	find . -name '__pycache__' -type d -delete
	cd backend && rm -rf __pycache__/
	cd frontend && rm -rf node_modules/ dist/
