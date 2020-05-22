# Gilda

![Build](https://github.com/bluegrass-devs/Gilda/workflows/Python%20package/badge.svg?branch=master)

A simple bot for the Bluegrass Developers guild .... Gilda. or should it be Guilda? 🤷‍♂️

Please feel free to submit PRs for any issues, errors, and/or additional functionality. Before doing so see the [code of conduct](CODE_OF_CONDUCT.md).

## Libraries and tools we use

* [Fn Project](https://fnproject.io/tutorials/python/intro/)
* [Insomnia Core](https://insomnia.rest/)
* [Terraform](https://www.terraform.io/intro/index.html)
* [OCI CLI](https://docs.cloud.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)

## build new functions

* `fn init --runtime python --trigger http <function name>`
* `fn list triggers gilda` should list the http trigger for the new event

## Running locally

1. start the local server `fn start --log-level debug`
1. Make sure you have a local app `fn list apps`
    * if not create one `fn create app gilda`
1. set up two environment variables `
    * `fn cf a gilda random_channel_id <some_id>`
    * `fn cf a gilda webhook_url <some_url>`
    * if you don't want to post to url `fn cf a gilda is_local True`
1. deploy locally `fn --verbose deploy --app gilda --all --local --no-bump`
1. List functions `fn list functions gilda`
1. Grab local url `fn inspect function gilda events`

## Deploy

1. create context `fn create context gilda --provider oracle --registry yyz.ocir.io/<id>/gilda --api-url https://functions.ca-toronto-1.oraclecloud.com`
1. `fn use context gilda `
1. `fn update context oracle.compartment-id`
1. `fn --verbose deploy --app Gilda --all`

### invoke

use the fn command `echo -n '{"name":"Bob"}' | fn invoke gilda events`

or simply good old fashioned curl, like your mother taught you:
```
curl -X "POST" -H "Content-Type: application/json" -d '{ "type": "url_verification","token": "JRoGaO6sIgohYqywBlT3Q0vz","challenge": "wnxwuwy1LjvmMB7HWTV3M2KRiYDhQgeLqlxhT2064MIvVFtOYTN1", "event": {"type": "member_joined_channel", "channel":"<some_id>", "user": "<some_url>"} }'  http://localhost:8080/t/gilda/events

curl -X "POST" -H "Content-Type: application/json" -d '{"token": "1234"}' http://localhost:8080/t/gilda/learning
```

Or use [Insomnia Core](https://insomnia.rest/) and import the `insomnia_export.json`
