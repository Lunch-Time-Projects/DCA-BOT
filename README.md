# DCA-BOT

Lunch project

## Prerequisite

- docker installation: https://docs.docker.com/get-docker/
- Terraform installation: https://learn.hashicorp.com/tutorials/terraform/install-cli

## Credential setups

### AWS

- get your credential: https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html
- add your credential to your local aws config: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

### Bitflyer

- get your api key from here: https://lightning.bitflyer.com/developer

## Develop

1. For first time running the terraform in local, run the following to initiate the terraform
    ```sh
    cd terraform/
    terraform init
    ```
1. Deploy lambda with terraform

    ```sh
    > sh build-lambda.sh

    > cd terraform/

    # check the changes, add key, and secret for bitflyer
    > terraform plan
    var.bitflyer_key
    Enter a value: ***

    var.bitflyer_secret
    Enter a value: ***


    # apply the changes, and key, and secret for bitflyer
    > terraform apply

    var.bitflyer_key
    Enter a value: ***

    var.bitflyer_secret
    Enter a value: ***
    ```

## Config setup

TODO
