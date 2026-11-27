# Pre-Requisitos

Para aproveitar ao máximo das seções técnicas das aulas o aluno deve instalar as ferramentas descritas neste documento.   

> **DISCLAIMER**: O passo a passo foi gerado por IA sob revisão humana.  

> **IMPORTANTE**: Verifique o tipo de processador de seu computador antes de instalar qualquer um dos softwares de prerequisitos se é INTEL/AMD ou ARM. Todo o material foi desenvolvido no sistema operacional Windows, se esta usando o MAC ou Linux pode haver diferenças em alguns comandos e recursos.  

## Tutorial de Instalação de Ambiente de Desenvolvimento Data Science

Este tutorial fornece instruções detalhadas para instalação e configuração de um ambiente completo de desenvolvimento para projetos de Data Science e Machine Learning em sistemas operacionais Windows, macOS e Ubuntu Linux.  

---  

## 1. Visual Studio Code

### Descrição

Visual Studio Code é um editor de código-fonte leve, extensível e integrado com IA, que oferece suporte para depuração, controle de versão Git integrado e extensões para praticamente qualquer linguagem de programação. [\[code.visua...studio.com\]](https://code.visualstudio.com/download), [\[code.visua...studio.com\]](https://code.visualstudio.com/Docs)

**Documentação Oficial:** <https://code.visualstudio.com/docs>

**Link de Download:** <https://code.visualstudio.com/download>

### Instalação no Windows

1.  Acesse o site oficial de download do Visual Studio Code. [\[code.visua...studio.com\]](https://code.visualstudio.com/download)
2.  Baixe o instalador User Installer x64 para Windows 10 ou 11. [\[code.visua...studio.com\]](https://code.visualstudio.com/download), [\[code.visua...studio.com\]](https://code.visualstudio.com/download)
3.  Execute o arquivo de instalação baixado (VSCodeUserSetup-x64-{version}.exe).
4.  Aceite os termos de licença.
5.  Selecione o diretório de instalação.
6.  Marque as opções recomendadas:
    *   Adicionar ao PATH
    *   Criar ícone na área de trabalho
    *   Adicionar ação "Abrir com Code" ao menu de contexto
7.  Clique em Instalar e aguarde a conclusão.
8.  Marque a opção "Executar Visual Studio Code" e clique em Concluir.

### Instalação no macOS

1.  Acesse <https://code.visualstudio.com/download>
2.  Baixe o arquivo .zip apropriado:
    *   Universal: para compatibilidade com Intel e Apple Silicon [\[code.visua...studio.com\]](https://code.visualstudio.com/download)
    *   Apple Silicon: para chips M1/M2/M3
    *   Intel chip: para processadores Intel
3.  Abra o arquivo .zip baixado.
4.  Arraste o Visual Studio Code.app para a pasta Applications.
5.  Abra o Visual Studio Code a partir da pasta Applications.

### Instalação no Ubuntu

1.  Abra o terminal.
2.  Atualize o índice de pacotes:

```bash
sudo apt update
```

3.  Instale o Visual Studio Code usando o pacote .deb:

```bash
wget -O vscode.deb 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'
sudo apt install ./vscode.deb
```

**Alternativa via Snap:**

```bash
sudo snap install --classic code
```

4.  Execute o Visual Studio Code:

```bash
code
```

---  

## 2. Python 3.12+

### Descrição

Python é uma linguagem de programação de alto nível, interpretada e de propósito geral, conhecida por sua simplicidade, legibilidade e amplo suporte a bibliotecas para desenvolvimento de aplicações, ciência de dados e aprendizado de máquina. [\[python.org\]](https://www.python.org/downloads/?keys=python%203.12%20windows)

**Documentação Oficial:** <https://docs.python.org/3/>

**Link de Download:** <https://www.python.org/downloads/>

### Instalação no Windows

1.  Acesse <https://www.python.org/downloads/> e baixe a versão mais recente do Python 3.12 ou superior. [\[python.org\]](https://www.python.org/downloads/?keys=python%203.12%20windows), [\[python.org\]](https://www.python.org/downloads/?keys=python%203.12%20windows)
2.  Execute o instalador baixado (python-3.12.x-amd64.exe).
3.  **IMPORTANTE:** Marque a opção "Add Python to PATH" na primeira tela.
4.  Clique em "Install Now" para instalação padrão ou "Customize installation" para opções avançadas.
5.  Aguarde a conclusão da instalação.
6.  Verifique a instalação abrindo o PowerShell e executando:

```powershell
python --version
```

### Instalação no macOS

1.  Acesse <https://www.python.org/downloads/> e baixe o instalador para macOS. [\[python.org\]](https://www.python.org/downloads/?keys=python%203.12%20windows)
2.  Abra o arquivo .pkg baixado.
3.  Siga o assistente de instalação, aceitando os termos de licença.
4.  Aguarde a conclusão da instalação.
5.  Verifique a instalação abrindo o Terminal e executando:

```bash
python3 --version
```

### Instalação no Ubuntu

1.  Atualize o índice de pacotes:

```bash
sudo apt update
```

2.  Instale Python 3.12 e ferramentas relacionadas:

```bash
sudo apt install python3.12 python3.12-venv python3-pip
```

3.  Verifique a instalação:

```bash
python3.12 --version
```

4.  Configure Python 3.12 como padrão (opcional):

```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
```

---  

## 3. Uv (Python Package Manager)

### Descrição

Uv é um gerenciador de pacotes e projetos Python extremamente rápido, escrito em Rust. Desenvolvido pela Astral (criadores do Ruff), o Uv oferece velocidade de 10-100x superior ao pip e substitui múltiplas ferramentas como pip, pip-tools, pipx, poetry, pyenv, virtualenv e outras. [\[docs.astral.sh\]](https://docs.astral.sh/uv/guides/install-python/)

**Documentação Oficial:** <https://docs.astral.sh/uv/>

**Repositório GitHub:** <https://github.com/astral-sh/uv>

### Instalação no Windows

1.  Abra o PowerShell e execute o comando de instalação:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

2.  Após a instalação, feche e reabra o PowerShell.
3.  Verifique a instalação:

```powershell
uv --version
```

4.  Instale o Python automaticamente via Uv (opcional):

```powershell
uv python install
```

### Instalação no macOS

1.  Abra o Terminal e execute:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2.  Adicione o Uv ao PATH editando o arquivo de configuração do shell:

```bash
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

3.  Verifique a instalação:

```bash
uv --version
```

### Instalação no Ubuntu

1.  Abra o terminal e execute:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2.  Adicione o Uv ao PATH:

```bash
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

3.  Verifique a instalação:

```bash
uv --version
```

### Uso Básico do Uv

```bash
# Instalar Python
uv python install 3.12

# Criar ambiente virtual
uv venv

# Instalar pacotes
uv pip install numpy pandas

# Instalar de requirements.txt
uv pip install -r requirements.txt
```

---  

## 4. WSL2 (Windows Subsystem for Linux)

### Descrição

WSL2 (Windows Subsystem for Linux 2) é uma camada de compatibilidade que permite executar um ambiente Linux completo diretamente no Windows, sem a necessidade de máquinas virtuais tradicionais ou configuração de dual boot. [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/windows/wsl/install)

**Documentação Oficial:** <https://learn.microsoft.com/en-us/windows/wsl/>

**Nota:** Disponível apenas para Windows. Usuários de macOS e Linux não precisam instalar esta ferramenta.

### Requisitos do Sistema

*   Windows 10 versão 2004 (Build 19041) ou superior [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/windows/wsl/install)
*   Windows 11 (qualquer versão)
*   Processador de 64 bits com suporte a virtualização
*   Mínimo de 4GB de RAM

### Instalação no Windows

1.  Abra o PowerShell como Administrador (clique com botão direito e selecione "Executar como administrador").

2.  Execute o comando de instalação:

```powershell
wsl --install
```

Este comando habilitará os recursos necessários e instalará a distribuição Ubuntu por padrão. [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/windows/wsl/install), [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/windows/wsl/install)

3.  Reinicie o computador quando solicitado.

4.  Após a reinicialização, o Ubuntu será iniciado automaticamente. Aguarde a conclusão da instalação.

5.  Crie um nome de usuário e senha para o ambiente Linux quando solicitado.

### Verificação da Instalação

```powershell
wsl --version
```

Para verificar as distribuições instaladas:

```powershell
wsl --list --verbose
```

### Instalando Distribuições Alternativas

Para visualizar distribuições disponíveis:

```powershell
wsl --list --online
```

Para instalar uma distribuição específica:

```powershell
wsl --install -d Debian
```

### Atualizando o WSL

```powershell
wsl --update
```

---  

## 5. Docker e Rancher Desktop

### Descrição do Docker Desktop

Docker Desktop é uma plataforma de desenvolvimento que permite construir, compartilhar e executar aplicações containerizadas. Oferece interface gráfica intuitiva para gerenciar containers, imagens e recursos Docker. [\[docs.docker.com\]](https://docs.docker.com/desktop/setup/install/windows-install/)

**Documentação Oficial:** <https://docs.docker.com/desktop/>

**Link de Download:** <https://www.docker.com/products/docker-desktop/>

### Descrição do Rancher Desktop

Rancher Desktop é uma aplicação open-source que fornece todos os recursos essenciais para trabalhar com containers e Kubernetes no desktop, oferecendo uma alternativa ao Docker Desktop.

**Documentação Oficial:** <https://docs.rancherdesktop.io/>

**Link de Download:** <https://rancherdesktop.io/>

---  

### Opção A: Docker Desktop

#### Instalação no Windows

**Requisitos:**

*   WSL 2 versão 2.1.5 ou superior [\[docs.docker.com\]](https://docs.docker.com/desktop/setup/install/windows-install/)
*   Windows 10 64-bit: versão 22H2 (build 19045) ou superior
*   Windows 11 64-bit: versão 23H2 (build 22631) ou superior [\[docs.docker.com\]](https://docs.docker.com/desktop/setup/install/windows-install/)
*   4GB de RAM
*   Virtualização habilitada na BIOS/UEFI

**Passos:**

1.  Certifique-se de que o WSL2 está instalado e atualizado:

```powershell
wsl --update
```

2.  Baixe o Docker Desktop para Windows em <https://www.docker.com/products/docker-desktop/>

3.  Execute o instalador Docker Desktop Installer.exe.

4.  Durante a instalação, certifique-se de que a opção "Use WSL 2 instead of Hyper-V" está marcada.

5.  Siga o assistente de instalação e aguarde a conclusão.

6.  Após a instalação, inicie o Docker Desktop.

7.  Aceite os termos de serviço.

8.  Aguarde o Docker inicializar completamente.

9.  Verifique a instalação no PowerShell:

```powershell
docker --version
docker run hello-world
```

#### Instalação no macOS

1.  Baixe o Docker Desktop para macOS em <https://www.docker.com/products/docker-desktop/>

2.  Escolha a versão apropriada:
    *   Apple Silicon (M1/M2/M3)
    *   Intel chip

3.  Abra o arquivo .dmg baixado.

4.  Arraste o ícone do Docker para a pasta Applications.

5.  Abra o Docker Desktop a partir da pasta Applications.

6.  Autorize as permissões necessárias quando solicitado.

7.  Aguarde a inicialização do Docker.

8.  Verifique a instalação no Terminal:

```bash
docker --version
docker run hello-world
```

#### Instalação no Ubuntu

1.  Atualize o índice de pacotes:

```bash
sudo apt update
```

2.  Instale dependências:

```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

3.  Adicione a chave GPG oficial do Docker:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

4.  Adicione o repositório do Docker:

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5.  Instale o Docker Desktop:

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

6.  Inicie e habilite o serviço Docker:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

7.  Adicione seu usuário ao grupo docker:

```bash
sudo usermod -aG docker $USER
```

8.  Reinicie a sessão ou execute:

```bash
newgrp docker
```

9.  Verifique a instalação:

```bash
docker --version
docker run hello-world
```

---  

### Opção B: Rancher Desktop

#### Instalação no Windows

1.  Baixe o Rancher Desktop para Windows em <https://rancherdesktop.io/>

2.  Execute o instalador Rancher.Desktop.Setup.exe.

3.  Siga o assistente de instalação.

4.  Escolha o runtime de container:
    *   dockerd (Docker)
    *   containerd

5.  Configure a versão do Kubernetes desejada.

6.  Aguarde a conclusão da instalação e inicialização.

7.  Verifique a instalação no PowerShell:

```powershell
docker --version
kubectl version --client
```

#### Instalação no macOS

1.  Baixe o Rancher Desktop para macOS em <https://rancherdesktop.io/>

2.  Escolha a versão apropriada (Intel ou Apple Silicon).

3.  Abra o arquivo .dmg baixado.

4.  Arraste o Rancher Desktop para a pasta Applications.

5.  Abra o Rancher Desktop.

6.  Configure o runtime de container e versão do Kubernetes.

7.  Verifique a instalação:

```bash
docker --version
kubectl version --client
```

#### Instalação no Ubuntu

1.  Baixe o arquivo .deb ou AppImage em <https://rancherdesktop.io/>

2.  Para instalação via .deb:

```bash
sudo apt install ./rancher-desktop-<version>-amd64.deb
```

3.  Ou execute o AppImage:

```bash
chmod +x Rancher.Desktop-<version>.AppImage
./Rancher.Desktop-<version>.AppImage
```

4.  Configure o runtime e Kubernetes conforme necessário.

5.  Verifique a instalação:

```bash
docker --version
kubectl version --client
```

---  

## 6. Git

### Descrição

Git é um sistema de controle de versão distribuído amplamente utilizado para rastrear mudanças no código-fonte durante o desenvolvimento de software. É essencial para colaboração em equipe e gerenciamento de projetos. [\[git-scm.com\]](https://git-scm.com/install/windows)

**Documentação Oficial:** <https://git-scm.com/doc>

**Link de Download:** <https://git-scm.com/downloads>

### Instalação no Windows

1.  Acesse <https://git-scm.com/download/win> e baixe o instalador mais recente. [\[git-scm.com\]](https://git-scm.com/install/windows), [\[git-scm.com\]](https://git-scm.com/install/windows)

2.  Execute o arquivo Git-{version}-64-bit.exe.

3.  Siga o assistente de instalação com as seguintes recomendações:
    *   Editor padrão: Selecione Visual Studio Code ou seu editor preferido
    *   Ajuste da variável PATH: "Git from the command line and also from 3rd-party software"
    *   SSH executable: "Use bundled OpenSSH"
    *   HTTPS transport backend: "Use the OpenSSL library"
    *   Line ending conversions: "Checkout Windows-style, commit Unix-style line endings"
    *   Terminal emulator: "Use MinTTY"
    *   Default behavior of git pull: "Default (fast-forward or merge)"

4.  Conclua a instalação.

5.  Verifique a instalação no PowerShell:

```powershell
git --version
```

### Instalação no macOS

**Opção 1: Via Homebrew (recomendado)**

```bash
brew install git
```

**Opção 2: Via instalador oficial**

1.  Acesse <https://git-scm.com/download/mac>
2.  Baixe o instalador .dmg
3.  Abra o arquivo e siga as instruções
4.  Verifique a instalação:

```bash
git --version
```

### Instalação no Ubuntu

1.  Atualize o índice de pacotes:

```bash
sudo apt update
```

2.  Instale o Git:

```bash
sudo apt install git
```

3.  Verifique a instalação:

```bash
git --version
```

### Configuração Inicial do Git

Após a instalação, configure seu nome de usuário e e-mail (obrigatório):

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

Verifique as configurações:

```bash
git config --list
```

Configurações adicionais recomendadas:

```bash
# Editor padrão
git config --global core.editor "code --wait"

# Branch padrão
git config --global init.defaultBranch main

# Habilitar cores
git config --global color.ui auto
```

---  

## 7. DVC (Data Version Control)

### Descrição

DVC (Data Version Control) é uma ferramenta de linha de comando que auxilia no desenvolvimento de projetos de Machine Learning reproduzíveis. Funciona como o Git, mas para dados e modelos, permitindo versionamento de datasets grandes e rastreamento de experimentos. [\[doc.dvc.org\]](https://doc.dvc.org/user-guide/data-management/remote-storage), [\[doc.dvc.org\]](https://doc.dvc.org/user-guide/data-management/remote-storage)

**Documentação Oficial:** <https://dvc.org/doc>

**Repositório GitHub:** <https://github.com/iterative/dvc>

### Instalação no Windows

1.  Abra o PowerShell e execute:

```powershell
pip install dvc
```

**Alternativa com Uv:**

```powershell
uv pip install dvc
```

2.  Para suporte a armazenamento remoto específico, instale extras:

```powershell
# Amazon S3
pip install "dvc[s3]"

# Azure Blob Storage
pip install "dvc[azure]"

# Google Cloud Storage
pip install "dvc[gs]"

# Google Drive
pip install "dvc[gdrive]"

# Todos os extras
pip install "dvc[all]"
```

3.  Verifique a instalação:

```powershell
dvc version
```

### Instalação no macOS

1.  Abra o Terminal e execute:

```bash
pip3 install dvc
```

**Alternativa via Homebrew:**

```bash
brew install dvc
```

2.  Para extras de armazenamento:

```bash
pip3 install "dvc[s3,azure,gs]"
```

3.  Verifique a instalação:

```bash
dvc version
```

### Instalação no Ubuntu

1.  Instale via pip:

```bash
pip3 install dvc
```

2.  Para extras:

```bash
pip3 install "dvc[s3,azure,gs]"
```

3.  Verifique a instalação:

```bash
dvc version
```

### Configuração Inicial do DVC

1.  Navegue até o diretório do seu projeto Git:

```bash
cd /caminho/do/seu/projeto
```

2.  Inicialize o DVC:

```bash
dvc init
```

3.  Configure um remote storage (exemplo com diretório local):

```bash
dvc remote add -d myremote /tmp/dvcstore
```

**Exemplos de configuração com cloud providers:**

**Amazon S3:**

```bash
dvc remote add -d myremote s3://mybucket/path
dvc remote modify myremote region us-west-2
```

**Azure Blob Storage:**

```bash
dvc remote add -d myremote azure://mycontainer/path
```

**Google Cloud Storage:**

```bash
dvc remote add -d myremote gs://mybucket/path
```

**Google Drive:**

```bash
dvc remote add -d myremote gdrive://folder-id
```

4.  Adicione dados ao DVC:

```bash
dvc add data/dataset.csv
git add data/dataset.csv.dvc data/.gitignore
git commit -m "Add dataset to DVC"
```

5.  Envie dados para o remote:

```bash
dvc push
```

6.  Para baixar dados do remote:

```bash
dvc pull
```

### Comandos Essenciais do DVC

| Comando          | Descrição                            |
| ---------------- | ------------------------------------ |
| `dvc init`       | Inicializa DVC no repositório        |
| `dvc add <file>` | Adiciona arquivo/diretório ao DVC    |
| `dvc remote add` | Configura armazenamento remoto       |
| `dvc push`       | Envia dados para o remote            |
| `dvc pull`       | Baixa dados do remote                |
| `dvc status`     | Verifica status dos dados            |
| `dvc checkout`   | Restaura versão específica dos dados |

---  

## 8. Criação de Conta no GitHub

### Descrição

GitHub é a maior plataforma de hospedagem de código-fonte e colaboração para desenvolvedores, construída sobre o Git. Permite armazenar repositórios, colaborar em projetos e gerenciar código com controle de versão.【0†L1】

**Site Oficial:** <https://github.com>

**Documentação:** <https://docs.github.com>

### Passo a Passo para Criar Conta

1.  Acesse <https://github.com> no seu navegador.

2.  Clique no botão "Sign up" no canto superior direito.【0†L1】

3.  Preencha as informações solicitadas:
    *   **Email**: Digite seu endereço de e-mail
    *   **Password**: Crie uma senha forte (mínimo 15 caracteres OU mínimo 8 caracteres incluindo um número e uma letra minúscula)
    *   **Username**: Escolha um nome de usuário único (apenas caracteres alfanuméricos ou hífens)

4.  Complete o desafio de verificação para confirmar que você não é um robô.

5.  Clique em "Create account".

6.  Verifique seu e-mail. O GitHub enviará um código de verificação.

7.  Digite o código de verificação recebido por e-mail.

8.  Personalize sua experiência (opcional):
    *   Selecione suas áreas de interesse
    *   Indique seu nível de experiência
    *   Escolha como pretende usar o GitHub

9.  Escolha o plano:
    *   **Free**: Repositórios públicos e privados ilimitados
    *   **Pro/Team/Enterprise**: Recursos avançados (opcional)

10. Complete o cadastro clicando em "Complete setup".

### Configuração Inicial da Conta GitHub

Após criar a conta, configure o Git local para usar suas credenciais do GitHub:

```bash
git config --global user.name "seu-username-github"
git config --global user.email "seu-email@github.com"
```

### Autenticação via SSH (Recomendado)

1.  Gere uma chave SSH:

```bash
ssh-keygen -t ed25519 -C "seu-email@github.com"
```

2.  Pressione Enter para aceitar o local padrão.

3.  Digite uma senha segura (opcional mas recomendado).

4.  Adicione a chave ao ssh-agent:

**Windows (PowerShell):**

```powershell
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
ssh-add ~/.ssh/id_ed25519
```

**macOS/Linux:**

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

5.  Copie a chave pública:

**Windows:**

```powershell
cat ~/.ssh/id_ed25519.pub | clip
```

**macOS:**

```bash
pbcopy < ~/.ssh/id_ed25519.pub
```

**Linux:**

```bash
cat ~/.ssh/id_ed25519.pub
```

6.  Adicione a chave no GitHub:
    *   Acesse <https://github.com/settings/keys>
    *   Clique em "New SSH key"
    *   Cole a chave pública no campo "Key"
    *   Adicione um título descritivo
    *   Clique em "Add SSH key"

7.  Teste a conexão:

```bash
ssh -T git@github.com
```

Você deverá ver uma mensagem de boas-vindas confirmando a autenticação.

### Autenticação via Token (Alternativa)

1.  Acesse <https://github.com/settings/tokens>

2.  Clique em "Generate new token" > "Generate new token (classic)"

3.  Configure o token:
    *   Nome: Descreva o propósito
    *   Expiration: Escolha a validade
    *   Scopes: Selecione "repo" para acesso completo aos repositórios

4.  Clique em "Generate token"

5.  Copie o token gerado (não será possível visualizá-lo novamente)

6.  Use o token como senha ao fazer push/pull via HTTPS

---  

## Verificação Final do Ambiente

Execute os seguintes comandos para verificar se todas as ferramentas foram instaladas corretamente:

```bash
# Visual Studio Code
code --version

# Python
python --version

# Uv
uv --version

# WSL2 (apenas Windows)
wsl --version

# Docker ou Rancher
docker --version

# Git
git --version

# DVC
dvc version
```

---  

## Resumo de Links Importantes

| Ferramenta         | Documentação                               | Download                                          |
| ------------------ | ------------------------------------------ | ------------------------------------------------- |
| Visual Studio Code | <https://code.visualstudio.com/docs>       | <https://code.visualstudio.com/download>          |
| Python             | <https://docs.python.org/3/>               | <https://www.python.org/downloads/>               |
| Uv                 | <https://docs.astral.sh/uv/>               | <https://github.com/astral-sh/uv>                 |
| WSL2               | <https://learn.microsoft.com/windows/wsl/> | Instalado via comando                             |
| Docker Desktop     | <https://docs.docker.com/desktop/>         | <https://www.docker.com/products/docker-desktop/> |
| Rancher Desktop    | <https://docs.rancherdesktop.io/>          | <https://rancherdesktop.io/>                      |
| Git                | <https://git-scm.com/doc>                  | <https://git-scm.com/downloads>                   |
| DVC                | <https://dvc.org/doc>                      | Instalado via pip                                 |
| GitHub             | <https://docs.github.com>                  | <https://github.com>                              |

---  
