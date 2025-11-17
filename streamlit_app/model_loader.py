"""Módulo para carregamento de modelos do GitHub Releases."""

import os
from pathlib import Path

import joblib
import requests
import streamlit as st
from sklearn.base import BaseEstimator


class ModelLoader:
    """Classe para gerenciar download e cache de modelos do GitHub Releases."""

    def __init__(
        self,
        repo_owner: str = "camposdojoao",
        repo_name: str = "po-235",
        model_version: str | None = None,
    ) -> None:
        """
        Inicializa o ModelLoader.

        Args:
            repo_owner: Nome do dono do repositório GitHub.
            repo_name: Nome do repositório GitHub.
            model_version: Versão do modelo a ser carregada (tag da release).
                Se None, busca automaticamente a última release.
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
        Busca a tag da última release no GitHub.

        Returns:
            Tag da última release (ex: 'v1.0.0').

        Raises:
            Exception: Se houver erro ao buscar a release.
        """
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            latest_tag = response.json()["tag_name"]
            return latest_tag
        except requests.exceptions.RequestException as e:
            # Se falhar, usa versão padrão
            st.warning(
                f"⚠️ Não foi possível buscar a última release. "
                f"Usando versão padrão v1.0.0.\nErro: {str(e)}"
            )
            return "v1.0.0"
        except KeyError:
            st.warning("⚠️ Nenhuma release encontrada. Usando versão padrão v1.0.0.")
            return "v1.0.0"

    def _get_model_url(self, model_filename: str) -> str:
        """
        Constrói a URL para download do modelo do GitHub Releases.

        Args:
            model_filename: Nome do arquivo do modelo.

        Returns:
            URL completa para download do modelo.
        """
        return (
            f"https://github.com/{self.repo_owner}/{self.repo_name}/"
            f"releases/download/{self.model_version}/{model_filename}"
        )

    def _download_model(self, model_filename: str, cache_path: Path) -> None:
        """
        Faz download do modelo do GitHub Releases.

        Args:
            model_filename: Nome do arquivo do modelo.
            cache_path: Caminho local onde o modelo será salvo.

        Raises:
            Exception: Se houver erro no download.
        """
        url = self._get_model_url(model_filename)

        try:
            with st.spinner(f"Baixando modelo {self.model_version}..."):
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                with cache_path.open("wb") as f:
                    f.write(response.content)

                st.success(f"✓ Modelo {self.model_version} baixado com sucesso!")
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Erro ao baixar modelo: {str(e)}\n"
                f"Verifique se a release {self.model_version} existe no GitHub."
            ) from e

    @st.cache_resource
    def load_model(
        _self,  # noqa: N805
        model_filename: str = "random_forest_model.pkl",
    ) -> BaseEstimator:
        """
        Carrega o modelo do cache local ou baixa do GitHub Releases.

        Args:
            model_filename: Nome do arquivo do modelo.

        Returns:
            Modelo carregado e pronto para inferência.

        Raises:
            Exception: Se houver erro ao carregar o modelo.
        """
        cache_path = _self.cache_dir / f"{model_filename}_{_self.model_version}"

        # Se o modelo não está em cache, faz download
        if not cache_path.exists():
            _self._download_model(model_filename, cache_path)

        # Carrega o modelo do cache
        try:
            model = joblib.load(cache_path)
            return model
        except Exception as e:
            raise Exception(f"Erro ao carregar modelo: {str(e)}") from e


def get_model_version() -> str | None:
    """
    Obtém a versão do modelo a partir de variável de ambiente.

    Permite configurar a versão do modelo via variável de ambiente
    MODEL_VERSION, útil para deploys no Streamlit Cloud.

    Se a variável não estiver definida, retorna None para buscar
    automaticamente a última release.

    Returns:
        Versão do modelo (ex: 'v1.0.0') ou None para buscar automaticamente.
    """
    return os.getenv("MODEL_VERSION", None)
