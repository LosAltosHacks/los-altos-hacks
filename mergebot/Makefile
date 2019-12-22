SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Default - top level rule is what gets ran when you run just `make`
build: out/image-id
.PHONY: build

# Clean up the output directories; since all the sentinel files go under tmp, this will cause everything to get rebuilt
clean:
	rm -rf out
.PHONY: clean

# Docker image
out/image-id: $(shell find src -type f) Dockerfile requirements.txt
	mkdir -p $(@D)
	image_id="lah/mergebot:$(call rand_id)"
	docker build --tag="$${image_id}" .
	echo "$${image_id}" > out/image-id

define rand_id
$(shell head --bytes=20 /dev/urandom | base32)
endef

run: out/image-id
	docker run -it --rm --publish 3000:8080 $$(cat out/image-id)
.PHONY: run


SERVE_CONTAINER_NAME = mergebot_serve

serve: out/image-id
	watchexec --watch src --restart $(MAKE) serve_restart
.PHONY: serve

serve_start: out/image-id
	@echo ========= RESTARTING DOCKER CONTAINER =========
	docker run -i --rm --publish 3000:8080 --name $(SERVE_CONTAINER_NAME) -e PYTHONUNBUFFERED=1 $$(cat out/image-id) 2>&1
.PHONY: serve_start

serve_stop:
	docker container stop $(SERVE_CONTAINER_NAME) || true
.PHONY: serve_stop

serve_restart: serve_stop serve_start
	@echo "RESTARTED APP $(SERVE_CONTAINER_NAME)"
.PHONY: serve_restart
