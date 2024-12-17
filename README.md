# Serverless Python + AWS Lambda HTTP Post
This is a simple example of how to deploy a Python function as a POST HTTP endpoint to AWS Lambda using Serverless.

## Configure Serverless

1. Install the `serverless-python-requirements` plugin if you don't have it already.

```bash
sls plugin install -n serverless-python-requirements
```

2. Update `serverless.yml` to include the `serverless-python-requirements` plugin.
3. Update the 'service' of the service in `serverless.yml` to your desired service name.

## Deploy Serverless

```bash
serverless deploy 
```
