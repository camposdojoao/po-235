# Arquitetura do Projeto PO-235

Este documento apresenta a arquitetura e estrutura organizacional do projeto de PO-235, detalhando a finalidade de cada diretório e como os componentes do projeto estão organizados.

## Visão Geral

O projeto PO-235 é uma aplicação de ciência de dados focada na análise e predição de qualidade de vinhos utilizando técnicas de machine learning. O projeto foi estruturado seguindo boas práticas de engenharia de software, separando responsabilidades em diferentes camadas e módulos.

## Estrutura de Diretórios

```
po-235/
├── 📂 configs/
├── 📂 docs/
├── 📂 entrypoints/
├── 📂 model/
├── 📂 src/
├── 📂 streamlit/
├── 📂 tests/
├── 📜 LICENSE
├── 📜 Makefile
└── 📜 README.md
```

## Descrição dos Diretórios

### 📁 `configs/`

**Propósito:** Armazenar arquivos de configuração do projeto.

Este diretório é destinado a centralizar todas as configurações necessárias para o funcionamento da aplicação, por exemplo:

- Configurações de modelos de machine learning (hiperparâmetros)
- Configurações de conexão com bases de dados
- Variáveis de ambiente
- Parâmetros de execução de pipelines
- Configurações de logging e monitoramento

**Exemplo de uso:**
```
configs/
├── model_config.yaml
├── database_config.yaml
└── pipeline_config.json
```

### 📁 `docs/`

**Propósito:** Documentação do projeto.

Contém toda a documentação técnica e de usuário do projeto, incluindo:

