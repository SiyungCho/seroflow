## Seroflow Package Guide

Welcome to **Seroflow**! This repository contains the source code, documentation, and examples to help you get started and contribute to this project.

## Overview
`Seroflow` is a powerful Python package designed to help users build and execute efficient ETL (or ELT) data pipelines. ETL stands for Extract, Transform, and Load — a process that extracts data from various sources, transforms it into a suitable format, and then loads it into a destination system. 

With `Seroflow`, each phase of your data pipeline is broken down into concrete steps: `Extractor` steps for data extraction, `Transformation` steps for data manipulation, and `Loader` steps for data loading. Think of it like assembling a Lego set—Seroflow provides all the essential bricks, and you simply pick and add the desired step objects sequentially into a `Pipeline` object, then run `pipeline.execute()` to run your entire process. 

Additionally, the package supports seamless creation of custom `Extractors`, `Loaders`, and `Transformations` through its intuitive interfaces, along with robust features like logging, caching, and chunking. Plus, it comes preloaded with over 70+ predefined transformations, making it an indispensable tool for data pipeline creation and execution.

To Get Started using Seroflow head over to our [Get Started](docs/getting_started.md) Page.

## Table of Contents

- [Seroflow Package Guide](#seroflow-package-guide)
- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using pip](#using-pip)
  - [Installing from Source](#installing-from-source)
- [Documentation](#documentation)
- [License](#license)
- [Contributing](#contributing)

## Prerequisites

Before installing the package, ensure you have the following:

- **Python Version:** Python 3.7 or higher.
- **pip:** The latest version of pip. You can upgrade pip with:
```bash
python -m pip install --upgrade pip
```
- **Virtual Environment (Recommended):** Use venv or virtualenv to create an isolated environment.
```bash
python -m venv venv_name

venv_name\Scripts\activate # Windows OS
source venv_name/bin/activate  # mac/lunix OS
```

## Installation

### Using pip

To install the package from PyPI, run the following command:

```bash
pip install seroflow
```

## Documentation
Below are some links to the documentation provided for the various components in the Seroflow package. It is recommended that users review some of these components prior to using the package.

- [Getting Started](docs/getting_started.md)
- [Seroflow](docs/Seroflow.md)
- [Step](docs/step.md)
- [Transformations](docs/transformations/transformation.md)
- [Extractors](docs/extract.md)
- [Loaders](docs/load.md)
- [Caching](docs/cache.md)
- [Chunking](docs/chunker.md)
- [Engines](docs/engine.md)
- [Contexts](docs/context.md)
- [Logging](docs/log.md)
- [Type Validation](docs/types.md)
- [Utility](docs/utils.md)
- [Wrappers](docs/wrappers.md)

## License
This project is licensed under the MIT License. Please review the license for more details.

## Contributing
We welcome contributions! Please read our [Contributing](docs/contributing.md) for guidelines on how to contribute to the project.
