# Providers
provider "aws" {
  region = var.regiao_aws  # região 
}

# Recurso EC2
resource "aws_instance" "mysql_instance" {
  ami           = var.ami
  instance_type = var.instancia  # Free tier
  key_name = element(split("/",var.chave),2)

  tags = {
    Name = "MySQL Instance"
  }
    # Recurso de segurança
  security_groups = [aws_security_group.mysql_security_group.name, aws_security_group.allow_ssh.name]
}

resource "aws_key_pair" "chaveSSH" {
  key_name = element(split("/",var.chave),2)
  public_key = file("${var.chave}.pub")
}

# Recurso de grupo de segurança portas mysql
resource "aws_security_group" "mysql_security_group" {
  name        = "mysql_security_group"
  description = "Allow MySQL traffic"

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Recurso de grupo de segurança portas ssh
resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}