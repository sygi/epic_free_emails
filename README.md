# Epic Store free game notifications

Sends an email whenever there is a new free game in the Epic Store.

Deployment:
```bash
rm deploy.zip && cd package && zip -r ../deploy.zip .&& cd ../ && zip deploy *.py
```
And uploading the zip through AWS lambda UI.
