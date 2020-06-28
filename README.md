# Gilda

![Build](https://github.com/bluegrass-devs/Gilda/workflows/Python%20package/badge.svg?branch=master)

A simple bot for the Bluegrass Developers guild .... Gilda. or should it be Guilda? 🤷‍♂️

Please feel free to submit PRs for any issues, errors, and/or additional functionality. Before doing so see the [code of conduct](CODE_OF_CONDUCT.md).

## Getting started

### Install dev dependencies

1. [Docker](https://www.docker.com/get-started)
1. [Fn Project](https://fnproject.io/tutorials/python/intro/)

### Start Gilda

1. Start the local server: `fn start --log-level debug`
1. Create Gilda app: `fn create app gilda`
1. Deploy locally: `fn --verbose deploy --app gilda --all --local --no-bump`
1. Create a new function: `fn init --runtime python --trigger http <function name>`
1. Run your function: `echo -n '<args>' | fn invoke gilda <function name>`

## Libraries and tools we use

- [Insomnia Core](https://insomnia.rest/)
- [Terraform](https://www.terraform.io/intro/index.html)
- [OCI CLI](https://docs.cloud.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)

## Useful commands

- Start the local server `fn start --log-level debug`
- See local apps `fn list apps`
- Create environment variables:

  - if you don't want to use Slack or OCI endpoints (everything stays local) `fn cf a gilda is_local True` to delete `fn cf a gilda is_local ""`
  - to use OCI local config `fn cf a gilda local_oci_config True` to delete `fn cf a gilda local_oci_config ""`
  - `fn cf a gilda random_channel_id <some_id>`
  - `fn cf a gilda slack_bot_token <some token>`
  - `fn cf a gilda compartment_id <oracle OCID>`
  - `fn cf a gilda web_auth_token auth_1234`
  - `fn cf a gilda local_oci_config True`

- Deploy locally: `fn --verbose deploy --app gilda --all --local --no-bump`
- List functions: `fn list functions gilda`
- Grab local url: `fn inspect function gilda events`
- List http triggers: `fn list triggers gilda`

## Deploy

1. create context `fn create context gilda --provider oracle --registry yyz.ocir.io/<id>/gilda --api-url https://functions.ca-toronto-1.oraclecloud.com`
1. `fn use context gilda`
1. `fn update context oracle.compartment-id`
1. `fn --verbose deploy --app Gilda --all`

### Invoke

use the fn command `echo -n '{"name":"Bob"}' | fn invoke gilda events`

or simply good old fashioned curl, like your mother taught you:

```
curl -X "POST" -H "Content-Type: application/json" -d '{ "type": "url_verification","token": "JRoGaO6sIgohYqywBlT3Q0vz","challenge": "wnxwuwy1LjvmMB7HWTV3M2KRiYDhQgeLqlxhT2064MIvVFtOYTN1", "event": {"type": "member_joined_channel", "channel":"<some_id>", "user": "<some_url>"} }'  http://localhost:8080/t/gilda/events

curl -X "POST" -H "Content-Type: application/json" -d '{"token": "auth_1234"}' http://localhost:8080/t/gilda/learning
```

Or use [Insomnia Core](https://insomnia.rest/) and import the `insomnia_export.json`
