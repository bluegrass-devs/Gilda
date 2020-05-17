# Gilda
A simple learning/bot for the Bluegrass Developers guild .... Gilda. or should it be Guilda? 🤷‍♂️

## build new functions

* `fn init --runtime python --trigger http events`
* `fn list triggers gilda `

## Running locally

1. start the local server `fn start --log-level debug`
1. Make sure you have a local app `fn list apps`
1. set up two environment variables `
    * `fn cf a gilda random_channel_id <some_id>`
    * `fn cf a gilda webhook_url <some_url>`
1. deploy locally `fn --verbose deploy --app gilda --all --local`
1. List functions `fn list functions gilda`
1. Grab local url `fn inspect function gilda events`

### invoke

use the fn command `echo -n '{"name":"Bob"}' | fn invoke gilda events`

or simply good old fashioned curl, like your mother taught you:
```
curl -X "POST" -H "Content-Type: application/json" -d '{ "type": "url_verification","token": "1234","challenge": "5678"}' http://localhost:8080/t/gilda/events
```
