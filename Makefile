.PHONY: build check lint race static-check test verify vet

override REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

check: test race lint static-check

verify: check

build: test

lint: vet

test:
	cd "$(REPO_ROOT)" && go test ./...

race:
	cd "$(REPO_ROOT)" && go test -race ./...

vet:
	cd "$(REPO_ROOT)" && go vet ./...

static-check:
	python3 "$(REPO_ROOT)/scripts/check-baseline.py"
