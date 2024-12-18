# Serverless Python + AWS Lambda HTTP Post To Categorize Content

An AWS Lambda function to categorize content based on the brand id and content.

## Configure Serverless

1. Install the `serverless-python-requirements` plugin if you don't have it already.

```bash
sls plugin install -n serverless-python-requirements
```

2. Update `serverless.yml` to include the `serverless-python-requirements` plugin.
3. Update the 'service' of the service in `serverless.yml` to your desired service name.
4. If you want to see logs in CloudWatch, you can add the following handler to the `handler.py` file:

```python
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.StreamHandler()  # Output logs to stdout
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
```

## Run Locally

```bash
serverless invoke local --function categorize --data '{"body": "{\"brandId\": \"d42d5411-aac8-4cbd-aacb-05e946e78af5\", \"content\": \"Hello engineers\"}"}'
```

## Deploy Serverless

```bash
serverless deploy
```
