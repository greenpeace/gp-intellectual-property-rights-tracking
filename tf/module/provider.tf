variable "path" {default = "/Users/tzetterl/Documents"}

provider "google" {
    project = "torbjorn-zetterlund"
    region  = "us-central1"
    #credentials = "${file("${var.path}/torbjorn-zetterlund-b1ef72b3b19b.json")}"
}