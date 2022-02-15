# Bitbucket Google Chat Notifications

A simple flask application that acts as a notification bridge between Bitbucket and Google Chat.


## Build with Docker

```
docker build -t bb-gc-api -f Dockerfile .
```

## Run with Docker

```
docker run -d --rm --name bb-gc-api -p 5000:5000 bb-gc-api
```

## Supported events

- `repo:refs_changed`
- `repo:modified`
- `repo:fork`
- `repo:comment:added`
- `repo:comment:edited`
- `repo:comment:deleted`
- `pr:opened`
- `pr:from_ref_updated`
- `pr:modified`
- `pr:reviewer:updated`
- `pr:reviewer:approved`
- `pr:reviewer:unapproved`
- `pr:reviewer:needs_work`
- `pr:merged`
- `pr:declined`
- `pr:deleted`
- `pr:comment:added`
- `pr:comment:edited`
- `pr:comment:deleted`

See [this page](https://confluence.atlassian.com/bitbucketserver/manage-webhooks-938025878.html) for more information on event payloads.

`mirror:repo_synchronized` is not supported.

## Webhook Configuration

Bitbucket webhook configuration:

`http://my-api-url/api/bitbucket/invoke?space=[SPACE_KEY]&key=[GOOGLE_CHAT_KEY]&token=[GOOGLE_CHAT_TOKEN]`

Replace the follow variables in brackets above:

- `SPACE_KEY` The space key in the google chat webhook url
- `GOOGLE_CHAT_KEY` The key parameter in the google chat webhook url
- `GOOGLE_CHAT_TOKEN` The token parameter in the google chat webhook url

## Secure Mode

The application runs in insecure mode by default.  The application will not verify message integrity in insecure mode.

Set the environment variable `BBGC_SECRET_TOKEN` to enable secure mode.  The value of this token must equal the value of
the Secret field on the Bitbucket webhook configuration page.  Secure mode will validate all your requests using the token
set by `BBGC_SECRET_TOKEN`.  If the message integrity cannot be verified, the message will be dropped.  

`BBGC_SECRET_TOKEN` can be set when running with docker with the parameter `-e BBGC_SECRET_TOKEN=my-token-value`

See [this page](https://confluence.atlassian.com/bitbucketserver0718/manage-webhooks-1097182842.html#Managewebhooks-webhooksecretsWebhooksecrets) for more information.

## Compatibility

This project has only been tested with Bitbucket Server 6.x and above.

Compatibility with Bitbucket Cloud is unknown.

## License

Copyright (c) 2022 Travis Ball

Licensed under the [MIT License](LICENSE)