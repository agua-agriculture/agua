# Agua
sms based water management for Brazilian farmers

## What is it?

An sms based service to help farmers (beginning in Brazil) manage their water usage. The service is currently in development and is not yet ready for use.

## Contributing

To get started, clone the repo and run the following:

```bash

pip install -r requirements.txt

# then create a .env file using the command:
cp .env.example .env

# and fill in the values according to your own db or the admin one
```

To run the server, run the following:

```bash

# From the root directory
python3.10 -m agua

# or if you only have a single version installed
python3 -m agua 
```