# Projeto de PO-235

Este documento irá apresentar um passo a passo estabelecendo padrões de contribuição para o projeto. Os padrões de contribuição envolvem boas práticas relacionadas à versionamento e sobre nossa pipeline de CI/CD. Esta documentação já considera que o ambiente está configurado e o repositório clonado.

## <pensar_em_um_titulo>

Primeiramente, vamos nos certificar que branch master está atualizada. Para isso, execute o seguinte comando no seu terminal:

```
git pull
```


Esse comando irá atualizar a sua branch master de acordo com a branch master remota, garantindo que o seu repositório está atualizado de acordo com a última versão publicada.

### Criação de branch

Com a master atualizada, podemos criar nossa branch e trabalhar em nossa task. Seguindo as boas práticas de desenvolvimento, vamos criar uma branch por task desenvolvida. 

1. As branches seguirão uma organização simples usando prefixos _feature/_ e _fix/_. Se sua branch adicionar uma funcionalidade nova, ela deverá ter o prefixo _feature/_, caso sua branch faça uma correção ou exclusão de alguma funcionalidade, ela deverá ter o prefixo _fix/_. 

2. Para criar uma branch, vamos usar como referência o nome da sua task. Por exemplo:

    <p>
    <img src="./img/task_img.png" alt="Task" title="Versão 1.2" width="500">
    </p>

    Essa task diz respeito à criação da documentação do código, então o nome dela será `feature/documentacao-do-codigo`. Dito isso, para criar uma branch (usando essa como exemplo), esse seria o comando:


    ```
    git checkout -b "feature/documentacao-do-codigo"
    ```

    Esse comando retornará os seguinte:
    <p>
    <img src="./img/criacao_de_branch.png" alt="Task" title="Versão 1.2" width="500">
    </p>

    Após criar a branch, você está apto a desenvolver sua task livremente.

    ⚠️ _OBS: Se certifique de atualizar o nome da branch para o seu respectivo caso._

### Commit

Quando terminar sua task, seja desenvolvendo novas funcionalidade ou corrigindo já existentes, após testar o código para ter certeza que está tudo funcionando corretamente, devemos fazer o commit dessas alterações. Para isso, siga os seguintes passos:

1. Verifique os arquivos que foram adicionados/alterados no seu repositório através do comando abaixo:
    ```
    git status
    ```
    Esse comando irá retornar todos os arquivos que foram adicionados/alterados por você na sua branch. Algo assim será retornado:
    <p>
    <img src="./img/git_status.png" alt="Task" title="Versão 1.2" width="500">
    </p>

  

 