
# TERQA

**Test Execution, Regression & Quality Assurance**

[![Unit Tests](https://github.com/aacar33/terqa/actions/workflows/unit-tests.yml/badge.svg?branch=main)](https://github.com/aacar33/terqa/actions/workflows/unit-tests.yml)

## Overview

TERQA is an extensible, cross-platform, Python-based test automation framework designed to support automated software, system and hardware validation.

The project aims to provide a modular, scalable and maintainable foundation for test automation across multiple products, interfaces and technologies.

TERQA is currently under active development.

## Project Objectives

- Provide reusable test automation components.
- Support multiple products, device types and communication protocols.
- Separate framework logic from product-specific test implementations.
- Support cross-platform test development and execution.
- Provide reliable error handling, logging and diagnostics.
- Support automated functional and regression testing.
- Provide centralised test execution and reporting capabilities.
- Maintain framework reliability through continuous integration.
- Minimise hardware and environmental dependencies within framework validation.
- Maintain consistent coding standards and comprehensive documentation.

## Design Principles

- Modularity
- Scalability
- Maintainability
- Extensibility
- Reusability
- Platform independence
- Separation of concerns
- Testability

## Current Capabilities

- Serial communication with embedded devices.
- Command-based device communication.
- JSON response parsing.
- Device response structure and command validation.
- Serial communication timeout handling.
- Sensor data parsing.
- Mock-based unit testing.
- Automated framework unit test execution through GitHub Actions.
- Parametrised unit testing.
- Serial communication exception handling.
- Exception chaining for failure diagnostics.

### Supported Hardware

The initial hardware integration focuses on the following devices:

| Device | Description |
| --- | --- |
| M5Stack Tab5 | Embedded development platform |
| Sensirion SCD40 | CO2, temperature and humidity sensor |

Communication with the M5Stack Tab5 requires compatible device firmware.

TERQA is not intended to be limited to these devices.

## Platform Compatibility

TERQA is designed to be a cross-platform test automation framework, minimising operating system dependencies wherever possible.

| Platform | Compatibility Status |
| --- | --- |
| Windows 11 | Framework unit tests validated locally and through CI |
| Linux (Ubuntu) | Framework unit tests validated through CI |
| Windows Subsystem for Linux (WSL2) | Framework unit tests validated locally |
| macOS | Framework unit tests validated through CI |

Framework unit tests are designed to run independently of physical hardware and external test environments.

Product-specific tests may require additional hardware, drivers, permissions or operating system configuration.

## Repository Structure

```
terqa/
├── .github/
│   └── workflows/
│       └── unit-tests.yml
├── tab5/
│   ├── __init__.py
│   ├── client.py
│   ├── parser.py
│   └── serial_reader.py
├── tests/
│   └── unit/
│       ├── conftest.py
│       ├── test_client.py
│       ├── test_parser.py
│       └── test_serial_reader.py
├── .gitignore
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Technologies

- Python
- pytest
- PySerial
- unittest.mock
- JSON
- Git
- GitHub Actions

## Getting Started

### Prerequisites

- Python 3.14 (current CI baseline)
- Git
- Python venv module

### Windows (PowerShell)

Clone the repository:

```powershell
git clone https://github.com/aacar33/terqa.git
cd terqa
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Run the framework unit tests:

```powershell
python -m pytest -v tests/unit
```

### Linux / WSL2 / macOS

Clone the repository:

```bash
git clone https://github.com/aacar33/terqa.git
cd terqa
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the framework unit tests:

```bash
python -m pytest -v tests/unit
```

On Ubuntu, the appropriate python3-venv package may need to be installed.

Ensure that the Python interpreter used to create the virtual environment matches the current CI Python version.

For WSL2 development, a separate repository clone within the Linux filesystem is recommended.

Framework unit tests are validated on macOS through GitHub Actions.

Local macOS installation and physical device communication have not yet been validated.

### Deactivate the Virtual Environment

```bash
deactivate
```

## Dependency Management

TERQA uses Python virtual environments to isolate local development and testing dependencies.

Development dependencies are maintained in `requirements-dev.txt`.

| Dependency | Version |
| --- | --- |
| pytest | 9.2.0 |
| pyserial | 3.5 |

Virtual environments are excluded from version control and must be created locally.

Each operating system must use its own virtual environment.

Dependency requirements should be maintained consistently across local development and continuous integration environments.

## Testing Strategy

TERQA establishes a clear separation between framework validation and product validation.

### Framework Validation

Framework tests validate the correctness, reliability and integrity of TERQA itself.

These tests are designed to be hardware-independent and use mocking where appropriate.

Framework validation focuses on:

- Functional correctness.
- Regression prevention.
- Input and output validation.
- Exception and error handling.
- Communication interface behaviour.
- Boundary conditions.
- Cross-platform compatibility.
- Framework component integration.
- Simulated communication failures.

Framework validation tests form the basis of TERQA's continuous integration and merge protection strategy.

### Product Validation

Product tests use TERQA to validate the functionality, behaviour, performance and reliability of a product under test.

Future product validation capabilities may include:

- Functional testing.
- Regression testing.
- System testing.
- Integration testing.
- End-to-end testing.
- Hardware-in-the-loop (HITL) testing.
- REST API testing.
- Web UI testing.
- Performance testing.

Product tests may require physical hardware, external services or dedicated test environments.

Product validation is kept separate from framework validation and does not form part of TERQA's required continuous integration merge checks.

## Continuous Integration

TERQA uses GitHub Actions to automatically validate framework changes.

The continuous integration workflow executes framework unit tests on pushes and pull requests targeting the `main` branch.

### Current CI Environment

| Configuration | Value |
| --- | --- |
| CI Platform | GitHub Actions |
| Operating Systems | Windows, Linux and macOS |
| Python Version | 3.14 |
| Test Framework | pytest |
| Execution Strategy | Parallel matrix execution |
| Hardware Required | No |

### Merge Protection

The `main` branch is protected through GitHub repository rules.

All changes must be submitted through pull requests and satisfy the required automated test checks before merging.

Framework unit tests are executed independently across Windows, Linux and macOS.

The aggregate `unit-tests` status check requires successful completion across all three platforms.

A failure on any platform must prevent the pull request from being merged.

Product-specific tests are excluded from the required CI checks.

## Development Workflow

All framework changes should follow the established development workflow:

1. Create a development branch from `main`.
2. Implement the proposed changes.
3. Create or update relevant framework tests.
4. Execute framework tests locally.
5. Update relevant documentation.
6. Commit and push changes.
7. Create a pull request.
8. Verify that all required CI checks pass.
9. Merge approved changes into `main`.

## Documentation

Documentation is maintained alongside framework development.

Changes affecting architecture, functionality, requirements, dependencies or supported platforms should include relevant documentation updates within the same pull request.

Additional technical documentation will be introduced as the framework evolves.

## Development Roadmap

### Framework Foundations

- [x] Serial communication
- [x] Structured device command interface
- [x] JSON response parsing
- [x] Mock-based unit testing
- [x] Git version control
- [x] GitHub Actions integration
- [x] Branch protection configuration
- [x] Development dependency definition
- [x] Shared dependency installation between local development and CI
- [x] Local virtual environment validation
- [x] Enhanced response validation
- [ ] Configuration management
- [ ] Centralised logging and diagnostics
- [ ] Custom exception handling
- [ ] Reusable device interfaces

### Cross-Platform Compatibility

- [x] Linux framework unit testing through CI
- [x] WSL2 validation
- [x] Windows CI validation
- [x] macOS CI validation
- [x] Cross-platform CI merge requirements

### Product Testing Capabilities

- [ ] Hardware-in-the-loop testing
- [ ] REST API testing
- [ ] Web UI testing
- [ ] Performance testing

### Test Management and Reporting

- [ ] Test execution management
- [ ] Test plan management
- [ ] Test result management
- [ ] Test reporting
- [ ] Historical result analysis
- [ ] Regression tracking
- [ ] Test dashboards
- [ ] Parallel test execution
- [ ] Test resource management

## Project Status

TERQA is under active development.

Its architecture, requirements, capabilities and documentation will evolve as development progresses.

Roadmap items represent planned or potential capabilities and are subject to change.
