.PHONY: build check lint static-check test verify vet

check: test lint static-check

verify: check

build: test

lint: vet

test:
	go test ./...

vet:
	go vet ./...

static-check:
	python3 scripts/check-baseline.py
