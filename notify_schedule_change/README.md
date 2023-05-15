# Notify Schedule Changes FaaS
This is an event-driven function that uses Google Pub/Sub to listen to changes to the schedule and notify all users (pub/sub consumers) of delays and cancellations. 

When a new schedule is uploaded to the bucket, this function will fire, look for any delays, and send the list of delays as a message to the topic. It's a one-to-many mapping; all users subscribed to the topic will get notified.

In a real-world setting, a user can be a subscriber to the topic by having the 2727 app installed and allowing notifications.


To deploy:
- first run '../pubsubclients/create_topic_sub.py'
- change the bucket id and project id in the .env.yaml file.
- make sure to use the same topic name when creating the topic, subscribing, and publishing
- `gcloud functions deploy notify_schedule_change --runtime python310 --region=us-central1 --gen2 --entry-point=notify_schedule_change --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=group3_schedule" --env-vars-file .env.yaml --memory 2Gi --allow-unauthenticated`

Then run the consumer to listen to schedule changes.

To test the function, upload a new (or the same) schedule to the bucket.