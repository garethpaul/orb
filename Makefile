.PHONY: build check lint race static-check test verify vet

check: test race lint static-check

verify: check

build: test

lint: vet

test:
	go test ./...

race:
	go test -race ./...

vet:
	go vet ./...

static-check:
	python3 scripts/check-baseline.py
