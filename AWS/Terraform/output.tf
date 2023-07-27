output "IP_public" {
  value = aws_instance.mysql_instance.public_ip
}