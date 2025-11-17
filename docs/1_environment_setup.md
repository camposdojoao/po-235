# PO-235 Project

## Environment Setup Guide

To work in a standardized and controlled manner, we will use Linux. First, we'll proceed with the installation of WSL (Windows Subsystem for Linux). This step is only necessary if your machine runs Windows; if you're already on Linux, skip it.

### 1. WSL (Windows Subsystem for Linux)

To install WSL, open PowerShell (Windows key + S: PowerShell) and run the following command:

```bash
wsl --install -d Ubuntu-22.04
```

This command will install WSL with the Ubuntu 22.04 distribution. If prompted for a UNIX user and password, fill them in freely.

### 2. Repository

Open your IDE (VS Code, Cursor, etc.). If you don't have an IDE installed, the recommended one is VS Code. Follow the link below to download and install it: [VS Code](https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user)

⚠️ **Note:** When installing the IDE, make sure the "Add to PATH" option is checked.

With VS Code available, after opening it, press F1 and search for:

```
WSL: Connect to WSL using Distro...
```

Select the distribution we just installed, **Ubuntu 22.04**. By doing this, your VS Code will be "inside" this distribution. This is what we want.

With this done, we can clone the repository. Open the VS Code terminal and type:

```bash
git clone https://github.com/camposdojoao/po-235.git
```

This command will clone the repository inside your Linux distribution. If you're not redirected to the repository folder, go to "File", then "Open Folder" and select the project folder: **PO-235**. Done, you're inside the repository.

After cloning the repository, configure your credentials to make commits. Run these two commands:

```bash
git config --global user.email "your@email.com"
git config --global user.name "your_name"
```

### 3. Environment Setup

With the repository installed, we'll proceed with environment configuration. For this, we'll use **UV**. **UV** is an extremely fast Python package manager and environment manager written in Rust. With UV, we can control Python versions, libraries, and their dependencies.

#### 3.1 Install UV

To install UV, open the VS Code terminal and run this command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If you get the error **curl: (60) SSL certificate problem: unable to get local issuer certificate**, contact the project team for assistance.

After installation, add UV to your PATH by running:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### 3.2 Install System Dependencies

Install basic packages needed for the project. In your terminal, execute:

```bash
sudo apt update
```

```bash
sudo apt install make
```

This installs `make` which is used to run Makefile commands.

#### 3.3 Install Python 3.11 with UV

UV can install and manage Python versions directly. Install Python 3.11:

```bash
uv python install 3.11
```

This command downloads and installs Python 3.11. UV will automatically use this version for the project.

#### 3.4 Install Project Dependencies

Now, install all project dependencies:

```bash
uv sync
```

This command will:
- Create a virtual environment automatically
- Install all dependencies defined in `pyproject.toml`
- Lock dependencies in `uv.lock` for reproducibility

**That's it!** Your environment is ready to use. UV handles everything: Python version, virtual environment, and dependencies.

### 4. Running the Application

To run the Streamlit application locally:

```bash
make streamlit
```

Or alternatively:

```bash
uv run streamlit run entrypoints/st_app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

### 5. Running Tests

To run the automated tests:

```bash
make test
```

Or alternatively:

```bash
uv run pytest tests/
```

### 6. Code Quality Checks

To run linting and formatting checks:

```bash
make check
```

This will run:
- Code linting with automatic fixes (`ruff check --fix`)
- Code formatting validation (`ruff format --check`)

To automatically format all code:

```bash
make format
```

### 7. CI Simulation

To simulate the entire CI pipeline locally before pushing:

```bash
make run-ci
```

This command runs:
1. ✅ Code quality checks (`make check`)
2. ✅ Full test suite with coverage (`make test-ci`)

This is useful to catch issues before creating a PR, ensuring your changes will pass the CI pipeline.

### Available Make Commands

**Environment Setup:**
- `make install-uv` - Install UV package manager
- `make install` - Install project dependencies (uv lock + sync)

**Development:**
- `make streamlit` - Run the Streamlit application locally
- `make tests` - Run tests with detailed coverage report
- `make test-ci` - Run tests in CI mode (shorter output)

**Code Quality:**
- `make check` - Run linting and format checks (with auto-fix)
- `make format` - Auto-format all code with ruff

**CI/CD:**
- `make run-ci` - Simulate the complete CI pipeline locally

For more details, check the `Makefile` in the project root.

## Troubleshooting

### UV Installation Issues

If you encounter SSL certificate errors during UV installation, you may need to:
1. Check your internet connection
2. Verify proxy settings
3. Contact the project team for assistance

### Python Version Issues

If `pyenv install 3.11` fails, ensure all required system packages are installed:

```bash
sudo apt update
sudo apt upgrade
```

Then try the installation again.

### Permission Issues

If you encounter permission errors, ensure you're running commands with appropriate privileges:
- Use `sudo` only for system-wide installations
- Regular commands should run without `sudo`

## Next Steps

After setting up your environment:
1. Read the [Contribution Guide](./2_contribution_guide.md)
2. Explore the [Project Architecture](./3_project_architecture.md)
3. Start contributing to the project!

