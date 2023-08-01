

# Objetivo
O projeto tem como objetivo realizar a extração de dados climáticos do site [Visual Crossing](https://www.visualcrossing.com/) e disponibilizá-los no POWER BI, com o propósito de aprendizado. Para a implementação, optei por utilizar a nuvem da AWS, mais especificamente o serviço EC2, e também empreguei as ferramentas Terraform e Ansible para facilitar o gerenciamento e a automação do ambiente.
# Execução
## Criando conta e chave da API | Visual Crossing
- [Como gerar API key no Visual Crossing](https://www.visualcrossing.com/resources/documentation/weather-api/how-to-change-your-visual-crossing-weather-api-key/)
## Criando um ssh
- crie uma pasta **key**:  ```mkdir AWS/key/```
- crie a chave ssh: ```ssh-keygen -t rsa /AWS/key/xadia_acess```
## Configurando acesso a AWS CLI
- [Passo a Passo da configuração  da AWS CLI](https://www.treinaweb.com.br/blog/como-instalar-e-configurar-o-aws-cli)

## Configurando o Terraform

- [Instalação Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) **|** versão utilizada: 1.5.4

- Entre na pasta ```cd AWS/Terraform```
- Crie o arquivo ```touch terraform.tfvars```
- E adicione as seguintes variaveis de configuração da zona,maquina e chave ssh
- <img src="https://user-images.githubusercontent.com/84480805/257296571-42ef1bd0-2a3a-4220-9f43-e233ded9f3da.png"/> 
-  Execute o comando ```terraform init``` 
> **Nota:** **certifique-se** de estar na pasta Terraform **antes de executar** o terraform init
- Execute o comando ``` terraform apply -autoa-pprove``` 
Serão criado 4 serviços na AWS EC2

## Configurando Ansible
- [Instalação Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) **|** versão utilizada: core 2.15.2
- Na pasta **Ansible** acesse o arquivo **config.ini** e coloque o IP da maquina que é disponibilizado após execução do Terraform
- <img src="https://user-images.githubusercontent.com/84480805/257586033-69f6a946-eb4b-4409-a4dc-38acd0f5f0cc.PNG"/>
- Acesse a pasta Ansible no cmd ``` cd /AWS/Ansible```
  - ### Criação do Ansible Vault
  - execute na pasta **Ansible** o comando ``ansible-vault create vault.yml``
  - Dentro do arquivo **vault.yml** insira as seguintes variaveis
  - <img src="https://user-images.githubusercontent.com/84480805/257593044-021e31c5-8c02-46ff-80fe-be63238e7d14.png"/>
>**Nota:** A variavel api_key é a **chave** disponibilizada pelo site [Visual Crossing](#criando-conta-e-chave-da-api--visual-crossing)
>>  Caso haja duvidas de como usar o Ansible Vault: [Acesse aqui](https://www.redhat.com/sysadmin/introduction-ansible-vault)

- ### Executando Ansible
- Dentro da pasta **ansible** execute no cmd ``ansible-playbook playbook.yml --ask-vault-pass``
