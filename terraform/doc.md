## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| archive | n/a |
| aws | n/a |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| bitflyer\_key | n/a | `string` | n/a | yes |
| bitflyer\_secret | n/a | `string` | n/a | yes |
| dca\_bot\_config | Below is an example of a single config entry, which we want to schedule a MARKET buy of 1000JPY worth of BTC\_JPY every two minutes:  default = { btc-bitflyer = { input = { product\_code = "BTC\_JPY", target\_cost  = 1000 }, schedule\_expression = "cron(\*/2 \* \* \* ? \*)" } } | `map(any)` | `{}` | no |

## Outputs

No output.
