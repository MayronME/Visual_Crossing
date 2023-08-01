
# Objetivo

O objetivo deste projeto é realizar a extração de dados climáticos do site [Visual Crossing](https://www.visualcrossing.com/) e disponibilizá-los no POWER BI, com o propósito de aprendizado. Para a implementação, foi escolhido utilizar a nuvem da AWS, mais especificamente o serviço EC2, e também empreguei as ferramentas Terraform e Ansible para facilitar o gerenciamento e a automação do ambiente.

# Execução

## Criando conta e chave da API no Visual Crossing

Para começar, é necessário gerar uma API key no Visual Crossing. [Aqui](https://www.visualcrossing.com/resources/documentation/weather-api/how-to-change-your-visual-crossing-weather-api-key/) estão as instruções de como fazer isso.

## Criando uma chave SSH

1. Crie uma pasta **key**:
   ```
   mkdir AWS/key/
   ```

2. Crie a chave SSH:
   ```
   ssh-keygen -t rsa -f /AWS/key/xadia_acess
   ```

> **AVISO**: Caso mude o caminho ou o nome da **chave SSH**, lembre-se de alterar nos seguintes arquivos:
>
> - */AWS/ansible.cfg* >> **variável private_key_file**
> - */Terraform/terraform.tfvars* >> **variável chave**

## Configurando acesso à AWS CLI

Para configurar o acesso à AWS CLI, siga este [Passo a Passo da configuração da AWS CLI](https://www.treinaweb.com.br/blog/como-instalar-e-configurar-o-aws-cli).

## Configurando o Terraform

1. [Instale o Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli). A versão utilizada é a 1.5.4.

2. Entre na pasta **```cd AWS/Terraform```**

3. Crie o arquivo:
   ```
   touch terraform.tfvars
   ```

4. Adicione as seguintes variáveis de configuração da zona, máquina e chave SSH:

   ```
   # Variáveis para o Terraform
   instancia= "sua_maquina_escolhida"
   regiao_aws = "sua_zona_escolhida"
   chave = "/AWS/key/xadia_acess"
   ami = "sua_ami_escolhida
   ```

   ![Imagem das variáveis do Terraform](https://user-images.githubusercontent.com/84480805/257296571-42ef1bd0-2a3a-4220-9f43-e233ded9f3da.png)

5. Execute o comando:
   ```
   terraform init
   ```

> **Nota**: **Certifique-se** de estar na pasta Terraform **antes de executar** o comando `terraform init`.

6. Faça a configuração do Terraform:
   ```
   terraform apply -auto-approve
   ```

> **Nota**: Serão criados 4 serviços na AWS EC2.

## Configurando o Ansible

1. [Instale o Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). A versão utilizada é a core 2.15.2.

2. Na pasta **Ansible**, acesse o arquivo **config.ini** e coloque o IP da máquina que é disponibilizado após a execução do Terraform.

   ![Imagem do arquivo config.ini do Ansible](https://user-images.githubusercontent.com/84480805/257586033-69f6a946-eb4b-4409-a4dc-38acd0f5f0cc.PNG)

3. Acesse a pasta Ansible no terminal:
   ```
   cd /AWS/Ansible
   ```

4. ### Criação do Ansible Vault

   Execute na pasta **Ansible** o comando:
   ```
   ansible-vault create vault.yml
   ```

   Dentro do arquivo **vault.yml**, insira as seguintes variáveis:
   ```
   api_key: "sua_chave_api_do_Visual_Crossing"
   ```

   ![Imagem do arquivo vault.yml do Ansible](https://user-images.githubusercontent.com/84480805/257610802-33a23a48-f47b-453e-b306-28148a5b83fb.png)

   > **Nota**: A variável `api_key` é a **chave** disponibilizada pelo site [Visual Crossing](#criando-conta-e-chave-da-api--visual-crossing).

   Caso haja dúvidas de como usar o Ansible Vault, acesse [este link](https://www.redhat.com/sysadmin/introduction-ansible-vault).

5. ### Executando o Ansible

   Dentro da pasta **ansible**, execute:
   ```
   ansible-playbook playbook.yml --ask-vault-pass
   ```

   Serão feitas **16** alterações dentro da máquina na AWS.

## Configurando código para execução diária

Acesse a máquina e configure o **[crontab](https://acervolima.com/agendamento-de-scripts-python-no-linux/)**
