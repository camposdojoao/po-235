# Projeto de PO-235

## Como configurar o ambiente

Para trabalharmos de forma padronizada e controlada, vamos trabalhar usando Linux. Primeiramente, vamos seguir com a instalação do WSL (Windows Subsystem for Linux). Esse passo só é necessário caso sua máquina seja Windows, se for linux não é necessário. 

### 1. WSL
É necessário instalar a extensão WSL dentro do VSCode, que pode ser feita na aba de extensões no canto esquerdo da IDLE e procurar o nome da extensão.
Após isso, para instalar o WSL, vá até o PowerShell (tecla de atalho do windows + S: PowerShell) e digite o seguinte comando:

```
wsl --install -d Ubuntu-22.04
```

Ao rodar esse comando, será instalado o WSL com a distribuição Ubuntu na versão 22.04. Caso seja solicitado um UNIX user e password, preencha livremente.

**1.1 Instalar o Git com o Winget**

1.  **Abra o Terminal no VSCode:**

      * Vá no menu superior `Terminal > New Terminal` ou use o atalho `Ctrl + '` (a tecla de crase).
      * Certifique-se de que o terminal aberto seja o **PowerShell** (geralmente é o padrão).

2.  **Verifique se o Winget está funcionando:**
    Digite o comando abaixo e aperte Enter. Você deve ver uma lista de opções do Winget.

    ```powershell
    winget --version
    ```

4.  **Instale o Git:**
    Agora, execute o comando de instalação. Ele vai baixar e instalar o Git para você automaticamente.

    ```powershell
    winget install --id Git.Git -e --source winget
    ```

      * `winget install`: O comando para instalar.
      * `--id Git.Git`: O identificador exato do pacote que queremos.
      * `-e`: Significa "exact", para garantir que estamos instalando o pacote com esse ID exato.
      * `--source winget`: Diz para usar o repositório principal de pacotes da comunidade do Winget.

5.  **Feche e Reabra o VSCode (Importante\!):**
    Após a instalação ser concluída, feche completamente o VSCode e abra-o novamente. Isso é crucial para que o VSCode (e seu terminal) reconheça que o Git agora está instalado e disponível no sistema.

6.  **Verifique a Instalação:**
    Abra um novo terminal no VSCode e digite:

    ```powershell
    git --version
    ```

### 2. Repositório

Abra sua IDE (VS Code, Cursor etc). Caso não tenha uma IDE instalada, a IDE recomendada é o VS Code. Siga até o link abaixo e faça o download e instalação: [VS Code](https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user)

⚠️ **Observação:** Ao instalar a IDE, se certifique que a opção "Adicione em PATH" estará marcada.

Com o VS Code disponível, depois de abrí-lo, aperte a tecla F1 e procure:

```
WSL: Connect to WSL using Distro...
```

E selecione a distro que acabamos de instalar, _**Ubuntu 22.04**_. Ao fazer isso, o seu VS Code estará "dentro" dessa distro. É isto que queremos.

Com isto feito, podemos clonar o repositório. Abra o terminal do VS Code e digite:

```
git clone https://github.com/camposdojoao/po-235.git
```

Este comando irá clonar o repositório dentro da sua distribuição linux. Caso você não seja redirecionado à pasta do repositório, vá em "File", depois em "Open Folder" e selecione a pasta do projeto: "_**PO-235**_". Pronto, você está dentro do repositório.

Depois de clonar o repositório, configure suas credenciais para fazer commits. Execute esses dois comandos:

```
git config --global user.email "seu@email.com"
```

```
git config --global user.name "seu_nome"
```

### 3. Ambiente

Com o repositório instalado, iremos prosseguir com a configuração do ambiente. Para isso, vamos utilizar o _**UV**_. _**UV**_ é um gerenciador de pacotes para Python. Com ele conseguimos controlar as bibliotecas que usaremos e as versões dessas bibliotecas.



Para instalar o UV, abra o terminal do VS Code e execute este comando:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Caso tenha o erro _**curl: (60) SSL certificate problem: unable to get local issuer certificate**_, entre em contato com o João para resolver :D.
Com o UV instalado, vamos instalar pacotes básicos no nosso WSL. Esses pacotes vão ser necessários para instalar o Python e os nossos comandos do Makefile. No seu terminal, execute:

```
sudo apt update
```

```
sudo apt install gcc build-essential make zlib1g zlib1g-dev openssl libssl-dev libbz2-dev libsqlite3-dev libffi-dev  libreadline-dev libncursesw5-dev tk-dev liblzma-dev
```

Agora, vamos instalar um gerenciador de versões Python, o _**Pyenv**_. Execute este comando no terminal:

```
curl https://pyenv.run | bash
```

Com o Pyenv instalado, vamos adicionar as variáveis de ambiente. Execute o seguinte comando (esse comando irá abrir um editor de texto no terminal):

```
nano ~/.bashrc
```

Com o editor aberto, vá até o final do editor de texto (com a tecla "seta para baixo") e cole esses paths:

```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PATH="$PYENV_ROOT/shims:$PATH"
eval "$(pyenv init -)"
export PATH="$HOME/.local/bin:$PATH"
```
Depois de colar, aperte _**Ctrl+X**_, _**Y**_ e depois aperte _**Enter**_.

Depois de fazer isso, cole este comando no terminal para aplicar as alterações:

```
source ~/.bashrc
```

Com isso feito, vamos instalar a versão do Python (essa parte pode demorar uns minutinhos):

```
pyenv install 3.13.7
```
