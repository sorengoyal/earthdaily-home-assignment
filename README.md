## Deploying the App

> Make sure your AWS account has the bucket earthdaily-deployments-pdx
```
aws cloudformation package \
--template-file infrastructure_template/template.yaml \
--output-template-file packaged.template \
--s3-bucket earthdaily-deployments-pdx
```

```bash
aws cloudformation deploy \
--template-file packaged.template \
--stack-name EarthdailyAtmStack \
--capabilities CAPABILITY_IAM
```

## Testing the App
Import the Api spec - `EarthdailyAtmStack-Prod-swagger-postman.json` into postman.
Alternatively make the curl requests to the public endpoint - https://utkynsmhz0.execute-api.us-west-2.amazonaws.com/Prod

