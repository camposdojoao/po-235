# PO-235 Project Architecture

This document presents the architecture and organizational structure of the PO-235 project, detailing the purpose of each directory and how project components are organized.

## Overview

The PO-235 project is a data science application focused on wine quality analysis and prediction using machine learning techniques. The project was structured following software engineering best practices, separating responsibilities into different layers and modules.

## Directory Structure

```
po-235/
├── 📂 .github/             # GitHub workflows and actions
│   └── workflows/
│       ├── ci.yaml        # Continuous Integration pipeline
│       └── cd.yaml        # Continuous Deployment pipeline
├── 📂 .streamlit/          # Streamlit configuration
│   ├── config.toml        # App configuration
│   └── secrets.toml       # Secrets (not versioned)
├── 📂 docs/                # Project documentation
│   ├── 1_environment_setup.md
│   ├── 2_contribution_guide.md
│   ├── 3_project_architecture.md
│   └── img/               # Documentation images
├── 📂 entrypoints/         # Application entry points
│   ├── st_app.py          # Streamlit app entry point
│   └── train.py           # Model training script
├── 📂 models/              # ML model logic and artifacts
│   ├── __init__.py
│   ├── model.py           # Model training class
│   ├── preprocessing.py   # Data preprocessing
│   ├── inferences.py      # Inference utilities
│   └── random_forest_model.joblib  # Trained model
├── 📂 src/                 # Source data
│   ├── winequality-red.csv
│   ├── winequality-white.csv
│   └── winequality.names
├── 📂 streamlit_app/       # Streamlit UI components
│   ├── __init__.py
│   ├── models.py          # UI model components
│   └── model_loader.py    # Model loader from GitHub
├── 📂 tests/               # Automated tests
│   ├── __init__.py
│   ├── conftest.py        # Pytest configuration
│   ├── test_model.py      # Model tests
│   ├── test_preprocessing.py  # Preprocessing tests
│   ├── test_inferences.py # Inference tests
│   └── test_train.py      # Training pipeline tests
├── 📜 .gitignore           # Git ignore patterns
├── 📜 LICENSE              # MIT License
├── 📜 Makefile             # Automation commands
├── 📜 pyproject.toml       # Project dependencies (UV)
├── 📜 uv.lock              # Locked dependencies
├── 📜 requirements.txt     # Legacy requirements
└── 📜 README.md            # Project overview
```

## Directory Descriptions

### 📁 `.github/`

**Purpose:** GitHub-specific configurations and automation.

Contains workflows for CI/CD:

- **ci.yaml**: Continuous Integration
  - Runs on PRs and feature branches
  - Executes tests, linting, coverage checks
  - Validates branch naming conventions
  
- **cd.yaml**: Continuous Deployment
  - Triggered by version tags (`v*`)
  - Trains model with 100% of data
  - Creates GitHub Release with model artifacts

### 📁 `.model_cache/`

**Purpose:** Cache directory for models downloaded from GitHub Releases.

The `ModelLoader` downloads and caches models here to avoid repeated downloads. Models are cached with their version tags (e.g., `random_forest_model.pkl_v1.4.0`).

### 📁 `.streamlit/`

**Purpose:** Streamlit application configuration.

Contains:
- **config.toml**: App settings (theme, server config, browser settings)
- **secrets.toml**: Secret keys and tokens (git-ignored)

### 📁 `configs/`

**Purpose:** Store project configuration files.

This directory is designated to centralize all configurations needed for the application to function, such as:

- ML model configurations (hyperparameters)
- Database connection settings
- Environment variables
- Pipeline execution parameters
- Logging and monitoring settings

**Example structure:**
```
configs/
├── model_config.yaml
├── database_config.yaml
└── pipeline_config.json
```

### 📁 `docs/`

**Purpose:** Project documentation.

Contains all technical and user documentation:

