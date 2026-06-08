.PHONY: check static-check test vet

check: test vet static-check

test:
	go test ./...

vet:
	go vet ./...

static-check:
	python3 scripts/check-baseline.py
