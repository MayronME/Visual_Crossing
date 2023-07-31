# Visual Crossing

## Objetivo
O projeto tem como objetivo realizar a extração de dados climáticos do site [Visual Crossing](https://www.visualcrossing.com/) e disponibilizá-los no POWER BI, com o propósito de aprendizado. Para a implementação, optei por utilizar a nuvem da AWS, mais especificamente o serviço EC2, e também empreguei as ferramentas Terraform e Ansible para facilitar o gerenciamento e a automação do ambiente.
## Execução
#### Configuração do Terraform
### Criando um ssh
- crie uma pasta **key**:  ```mkdir AWS/key/```
- crie a chave ssh: ```ssh-keygen -t rsa /AWS/key/xadia_acess```
### Configurando acesso a AWS CLI
- [Passo a Passo da configuração](https://www.treinaweb.com.br/blog/como-instalar-e-configurar-o-aws-cli)

### Configurando o Terraform

- [Instalação Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) versão utilizar: 1.5.4

- Entre na pasta ```cd AWS/Terraform```
- Crie o arquivo ```touch terraform.tfvars```
- E adicione as seguintes variaveis de configuração da zona,maquina e chave ssh
- <img src="https://user-images.githubusercontent.com/84480805/257296571-42ef1bd0-2a3a-4220-9f43-e233ded9f3da.png"/> 
-  Execute o comando ```terraform init``` 
> **Nota:** **certifique-se** de estar na pasta Terraform **antes de executar** o terraform init

Agora os serviços na AWS estão funcionando
