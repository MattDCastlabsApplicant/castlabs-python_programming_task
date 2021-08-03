
HTTP_PORT=8080
PWD ?= pwd_unknown
PROJECT_NAME = $(notdir $(PWD))
SERVICE_TARGET := main
ifeq ($(user),)
HOST_USER ?= $(strip $(if $(USER),$(USER),nodummy))
HOST_UID ?= $(strip $(if $(shell id -u),$(shell id -u),4000))
else
HOST_USER = $(user)
HOST_UID = $(strip $(if $(uid),$(uid),0))
endif
THIS_FILE := $(lastword $(MAKEFILE_LIST))
CMD_ARGUMENTS ?= $(cmd)
export PROJECT_NAME
export HOST_USER
export HOST_UID

.PHONY: shell help build rebuild service login test clean prune

shell:
ifeq ($(CMD_ARGUMENTS),)
	# no command is given, default to shell
	docker-compose -p $(PROJECT_NAME)_$(HOST_UID) run --rm $(SERVICE_TARGET) sh
else
	# run the command
	docker-compose -p $(PROJECT_NAME)_$(HOST_UID) run --rm $(SERVICE_TARGET) sh -c "$(CMD_ARGUMENTS)"
endif


build:
	docker build -t castlabs_image .
run:
	docker run -p $(HTTP_PORT):$(HTTP_PORT) castlabs_image
