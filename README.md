# Projeto de PO-235

## Como configurar o ambiente

Para trabalharmos de forma padronizada e controlada, vamos trabalhar usando Linux. Primeiramente, vamos seguir com a instalação do WSL (Windows Subsystem for Linux). Esse passo só é necessário caso sua máquina seja Windows, se for linux não é necessário. 

### 1. WSL
Para instalar o WSL, vá até o PowerShell (tecla de atalho do windows + S: PowerShell) e digite o seguinte comando:

``` wsl --install -d Ubuntu-22.04 ```

Ao rodar esse comando, será instalado o WSL com a distribuição Ubuntu na versão 22.04. Caso seja solicitado um UNIX user e password, preencha livremente.

### 2. Repositório

Abra sua IDE (VS Code, Cursor etc). Caso não tenha uma IDE instalada, a IDE recomendada é o VS Code. Siga até o link abaixo e faça o download e instalação: [VS Code](https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user)

⚠️ **Observação:** Ao instalar a IDE, se certifique que a opção "Adicione em PATH" estará marcada.

Com o VS Code disponível, depois de abrí-lo, aperte a tecla F1 e procure:

``` WSL: Connect to WSL using Distro...```

E selecione a distro que acabamos de instalar, _**Ubuntu 22.04**_. Ao fazer isso, o seu VS Code estará "dentro" dessa distro. É isto que queremos.

Com isto feito, podemos clonar o repositório. Abra o terminal do VS Code e digite:

```git clone https://github.com/camposdojoao/po-235.git```

Este comando irá clonar o repositório dentro da sua distribuição linux. Caso você não seja redirecionado à pasta do repositório, vá em "File", depois em "Open Folder" e selecione a pasta do projeto: "_**PO-235**_". Pronto, você está dentro do repositório.

Depois de clonar o repositório, configure suas credenciais para fazer commits. Execute esses dois comandos:

```git config --global user.email "seu@email.com"```

```git config --global user.name "seu_nome"```