- **1_como_configurar_ambiente.md**: Guia completo de configuração do ambiente de desenvolvimento
- **2_como_contribuir_com_o_projeto.md**: Padrões e boas práticas para contribuição no projeto
- **3_arquitetura_do_projeto.md**: Documentação da arquitetura (este documento)
- **img/**: Pasta com imagens e capturas de tela utilizadas na documentação

**Boas práticas:**
- Manter a documentação atualizada conforme o projeto evolui
- Incluir diagramas e exemplos quando necessário
- Usar nomenclatura padronizada para os arquivos

### 📁 `entrypoints/`

**Propósito:** Pontos de entrada da aplicação.

Este diretório irá conter os scripts principais que inicializam diferentes componentes da aplicação, por exemplo:

- Scripts de treinamento de modelos
- Scripts de inferência/predição
- Scripts de ETL (Extract, Transform, Load)
- Executáveis de pipelines de dados
- Scripts de automação e deployment
- Scripts de deploy do Streamlit

**Exemplo de estrutura:**
```
entrypoints/
├── train_model.py
├── predict.py
├── etl_pipeline.py
├── streamlit_app.py
└── deploy.py
```

**Características:**
- Scripts devem ser independentes e executáveis
- Cada entrypoint deve ter responsabilidade única e bem definida
- Possibilita futura integração com ferramentas de orquestração (Airflow, Prefect, etc.)

### 📁 `model/`

**Propósito:** Armazenar modelos de machine learning treinados.

Diretório dedicado a guardar os artefatos de modelos de machine learning, por exemplo:

- Modelos treinados (formato .pkl, .joblib, .h5, etc.)
- Pesos de redes neurais
- Versões de modelos

**Exemplo de estrutura:**
```
📁 model/
    ├── ⚙️ wine_quality_model_v1.pkl
    └── ⚙️ wine_quality_model_v2.pkl
```

**Boas práticas:**
- Usar versionamento de modelos
- Incluir metadados sobre performance e data de treinamento
- Considerar uso de ferramentas como MLflow para gerenciamento de modelos

### 📁 `src/`

**Propósito:** Armazenamento de dados.

Este diretório contém os dados utilizados no projeto:

**Dados atuais:**
- **winequality-red.csv**: Dataset com características físico-químicas de vinhos tintos
- **winequality-white.csv**: Dataset com características físico-químicas de vinhos brancos
- **winequality.names**: Documentação e metadados dos datasets

**Possível estrutura de código:**
```
📁 src/
│   ├── 🧾 winequality-red.csv
│   ├── 🧾 winequality-white.csv
│   └── 🧾 winequality.names
```

**Características:**
- Centraliza lógica de negócio reutilizável
- Módulos devem ser importáveis pelos entrypoints
- Código deve ser modular e seguir princípios SOLID

### 📁 `streamlit/`

**Propósito:** Interface de usuário web com Streamlit.

Diretório dedicado aos arquivos da aplicação web interativa construída com Streamlit:

- Páginas da aplicação
- Interação com o modelo
- Dashboard de métricas

**Exemplo de estrutura:**
```
📁 streamlit/
    ├── 📁 pages/
    │       ├── 1_predict.py
    │       ├── 2_analysis.py
    │       └── 3_model_info.py
    └── 📁 components/
            ├── sidebar.py
            └── charts.py
```

**Uso:**
```bash
make streamlit
```

### 📁 `tests/`

**Propósito:** Testes automatizados do projeto.

Poderá conter todos os testes unitários que serão implementados no projeto, por exemplo:

- Testes de funções de preprocessamento
- Testes de pipelines de dados
- Testes de modelos (performance, formato)
- Testes de base de dados
- Testes de entrypoints

**Exemplo de estrutura:**
```
tests/
├── __init__.py
├── test_preprocessing.py
├── test_models.py
├── test_pipeline.py
└── conftest.py
```

**Boas práticas:**
- Usar pytest como framework de testes
- Manter cobertura de testes acima de 60%
- Executar testes automaticamente na pipeline de CI/CD

## Arquivos na Raiz do Projeto

### 📄 `Makefile`

Arquivo de automação com comandos facilitadores para tarefas comuns, por exemplo:

- **install-uv**: Instala o gerenciador de pacotes UV
- **install-dev**: Instala dependências do projeto
- **streamlit**: Inicializa a aplicação Streamlit localmente

**Uso:**
```bash
make install-dev
```

**Benefícios:**
- Padroniza comandos entre desenvolvedores
- Simplifica tarefas complexas em comandos simples
- Documenta processos de build e deployment

### 📄 `README.md`

Documentação principal e ponto de entrada para novos desenvolvedores. Contém:

- Visão geral do projeto
- Instruções de configuração inicial
- Links para documentação detalhada

### 📄 `LICENSE`

Arquivo de licença do projeto, definindo os termos de uso e distribuição do código.

## Pipeline de CI/CD

O projeto utiliza uma pipeline de CI/CD que é acionada automaticamente ao criar um Pull Request. A pipeline executa:

1. **Testes Unitários**: Valida funcionamento das funções
2. **Linting**: Verifica padrões de código
3. **Validação de Branch**: Confirma nomenclatura correta (feature/* ou fix/*)

## Fluxo de Trabalho

### 1. Desenvolvimento

```
git pull → create branch → desenvolvimento → teste de novas funcionalidades → git commit → git push 
```

### 2. Experimentação

```
experimentação no repositório ou fora do repositório → validação → seguir etapas de desenvolvimento
```

### 3. Deploy

```
code in entrypoints/ → config in configs/ → run CD pipeline → serve via streamlit/
```

## Tecnologias Utilizadas

- **Python 3.11**: Linguagem principal
- **UV**: Gerenciador de pacotes e ambientes
- **Pyenv**: Gerenciador de versões Python
- **Github**: Controle de versão
- **Streamlit**: Framework para interface web
- **Pytest**: Framework de testes (implícito pela estrutura)

## Boas Práticas

### Organização de Código

1. **Separação de Responsabilidades**: Cada diretório tem um propósito claro e específico
2. **Modularidade**: Cada arquivo possui responsabilidade única e bem definida, facilitando manutenção, debug e evolução do projeto
3. **Testabilidade**: Estrutura facilita criação e execução de testes

### Versionamento

1. **Branch Naming**: Usar prefixos `feature/` ou `fix/`
2. **Commits**: Mensagens claras e descritivas
3. **Pull Requests**: Revisar código antes de mergear

### Documentação

1. Manter documentação atualizada
2. Documentar decisões arquiteturais
3. Incluir exemplos e diagramas quando necessário

### Para trabalhar no projeto:

1. Configure o ambiente seguindo o documento [1_como_configurar_ambiente.md](./1_como_configurar_ambiente.md)
2. Entenda o fluxo de contribuição em [2_como_contribuir_com_o_projeto.md](./2_como_contribuir_com_o_projeto.md)
3. Explore a estrutura de pastas conforme sua task
4. Desenvolva seguindo as boas práticas descritas

## Contato e Suporte

Para dúvidas sobre a arquitetura ou sugestões de melhorias, entre em contato com o time do projeto.

