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
out/image-id: $(shell find app -type f) Dockerfile requirements.txt
	mkdir -p $(@D)
	image_id="lah/registration:$(call rand_id)"
	docker build --tag="$${image_id}" .
	echo "$${image_id}" > out/image-id

define rand_id
$(shell head --bytes=20 /dev/urandom | base32)
endef

run: out/image-id
	docker run -it --rm --publish 8000:8000 --network=lah_reg $$(cat out/image-id)
.PHONY: run


SERVE_CONTAINER_NAME = lah_registration_serve

serve: out/image-id
	# Get watchexec here: https://github.com/watchexec/watchexec/releases
	watchexec --watch app --restart $(MAKE) serve_restart
.PHONY: serve

serve_start: out/image-id
	@echo ========= RESTARTING DOCKER CONTAINER =========
	docker run -i --rm --publish 8000:8000 --network=lah_reg --name $(SERVE_CONTAINER_NAME) -e PYTHONUNBUFFERED=1 $$(cat out/image-id) 2>&1
.PHONY: serve_start

serve_stop:
	docker container stop $(SERVE_CONTAINER_NAME) || true
.PHONY: serve_stop

serve_restart: serve_stop serve_start
	@echo "RESTARTED APP $(SERVE_CONTAINER_NAME)"
.PHONY: serve_restart

start_db:
	# TODO better error handling here
	docker network create lah_reg || true
	docker container rm --force lah_reg_postgres || true
	docker run --name lah_reg_postgres -d --network=lah_reg --publish 5432:5432 -e POSTGRES_DB=testregistration -e POSTGRES_USER=root postgres:11.5-alpine
