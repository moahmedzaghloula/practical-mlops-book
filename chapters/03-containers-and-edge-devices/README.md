# Chapter 3 — MLOps for Containers and Edge Devices

## Topics Covered

- Virtual machines versus containers
- Container images, layers, tags, and digests
- Registries and image distribution
- Dockerfile instructions
- Podman rootless containers on Fedora
- ENTRYPOINT and CMD
- Container linting with Hadolint
- Vulnerability scanning with Grype
- Serving an ML model over HTTP
- Model metadata and input validation
- Edge inference and quantization
- TensorFlow Lite
- Coral Edge TPU concepts
- Managed ML container workflows

## Labs

| Lab | Description | Status |
|---|---|---|
| 01 | Container fundamentals | Complete |
| 02 | Container quality and security | Complete |
| 03 | Containerized ML API | Complete |
| 04 | Edge inference CPU simulation | Complete |
| 05 | Legacy Edge TPU compiler | Conditional |

## Important Modernization Notes

- Podman is used instead of Docker as the Fedora-native runtime.
- The retired CentOS 8 example is replaced with Fedora 42.
- Boston Housing is replaced with a deterministic synthetic dataset.
- Azure Percept is studied historically because the product was retired.
- Coral/PyCoral steps are treated as legacy and hardware-dependent.

## Validation

Run each lab from its own directory and follow its README or Makefile.
