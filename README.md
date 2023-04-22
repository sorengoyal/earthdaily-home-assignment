## Usage
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