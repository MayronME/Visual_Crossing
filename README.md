# Visual Crossing

## Objetivo
O projeto tem como objetivo realizar a extração de dados climáticos do site [Visual Crossing](https://www.visualcrossing.com/) e disponibilizá-los no POWER BI, com o propósito de aprendizado. Para a implementação, optei por utilizar a nuvem da AWS, mais especificamente o serviço EC2, e também empreguei as ferramentas Terraform e Ansible para facilitar o gerenciamento e a automação do ambiente.
## Execução
Para fazer a execução do código será necessários

#### Configuração do Terraform
- [Instalação Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) versão utilizar: 1.5.4

- Entre na pasta AWS/Terraform/
<div aling="center">
<img src="https://github.com/MayronME/Visual_Crossing/issues/1#issue-1829689143"/>
</div>
- Crie o arquivo terraform.tfvars

-  e aplique o comando 'terraform init'
