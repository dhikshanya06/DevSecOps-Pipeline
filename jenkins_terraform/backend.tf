terraform {
  backend "s3" {
    bucket = "dhikshanya-k"
    key    = "Jenkins/terraform.tfstate"
    region = "us-east-1"
  }
}

