OUTPUT_BUCKET_NAME = $(shell terraform output bucket_name)
DATASET_ID = $(shell terraform output dataset_id)

all: plan apply

clean:
	gsutil rm -fr gs://$(OUTPUT_BUCKET_NAME)/*.csv || true
	rm -fr tf.plan .terraform build

init .terraform:
	@terraform init
	cat .terraform/terraform.tfstate

update:
	@terraform get -update

validate: .terraform
	@terraform validate

refresh: validate
	@terraform refresh

plan: validate
	@terraform plan -out tf.plan

sleep:
	@echo Sleeping 3 seconds, ctrl-c to abort
	$(shell sleep 3)

apply:
	terraform apply --auto-approve tf.plan

output:
	@terraform output

show:
	@terraform show

destroy:
	terraform destroy

trigger:
	@echo "todo"