- **1_environment_setup.md**: Complete environment setup guide
- **2_contribution_guide.md**: Standards and best practices for contributing
- **3_project_architecture.md**: Architecture documentation (this document)
- **img/**: Folder with images and screenshots used in documentation

**Best practices:**
- Keep documentation updated as the project evolves
- Include diagrams and examples when necessary
- Use standardized naming for files

### 📁 `entrypoints/`

**Purpose:** Application entry points.

This directory contains the main scripts that initialize different application components:

- **st_app.py**: Streamlit web application entry point
- **train.py**: Model training pipeline script

**Current structure:**
```
entrypoints/
├── __init__.py
├── st_app.py      # Streamlit app
└── train.py       # Model training
```

**Characteristics:**
- Scripts should be independent and executable
- Each entrypoint should have a single, well-defined responsibility
- Enables future integration with orchestration tools (Airflow, Prefect, etc.)

### 📁 `models/`

**Purpose:** Machine learning model logic and trained artifacts.

Contains:
- **model.py**: Model training class (`Modelo`)
- **preprocessing.py**: Data preprocessing class (`Preprocessing`)
- **inferences.py**: Inference utilities class (`Inferences`)
- **random_forest_model.joblib**: Trained model file

**Current structure:**
```
models/
├── __init__.py
├── model.py               # Training logic
├── preprocessing.py       # Data preprocessing
├── inferences.py          # Inference utilities
└── random_forest_model.joblib  # Trained model
```

**Model Details:**
- Algorithm: Random Forest Classifier
- Features: 11 physicochemical properties
- Target: Wine quality categories (0: Poor, 1: Average, 2: Good)
- Training: 100% of data by default (no test split)

**Best practices:**
- Use model versioning
- Include metadata about performance and training date
- Consider using tools like MLflow for model management

### 📁 `src/`

**Purpose:** Source data storage.

This directory contains the data used in the project:

**Current data:**
- **winequality-red.csv**: Dataset with physicochemical characteristics of red wines
- **winequality-white.csv**: Dataset with physicochemical characteristics of white wines
- **winequality.names**: Documentation and dataset metadata

**Structure:**
```
src/
├── winequality-red.csv    # Red wine data (1,599 samples)
├── winequality-white.csv  # White wine data (4,898 samples)
└── winequality.names      # Dataset documentation
```

### 📁 `streamlit_app/`

**Purpose:** Streamlit web interface components.

Dedicated directory for the interactive web application built with Streamlit:

- **models.py**: UI components for model interaction
- **model_loader.py**: Model loading from GitHub Releases

**Current structure:**
```
streamlit_app/
├── __init__.py
├── models.py          # UI components
└── model_loader.py    # GitHub Release loader
```

**Features:**
- Interactive form for wine property input
- Real-time prediction display
- Model version tracking
- Automatic model downloading from GitHub Releases

**Usage:**
```bash
make streamlit
# or
uv run streamlit run entrypoints/st_app.py
```

### 📁 `tests/`

**Purpose:** Automated project tests.

Contains all unit and integration tests:

- **conftest.py**: Pytest fixtures and configuration
- **test_model.py**: Model training and evaluation tests
- **test_preprocessing.py**: Data preprocessing tests
- **test_inferences.py**: Inference logic tests
- **test_train.py**: Training pipeline tests

**Current structure:**
```
tests/
├── __init__.py
├── conftest.py            # Fixtures
├── test_model.py          # Model tests
├── test_preprocessing.py  # Preprocessing tests
├── test_inferences.py     # Inference tests
└── test_train.py          # Pipeline tests
```

**Test Coverage:**
- Target: >75% coverage
- Includes unit and integration tests
- Runs automatically in CI pipeline

**Best practices:**
- Use pytest as testing framework
- Maintain test coverage above 75%
- Run tests automatically in CI/CD pipeline

## Root Files

### 📄 `Makefile`

Automation file with helper commands for common tasks:

**Available commands:**
- **install-uv**: Install UV package manager
- **install-dev**: Install project dependencies
- **streamlit**: Start Streamlit application
- **test**: Run automated tests
- **check**: Run code quality checks (linting, formatting)
- **format**: Auto-format code
- **clean**: Clean cache and temporary files

**Usage:**
```bash
make install-dev
make streamlit
make test
```

**Benefits:**
- Standardizes commands across developers
- Simplifies complex tasks into simple commands
- Documents build and deployment processes

### 📄 `pyproject.toml`

Modern Python project configuration file (PEP 518/621):

- Project metadata and dependencies
- UV package manager configuration
- Tool configurations (pytest, ruff, coverage)
- Build system requirements

### 📄 `uv.lock`

Locked dependency versions managed by UV. Ensures reproducible environments across all developers and deployments.

### 📄 `README.md`

Main documentation and entry point for new developers. Contains:

- Project overview
- Initial setup instructions
- Links to detailed documentation
- Quick start guide

### 📄 `LICENSE`

Project license file (MIT License), defining terms of use and code distribution.

## CI/CD Pipeline

### Continuous Integration (CI)

Triggered on:
- Pull requests to `main`
- Pushes to `feature/**` and `fix/**` branches

**Checks:**
1. **Unit Tests**: Validates function behavior
2. **Code Coverage**: Minimum 75% required
3. **Linting**: Verifies code standards (ruff)
4. **Branch Naming**: Confirms correct naming (feature/* or fix/*)

### Continuous Deployment (CD)

Triggered on:
- Push of version tags (e.g., `v1.5.0`)

**Process:**
1. Installs dependencies
2. Trains model with 100% of data
3. Creates GitHub Release
4. Uploads model artifacts (`.pkl` and metadata)
5. Makes model available for automatic download

## Workflow

### 1. Development Flow

```
git pull
    ↓
create branch (feature/* or fix/*)
    ↓
development
    ↓
test locally (make test)
    ↓
git commit
    ↓
git push
    ↓
create PR
    ↓
CI runs automatically
    ↓
code review
    ↓
merge to main
```

### 2. Model Training and Deployment

```
code changes
    ↓
create version tag (git tag v1.5.0)
    ↓
push tag (git push origin v1.5.0)
    ↓
CD pipeline triggers
    ↓
model trained with latest code
    ↓
GitHub Release created
    ↓
Streamlit app downloads new model
```

### 3. Local Development

```
clone repository
    ↓
setup environment (make install-dev)
    ↓
develop features
    ↓
run tests (make test)
    ↓
run app locally (make streamlit)
```

## Technologies Used

- **Python 3.11**: Main language
- **UV**: Modern package and environment manager (written in Rust)
  - Manages Python versions
  - Manages project dependencies
  - Creates virtual environments automatically
  - Extremely fast compared to traditional tools
- **GitHub**: Version control and CI/CD
- **Streamlit**: Web interface framework
- **pytest**: Testing framework
- **scikit-learn**: Machine learning library
- **pandas & numpy**: Data manipulation
- **joblib**: Model serialization

## Best Practices

### Code Organization

1. **Separation of Concerns**: Each directory has a clear and specific purpose
2. **Modularity**: Each file has a single, well-defined responsibility
3. **Testability**: Structure facilitates test creation and execution
4. **Documentation**: Code and architecture are well-documented

### Versioning

1. **Branch Naming**: Use `feature/` or `fix/` prefixes
2. **Commits**: Clear and descriptive messages
3. **Pull Requests**: Code review before merging
4. **Tags**: Semantic versioning for releases (v1.0.0, v1.5.0, v2.0.0)

### Documentation

1. Keep documentation updated with code changes
2. Document architectural decisions
3. Include examples and diagrams when necessary
4. Use English for consistency

### Testing

1. Write tests for new features
2. Maintain >75% code coverage
3. Run tests before creating PR
4. Fix failing tests immediately

## Getting Started

To work on the project:

1. Setup environment following [1_environment_setup.md](./1_environment_setup.md)
2. Understand contribution flow in [2_contribution_guide.md](./2_contribution_guide.md)
3. Explore directory structure as needed
4. Develop following described best practices

## Model Details

### Current Model Configuration

- **Algorithm**: Random Forest Classifier
- **Features**: 11 physicochemical properties
  - fixed acidity, volatile acidity, citric acid, residual sugar
  - chlorides, free sulfur dioxide, total sulfur dioxide
  - density, pH, sulphates, alcohol
- **Target**: Quality categories
  - 0: Poor (≤ 5)
  - 1: Average (6)
  - 2: Good (≥ 7)
- **Training Split**: 100% training (default), optional test split
- **Random State**: 42 (for reproducibility)

### Model Loading Strategy

Models are loaded from GitHub Releases:
1. Check `.model_cache/` for cached version
2. If not cached, download from GitHub Release
3. Cache locally for future use
4. Version specified by `MODEL_VERSION` env var or latest

## Contact and Support

For questions about architecture or improvement suggestions, contact the project team.

---

**Last Updated**: November 2024
**Document Version**: 2.0

