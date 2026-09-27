IMAGE ?= localhost/ch03-hardened:0.1.0
ARCHIVE ?= ch03-hardened.oci.tar

.PHONY: lint build smoke scan verify clean

lint:
	podman run --rm --interactive docker.io/hadolint/hadolint:v2.14.0 < Dockerfile

build:
	podman build --tag $(IMAGE) .

smoke:
	podman run --rm $(IMAGE) -c 'import os; assert os.getuid() == 10001; print("Lab 2 smoke test passed")'

scan: build
	podman save --format oci-archive --output $(ARCHIVE) $(IMAGE)
	podman run --rm --volume "$(CURDIR):/scan:Z" docker.io/anchore/grype:v0.110.0 oci-archive:/scan/$(ARCHIVE)

verify: lint build smoke

clean:
	rm -f $(ARCHIVE)
