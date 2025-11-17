"""Module for loading models from GitHub Releases."""

import os
from pathlib import Path

import joblib
import requests
import streamlit as st
from sklearn.base import BaseEstimator


class ModelLoader:
    """Class for managing download and caching of models from GitHub Releases."""

    def __init__(
        self,
        repo_owner: str = "camposdojoao",
        repo_name: str = "po-235",
        model_version: str | None = None,
    ) -> None:
        """
        Initialize the ModelLoader.

        Args:
            repo_owner: GitHub repository owner name.
            repo_name: GitHub repository name.
            model_version: Version of the model to load (release tag).
                If None, automatically fetches the latest release.
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name

        # Se versão não foi especificada, busca a última release
        if model_version is None:
            self.model_version = self._get_latest_release()
        else:
            self.model_version = model_version

        self.cache_dir = Path(".model_cache")
        self.cache_dir.mkdir(exist_ok=True)

    def _get_latest_release(self) -> str:
        """
        Fetch the tag of the latest release on GitHub.

        Returns:
            Tag of the latest release (e.g., 'v1.0.0').

        Raises:
            Exception: If there is an error fetching the release.
        """
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            latest_tag = response.json()["tag_name"]
            return latest_tag
        except requests.exceptions.RequestException as e:
            # If it fails, use default version
            st.warning(
                f"⚠️ Unable to fetch the latest release. "
                f"Using default version v1.0.0.\nError: {str(e)}"
            )
            return "v1.0.0"
        except KeyError:
            st.warning("⚠️ No release found. Using default version v1.0.0.")
            return "v1.0.0"

    def _get_model_url(self, model_filename: str) -> str:
        """
        Construct the URL for downloading the model from GitHub Releases.

        Args:
            model_filename: Model filename.

        Returns:
            Complete URL for downloading the model.
        """
        return (
            f"https://github.com/{self.repo_owner}/{self.repo_name}/"
            f"releases/download/{self.model_version}/{model_filename}"
        )

    def _download_model(self, model_filename: str, cache_path: Path) -> None:
        """
        Download the model from GitHub Releases.

        Args:
            model_filename: Model filename.
            cache_path: Local path where the model will be saved.

        Raises:
            Exception: If there is an error during download.
        """
        url = self._get_model_url(model_filename)

        try:
            with st.spinner(f"Downloading model {self.model_version}..."):
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                with cache_path.open("wb") as f:
                    f.write(response.content)

                st.success(f"✓ Model {self.model_version} downloaded successfully!")
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Error downloading model: {str(e)}\n"
                f"Check if release {self.model_version} exists on GitHub."
            ) from e

    @st.cache_resource
    def load_model(
        _self,  # noqa: N805
        model_filename: str = "random_forest_model.pkl",
    ) -> BaseEstimator:
        """
        Load the model from local cache or download from GitHub Releases.

        Args:
            model_filename: Model filename.

        Returns:
            Loaded model ready for inference.

        Raises:
            Exception: If there is an error loading the model.
        """
        cache_path = _self.cache_dir / f"{model_filename}_{_self.model_version}"

        # If model is not in cache, download it
        if not cache_path.exists():
            _self._download_model(model_filename, cache_path)

        # Load model from cache
        try:
            model = joblib.load(cache_path)
            return model
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}") from e


def get_model_version() -> str | None:
    """
    Get the model version from an environment variable.

    Allows configuring the model version via the MODEL_VERSION
    environment variable, useful for Streamlit Cloud deployments.

    If the variable is not set, returns None to automatically fetch
    the latest release.

    Returns:
        Model version (e.g., 'v1.0.0') or None to fetch automatically.
    """
    return os.getenv("MODEL_VERSION", None)
