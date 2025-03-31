## Seroflow
![PyPI](https://img.shields.io/pypi/v/seroflow)
![Python](https://img.shields.io/pypi/pyversions/seroflow)
<!-- [![codecov](https://codecov.io/gh/<USERNAME>/<REPO>/branch/main/graph/badge.svg)](https://codecov.io/gh/<USERNAME>/<REPO>) -->
[![Documentation Status](https://readthedocs.org/projects/seroflow/badge/?version=latest)](https://seroflow.readthedocs.io/en/latest/?badge=latest)

Welcome to **Seroflow**! This repository contains the source code, documentation, and examples to help you get started and contribute to this project.

## Overview
`Seroflow` is a powerful Python package designed to help users build and execute efficient data pipelines. Developing ETL, ELT and other forms of data pipelines has never been easier with `Seroflow's` emphasis on performance, customization and ease-of-use.

With `Seroflow`, each phase of your data pipeline is broken down into concrete steps: `Extractor` steps for data extraction, `Transformation` steps for data manipulation, and `Loader` steps for data loading. Think of it like assembling a Lego set—Seroflow provides all the essential bricks, and you simply pick and add the desired step objects sequentially into a `Pipeline` object, then run `pipeline.execute()` to run your entire process. 

Additionally, the package supports seamless creation of custom `Extractors`, `Loaders`, and `Transformations` through its intuitive interfaces, along with robust features like logging, caching, and chunking. Plus, it comes preloaded with over 70+ predefined transformations, making it an indispensable tool for data pipeline creation and execution.

To Get Started using Seroflow head over to our [Get Started](docs/getting_started.md) Page.

## Table of Contents

- [Seroflow](#seroflow)
- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
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

To install the package from PyPI, simply run the following command:

```bash
pip install seroflow
```

## Documentation
The documentation for the various components in the Seroflow package can be found [here](). It is recommended that users review some of these components prior to using the package.

## License
This project is licensed under the MIT License. Please review the [License](LICENSE.md) for more details.

## Contributing
We welcome contributions! Please read our [Contributing](docs/contributing.md) for guidelines on how to contribute to the project.
