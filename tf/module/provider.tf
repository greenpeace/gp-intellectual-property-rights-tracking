variable "path" {default = "/Users/tzetterl/Documents"}

provider "google" {
    project = "torbjorn-zetterlund"
    region  = "europe-west1"
    credentials = "${file("${var.path}/GlobalLandD-c35aace9c93f.json")}"
}