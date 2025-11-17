# Wine Quality Prediction

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

</div>

## 📋 About the Project

This project was developed as part of the **PO-235 - Data Science Project** course, taught by **Professor Filipe Verri**. The goal is to create a machine learning model capable of predicting wine quality based on its characteristics.

Using the [Wine Quality](https://archive.ics.uci.edu/dataset/186/wine+quality) dataset from the UCI Machine Learning Repository, this project explores classification techniques to evaluate red and white wines from the Vinho Verde region in Portugal.

## 🎯 Objectives

- Develop a classification model to predict wine quality
- Analyze the importance of physicochemical characteristics in wine quality
- Implement software engineering best practices in data science projects
- Create an interactive interface for visualization and prediction

## 📊 Dataset

The project uses the **Wine Quality Dataset** provided by the UCI Machine Learning Repository:

- **Source**: [UCI Wine Quality Dataset](https://archive.ics.uci.edu/dataset/186/wine+quality)
- **Instances**: 6,497 samples (1,599 red wines + 4,898 white wines)
- **Features**: 11 physicochemical variables
- **Target**: Wine quality (score from 0 to 10)

### Dataset Variables

| Variable              | Description                |
|-----------------------|----------------------------|
| fixed_acidity         | Fixed acidity              |
| volatile_acidity      | Volatile acidity           |
| citric_acid           | Citric acid                |
| residual_sugar        | Residual sugar             |
| chlorides             | Chlorides                  |
| free_sulfur_dioxide   | Free sulfur dioxide        |
| total_sulfur_dioxide  | Total sulfur dioxide       |
| density               | Density                    |
| pH                    | pH                         |
| sulphates             | Sulphates                  |
| alcohol               | Alcohol content            |
| quality               | Quality (target variable)  |

## 🤖 Methodology

### Model Used

The project uses the **Random Forest** algorithm for wine quality classification:

- **Random Forest** ✅ 
  - Robust and interpretable model
  - Excellent performance on tabular data
  - Resistant to overfitting
  - Provides feature importance

During initial development, other algorithms (XGBoost and Gradient Boosting) were evaluated, but **Random Forest** was chosen as the final model after comparative analysis of performance, evaluation metrics, and interpretability.

### Approach

1. **Exploratory Data Analysis (EDA)**: Understanding distributions and correlations
2. **Preprocessing**: Data treatment, feature engineering
3. **Model Training**: Experimentation with different algorithms
4. **Evaluation**: Comparison of metrics (accuracy, precision, recall, F1-score)
5. **Optimization**: Hyperparameter tuning of the selected model
6. **Deploy**: Interactive web interface with Streamlit

## 🛠️ Technologies Used

- **Python 3.11**: Main project language
- **UV**: Modern Python package and version manager (written in Rust)
- **scikit-learn**: Random Forest implementation and ML pipeline
- **pandas & numpy**: Data manipulation and analysis
- **matplotlib & seaborn**: Data visualization
- **Streamlit**: Interactive web interface
- **pytest**: Testing framework
- **GitHub Actions**: CI/CD pipeline

## 📁 Project Structure

```
po-235/
├── 📂 .github/          # GitHub Actions workflows (CI/CD)
├── 📂 .streamlit/       # Streamlit configuration
├── 📂 docs/             # Project documentation
│   ├── 1_environment_setup.md
│   ├── 2_contribution_guide.md
│   └── 3_project_architecture.md
├── 📂 entrypoints/      # Main scripts (training, prediction, deploy)
│   ├── st_app.py       # Streamlit application entry point
│   └── train.py        # Model training script
├── 📂 models/           # Trained models and artifacts
│   ├── model.py        # Model training logic
│   ├── preprocessing.py # Data preprocessing
│   └── inferences.py   # Inference utilities
├── 📂 src/              # Data sources
│   ├── winequality-red.csv
│   ├── winequality-white.csv
│   └── winequality.names
├── 📂 streamlit_app/    # Streamlit interface components
│   ├── models.py       # UI model components
│   └── model_loader.py # Model loading from GitHub Releases
├── 📂 tests/            # Automated tests
│   ├── test_model.py
│   ├── test_preprocessing.py
│   └── conftest.py
├── 📜 Makefile          # Automation commands
├── 📜 pyproject.toml    # Project dependencies (UV)
├── 📜 uv.lock           # Locked dependencies
├── 📜 requirements.txt  # For streamlit deploy
├── 📜 README.md         # This file
└── 📜 LICENSE           # Project license
```

For more details about the architecture, see [`docs/3_project_architecture.md`](./docs/3_project_architecture.md).

## 🚀 Getting Started

### Prerequisites

- Linux operating system (or WSL on Windows)
- Git installed
- Internet access for downloading dependencies

### Installation and Configuration

For complete development environment setup, follow the detailed guide in [`docs/1_environment_setup.md`](./docs/1_environment_setup.md).

**Quick start:**

1. **Clone the repository**
   ```bash
   git clone https://github.com/camposdojoao/po-235.git
   cd po-235
   ```

2. **Setup environment**
   ```bash
   make install-uv
   make install-dev
   ```

3. **Run the Streamlit application**
   ```bash
   make streamlit
   ```

## 🤝 How to Contribute

This project follows collaborative development best practices with simplified Git Flow. To contribute:

1. Update the `main` branch
2. Create a branch following the pattern `feature/*` or `fix/*`
3. Develop and test your changes
4. Commit with descriptive messages
5. Create a Pull Request

For detailed instructions, see [`docs/2_contribution_guide.md`](./docs/2_contribution_guide.md).

### CI/CD Pipeline

#### Continuous Integration (CI)

The CI pipeline runs automatically on:
- Pull requests to `main` branch
- Pushes to `feature/**`, `fix/**` branches

**Validation steps:**
1. ✅ **Branch naming validation** - Ensures branches follow patterns: `feature/*`, `fix/*`, `hotfix/*`, `release/*`
2. ✅ **Code linting** - Checks code style with `ruff check`
3. ✅ **Format validation** - Ensures code formatting with `ruff format --check`
4. ✅ **Dependency sync** - Validates `requirements.txt` is in sync with `pyproject.toml`
5. ✅ **Unit tests + coverage** - Runs all tests with minimum 75% code coverage
6. ✅ **Coverage report** - Uploads coverage report as artifact

#### Continuous Deployment (CD)

The CD pipeline triggers on version tags (e.g., `v1.0.0`, `v1.5.0`):
- Trains model with 100% of available data (all 11 features)
- Creates GitHub Release with trained model and metadata
- Makes model available for automatic download by Streamlit app

## 📚 Documentation

- [Environment Setup Guide](./docs/1_environment_setup.md)
- [Contribution Guide](./docs/2_contribution_guide.md)
- [Project Architecture](./docs/3_project_architecture.md)
- [Model Deployment Guide](./docs/4_model_deployment.md)

## 👥 Team

Project developed by students of the PO-235 - Data Science Project course.

## 📄 License

This project is under the MIT license. See the [LICENSE](./LICENSE) file for more details.
