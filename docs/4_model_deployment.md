# Model Deployment Guide

This guide explains how to deploy new model versions using the automated CD pipeline and GitHub Releases.

## Overview

The project uses an automated Continuous Deployment (CD) pipeline that:
1. Trains the model with 100% of available data
2. Creates a GitHub Release with the trained model
3. Makes the model automatically available to the Streamlit application

**Trigger:** Git tags following semantic versioning (`v*.*.*`)

---

## Quick Start

To deploy a new model version:

```bash
# 1. Ensure you're on main branch and it's up to date
git checkout main
git pull

# 2. Create a version tag
git tag v1.5.0

# 3. Push the tag to trigger CD pipeline
git push origin v1.5.0
```

That's it! The CD pipeline will automatically:
- ✅ Train the model with current code
- ✅ Create a GitHub Release
- ✅ Upload model artifacts (`.pkl` + `model_metadata.json`)
- ✅ Make it available for download

---

## Semantic Versioning

Tags must follow semantic versioning format: `vMAJOR.MINOR.PATCH`

### Format: `vX.Y.Z`

- **`X` (MAJOR)**: Breaking changes or major model architecture updates
  - Example: `v1.0.0` → `v2.0.0` (switched from 6 to 11 features)
  
- **`Y` (MINOR)**: New features or improvements (backward compatible)
  - Example: `v1.4.0` → `v1.5.0` (improved preprocessing)
  
- **`Z` (PATCH)**: Bug fixes or small tweaks
  - Example: `v1.5.0` → `v1.5.1` (fixed validation bug)

### Examples:

```bash
git tag v1.0.0   # First stable release
git tag v1.1.0   # Added new feature
git tag v1.1.1   # Fixed a bug
git tag v2.0.0   # Breaking change (architecture update)
```

---

## CD Pipeline Details

### What Happens When You Push a Tag:

1. **Environment Setup**
   - Installs Python 3.11 and UV
   - Installs project dependencies

2. **Model Training**
   - Runs `entrypoints/train.py`
   - Uses 100% of data (no test split by default)
   - Trains with all 11 features
   - Generates model file and metadata

3. **Artifact Preparation**
   - Converts `.joblib` to `.pkl` (for compatibility)
   - Prepares `model_metadata.json` with:
     - Training timestamp
     - Dataset information
     - Feature list
     - Performance metrics (if test split used)

4. **GitHub Release Creation**
   - Creates a new release with your tag
   - Uploads model artifacts
   - Generates release notes automatically

5. **Model Availability**
   - Model is available at: `https://github.com/camposdojoao/po-235/releases/download/v1.5.0/random_forest_model.pkl`
   - Streamlit app downloads it automatically via `ModelLoader`

### Viewing Pipeline Status:

Go to: **GitHub → Actions → CD - Model Release**

You'll see:
- ✅ Pipeline running/completed
- 📊 Training logs
- 📦 Uploaded artifacts
- ⏱️ Execution time

---

## GitHub Releases

### What is a GitHub Release?

A GitHub Release is a packaged version of your project at a specific point in time. It:
- Packages code with a specific tag/version
- Attaches binary files (like trained models)
- Provides download links
- Documents changes and release notes

### Accessing Releases:

**Repository → Releases** or visit:
```
https://github.com/camposdojoao/po-235/releases
```

Each release contains:
- 📦 **Source code** (zip/tar.gz)
- 🤖 **Model file** (`random_forest_model.pkl`)
- 📊 **Metadata** (`model_metadata.json`)
- 📝 **Release notes** (auto-generated)

---

## Important Rules

### ⚠️ DO NOT Reuse Tags

**Never push a tag that already exists:**

```bash
# ❌ WRONG - Tag v1.0.0 already exists
git tag v1.0.0
git push origin v1.0.0
# Error: tag 'v1.0.0' already exists
```

**Why?** 
- GitHub doesn't allow duplicate tags
- Creates confusion about which model is which
- Pipeline will fail

**Solution:**
- Always increment the version
- Check existing tags first: `git tag -l`

### Deleting a Tag (if needed):

```bash
# Delete locally
git tag -d v1.5.0

# Delete remotely (use with caution!)
git push origin --delete v1.5.0
```

⚠️ **Warning:** Deleting tags in production is not recommended. Only do this for mistakes before release.

---

## Common Workflows

### Deploying a Bug Fix:

```bash
# Fix the bug in code
git commit -m "fix: correct preprocessing validation"
git push

# Create patch version
git tag v1.4.1
git push origin v1.4.1
```

### Deploying a New Feature:

```bash
# Add the feature
git commit -m "feat: add new feature importance analysis"
git push

# Create minor version
git tag v1.5.0
git push origin v1.5.0
```

### Deploying Breaking Changes:

```bash
# Make breaking changes
git commit -m "feat!: change from 11 to 15 features"
git push

# Create major version
git tag v2.0.0
git push origin v2.0.0
```

---

## Using a Specific Model Version

### In Streamlit App:

The app automatically uses the latest release by default. To use a specific version, set the `MODEL_VERSION` environment variable:

**Locally:**
```bash
export MODEL_VERSION=v1.4.0
make streamlit
```

**In Streamlit Cloud:**
Set in `Secrets` or `Environment Variables`:
```
MODEL_VERSION=v1.4.0
```

### Downloading Manually:

```bash
# Download specific version
wget https://github.com/camposdojoao/po-235/releases/download/v1.5.0/random_forest_model.pkl

# Load in Python
import joblib
model = joblib.load('random_forest_model.pkl')
```

---

## Troubleshooting

### Pipeline Failed?

**Check:**
1. Go to **Actions → CD - Model Release → [Your workflow]**
2. Review error logs
3. Common issues:
   - Code errors in `train.py`
   - Dependency issues
   - Data file problems

**Fix:**
1. Fix the issue in code
2. Create a new tag (increment version)
3. Push again

### Model Not Loading in Streamlit?

**Check:**
1. Release was created successfully
2. Files were uploaded (`random_forest_model.pkl` present)
3. `MODEL_VERSION` env var (if set) matches an existing tag
4. Clear `.model_cache/` and restart app

### Tag Already Exists?

**Solution:**
```bash
# Check existing tags
git tag -l

# Use next available version
git tag v1.5.1  # instead of v1.5.0
git push origin v1.5.1
```

---

## Best Practices

1. ✅ **Test Locally First**
   - Run `make run-ci` before tagging
   - Ensure tests pass

2. ✅ **Meaningful Versions**
   - Use semantic versioning correctly
   - Document changes in commit messages

3. ✅ **Tag from Main**
   - Always tag from `main` branch
   - Ensure main is up to date

4. ✅ **Review Pipeline**
   - Wait for pipeline to complete
   - Check release was created successfully

5. ✅ **Monitor Performance**
   - Review `model_metadata.json` in release
   - Compare with previous versions

6. ❌ **Never Delete Production Tags**
   - Keep version history intact
   - Use new versions instead

---

## Summary

**To deploy a new model:**

```bash
git checkout main && git pull
git tag v1.x.x
git push origin v1.x.x
```

**Pipeline does the rest:**
- Trains model
- Creates release
- Deploys automatically

**Simple, automated, and reliable!** 🚀

---

## Need Help?

- **View releases**: [GitHub Releases](https://github.com/camposdojoao/po-235/releases)
- **Check pipeline**: [GitHub Actions](https://github.com/camposdojoao/po-235/actions)
- **Read more**:
  - [Contribution Guide](./2_contribution_guide.md)
  - [Project Architecture](./3_project_architecture.md)

