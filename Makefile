ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override REPO_ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)
export REPO_ROOT

.PHONY: build check lint race root-test static-check test verify vet workflow-contract

check: test race lint static-check root-test

verify: check

build: test

lint: vet

test:
	cd "$$REPO_ROOT" && go test ./...

race:
	cd "$$REPO_ROOT" && go test -race ./...

vet:
	cd "$$REPO_ROOT" && go vet ./...

static-check: workflow-contract
	python3 "$$REPO_ROOT/scripts/check-baseline.py"

workflow-contract:
	python3 "$$REPO_ROOT/tests/test_workflow_contract.py"

root-test:
	PYTHONDONTWRITEBYTECODE=1 python3 "$$REPO_ROOT/tests/test_makefile_root.py"
