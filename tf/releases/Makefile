TFLINT := $(shell command -v tflint 2>/dev/null)

all: plan apply

init .terraform:
	@terraform init

refresh:
	@terraform refresh

validate: .terraform
	@terraform validate

plan tf.plan: validate
	@terraform plan -out tf.plan

lint: tf.plan
ifndef TFLINT
	$(warning WARNING: tflint not installed: https://github.com/terraform-linters/tflint)
else
	tflint
endif

apply: lint
	@terraform apply --auto-approve tf.plan

show:
	@terraform show

output:
	@terraform output

destroy: init
	terraform destroy
