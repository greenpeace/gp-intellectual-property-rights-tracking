# Selector Bot

The Selector Bot is triggered by the messages that are placed in Pub-Sub by the merchandise bots. It will check in the Firestore database which items are new (those have status = False). It selects on keywords, duplicates and vintage. It deletes the non-relevant ones and sets the relevant links to active.

## The solution in few words
The bot will select the relevant links that were scraped by the e-commerce bots.


## Creating the Cloud Function
Go to the Cloud Functions page of the Google Cloud Platform Console. Create a new function and give it a name that is meaningful.

## Deploy
gcloud functions deploy <cloud function name> --runtime python310 --set-env-vars PROJECT_NAME=<gcp_project_name> --trigger-http --allow-unauthenticated --region=europe-west1 --memory=128MB

## You may have to alter the IAM if you can not get the function to work
gcloud functions add-iam-policy-binding <function name> --region=<region> --member=allUsers --role=roles/cloudfunctions.invoker

## Requests-html library
The selector bot uses the firebase libraries to access the database. 
