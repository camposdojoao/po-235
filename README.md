# Wine Quality Prediction

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

</div>

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte da disciplina **PO-235 - Projeto de Ciência de Dados**, ministrada pelo **Professor Filipe Verri**. O objetivo é criar um modelo de machine learning capaz de prever a qualidade de vinhos com base em suas características.

Utilizando o dataset [Wine Quality](https://archive.ics.uci.edu/dataset/186/wine+quality) da UCI Machine Learning Repository, este projeto explora técnicas de classificação para avaliar vinhos tintos e brancos da região do Vinho Verde em Portugal.

## 🎯 Objetivos

- Desenvolver um modelo de classificação para prever a qualidade de vinhos
- Analisar a importância de características físico-químicas na qualidade do vinho
- Implementar boas práticas de engenharia de software em projetos de ciência de dados
- Criar uma interface interativa para visualização e predição

## 📊 Dataset

O projeto utiliza o **Wine Quality Dataset** disponibilizado pela UCI Machine Learning Repository:

- **Fonte**: [UCI Wine Quality Dataset](https://archive.ics.uci.edu/dataset/186/wine+quality)
- **Instâncias**: 4.898 amostras (1.599 vinhos tintos + 4.898 vinhos brancos)
- **Características**: 11 variáveis físico-químicas
- **Target**: Qualidade do vinho (score de 0 a 10)

### Variáveis do Dataset

| Variável              | Descrição                 |
|-----------------------|---------------------------|
| fixed_acidity         | Acidez fixa               |
| volatile_acidity      | Acidez volátil            |
| citric_acid           | Ácido cítrico             |
| residual_sugar        | Açúcar residual           |
| chlorides             | Cloretos                  |
| free_sulfur_dioxide   | Dióxido de enxofre livre  |
| total_sulfur_dioxide  | Dióxido de enxofre total  |
| density               | Densidade                 |
| pH                    | pH                        |
| sulphates             | Sulfatos                  |
| alcohol               | Teor alcoólico            |
| quality               | Qualidade (variável alvo) |

## 🤖 Metodologia

### Modelo Utilizado

O projeto utiliza o algoritmo **Random Forest** para classificação da qualidade de vinhos:

- **Random Forest** ✅ 
  - Modelo robusto e interpretável
  - Excelente desempenho em dados tabulares
  - Resistente a overfitting
  - Fornece importância das features

Durante o desenvolvimento inicial, outros algoritmos (XGBoost e Gradient Boosting) foram avaliados, mas o **Random Forest** foi escolhido como modelo final após análise comparativa de performance, métricas de avaliação e interpretabilidade.

### Abordagem

1. **Análise Exploratória de Dados (EDA)**: Compreensão das distribuições e correlações
2. **Pré-processamento**: Tratamento de dados, feature engineering
3. **Treinamento de Modelos**: Experimentação com diferentes algoritmos
4. **Avaliação**: Comparação de métricas (acurácia, precisão, recall, F1-score)
5. **Otimização**: Tuning de hiperparâmetros do modelo selecionado
6. **Deploy**: Interface web interativa com Streamlit

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**: Linguagem principal do projeto
- **scikit-learn**: Implementação do Random Forest e pipeline de ML
- **pandas & numpy**: Manipulação e análise de dados
- **matplotlib & seaborn**: Visualização de dados
- **Streamlit**: Interface web interativa
- **UV**: Gerenciador de pacotes Python
- **Pyenv**: Gerenciador de versões Python
- **pytest**: Framework de testes
- **GitHub Actions**: CI/CD pipeline

## 📁 Estrutura do Projeto

```
po-235/
├── 📂 configs/           # Arquivos de configuração
├── 📂 docs/              # Documentação do projeto
│   ├── 1_como_configurar_ambiente.md
│   ├── 2_como_contribuir_com_o_projeto.md
│   └── 3_arquitetura_do_projeto.md
├── 📂 entrypoints/       # Scripts principais (treinamento, predição, deploy)
├── 📂 model/             # Modelos treinados e artefatos
├── 📂 src/               # Dados e código fonte
│   ├── winequality-red.csv
│   ├── winequality-white.csv
│   └── winequality.names
├── 📂 streamlit/         # Interface web
├── 📂 tests/             # Testes automatizados
├── 📜 Makefile           # Comandos de automação
├── 📜 README.md          # Este arquivo
└── 📜 LICENSE            # Licença do projeto
```

Para mais detalhes sobre a arquitetura, consulte [`docs/3_arquitetura_do_projeto.md`](./docs/3_arquitetura_do_projeto.md).

## 🚀 Como Começar

### Pré-requisitos

- Sistema operacional Linux (ou WSL no Windows)
- Git instalado
- Acesso à internet para download de dependências

### Instalação e Configuração

Para configurar o ambiente de desenvolvimento completo, siga o guia detalhado em [`docs/1_como_configurar_ambiente.md`](./docs/1_como_configurar_ambiente.md).

**Resumo dos passos:**

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/camposdojoao/po-235.git
   cd po-235
   ```

2. **Configurar ambiente**
   ```bash
   make install-uv
   make install-dev
   ```

3. **Executar a aplicação Streamlit**
   ```bash
   make streamlit
   ```

## 🤝 Como Contribuir

Este projeto segue boas práticas de desenvolvimento colaborativo com Git Flow simplificado. Para contribuir:

1. Atualize a branch `master`
2. Crie uma branch seguindo o padrão `feature/*` ou `fix/*`
3. Desenvolva e teste suas alterações
4. Faça commit com mensagens descritivas
5. Crie um Pull Request

Para instruções detalhadas, consulte [`docs/2_como_contribuir_com_o_projeto.md`](./docs/2_como_contribuir_com_o_projeto.md).

### Pipeline de CI/CD

O projeto possui uma pipeline automatizada que valida:
- ✅ Testes unitários
- ✅ Linting (padrões de código)
- ✅ Nomenclatura de branches

## 📚 Documentação

- [Como Configurar o Ambiente](./docs/1_como_configurar_ambiente.md)
- [Como Contribuir com o Projeto](./docs/2_como_contribuir_com_o_projeto.md)
- [Arquitetura do Projeto](./docs/3_arquitetura_do_projeto.md)

## 👥 Equipe

Projeto desenvolvido por estudantes da disciplina PO-235 - Projeto de Ciência de Dados.

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.
