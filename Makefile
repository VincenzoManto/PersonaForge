.PHONY: help install parse chat docker-build docker-run

help:
	@echo "🧬 PersonaForge Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install        Install Python dependencies"
	@echo "  make parse          Run the parser (requires APP, FILE, TARGET, OUTPUT)"
	@echo "  make chat           Start chatting with the persona (requires DATASET, MODEL)"
	@echo "  make docker-build   Build the Docker image"
	@echo "  make docker-run     Run the Docker container"

install:
	pip install -r requirements.txt

parse:
	@if [ -z "$(APP)" ] || [ -z "$(FILE)" ] || [ -z "$(TARGET)" ]; then \
		echo "Usage: make parse APP=whatsapp FILE=chat.txt TARGET=\"John\" OUTPUT=john.jsonl"; \
		exit 1; \
	fi
	python main.py parse --app $(APP) --file $(FILE) --target "$(TARGET)" --output $(OUTPUT:-dataset.jsonl)

chat:
	@if [ -z "$(DATASET)" ]; then \
		echo "Usage: make chat DATASET=john.jsonl MODEL=gpt-4-turbo"; \
		exit 1; \
	fi
	python main.py chat --dataset $(DATASET) --model $(MODEL:-gpt-3.5-turbo)

docker-build:
	docker build -t persona-forge .

docker-run:
	docker run -it --rm -v $(PWD):/app persona-forge /bin/bash
