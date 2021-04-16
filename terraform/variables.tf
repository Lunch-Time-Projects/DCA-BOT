# Below is an example of a single config entry, which we want to schedule
# a MARKET buy of 1000JPY worth of BTC_JPY every two minutes:
#
# default = {
#   btc-bitflyer = {
#     input = {
#       product_code = "BTC_JPY",
#       target_cost  = 1000
#     },
#     schedule_expression = "cron(*/2 * * * ? *)"
#   }
# }
variable "dca_bot_config" {
  type = map(any)
  default = {
  }
}

variable "bitflyer_key" {
  type      = string
  sensitive = true
}

variable "bitflyer_secret" {
  type      = string
  sensitive = true
}
