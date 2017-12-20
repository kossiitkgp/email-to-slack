
# Reading emails on slack

If your team works on a Slack workspace while you have to maintain a bunch of different email ids and wish to
be notified of every email instantly on slack, there is a hack for you.

## How does it work ?

1. Set up a [forwarding email](https://get.slack.help/hc/en-us/articles/206819278-Send-emails-to-Slack#set-up-a-forwarding-email-address). If you send any email to this address, it will appear as a file in your Direct Messaging channel with slackbot.
2. Add this address as a forwarding address of your email account. (For gmail find forwarding options from gmail settings)
3. Use Slack API (which sucks) to get notified about this.
4. Use Slack API (sucks so bad) to post the email on a channel you want to.

## Detailed instructions

Step 1 and 2 are very easy and you can help yourself by searching the web enough.

Step 3 -

* Go to https://api.slack.com/apps and create a new Slack app.
* After creating the app, navigate to the app dashboard and find "Event Subscriptions" in the sidebar.
* Subscribe to the event `message.im` which is the only event we need to be notified about.
* Go to "OAuth and Permissions" and add `files:read` and `im:history` scopes. Note the OAuth access token here to be used for `SLACK_WORKSPACE_TOKEN_FOR_APP` environment variable.
* Add the URL of your server (A heroku app which can be deployed from this repository)
  * Take care with the `Content-type` you use when interacting with Slack API. `application/x-www-form-urlencoded` works most of the time.
* The payload is then recieved and parsed in [main.go](https://github.com/kossiitkgp/email-to-slack/blob/master/main.go)
  * Slackbot uploads the email as a file. The file id is extracted from the message.
  * The email subject and body is extracted upon getting the file info.
* A message is then posted on the channel specified.

You can understand Step 4 in `main.go`. Simply search for `api.PostMessage` in the module.

# Description of environment variables used by the repository

| Config Variable                 | Description                                                          |
|---------------------------------|----------------------------------------------------------------------|
| `APP_ID`                        | You get this when you create the app                                 |
| `SLACK_PAYLOAD_TOKEN`           | You get this when you create the app                                 |
| `TEAM_ID`                       | ID of your slack workspace                                           |
| `CHANNEL_ID`                    | The ID of the channel you want to send your emails to                |
| `MY_DM_CHANNEL`                 | The ID of the direct messaging channel between you and @slackbot     |
| `SLACK_BOT_TOKEN`               | Token of a slack bot which has the permission to post to $CHANNEL_ID |
| `SLACKBOT_USER_ID`              | Set it to `USLACKBOT`                                                |
| `SLACK_WORKSPACE_TOKEN_FOR_APP` | Find it in our Slack App's "OAuth and Permissions" tab               |

Note that the Slack IDs (for channel, users, files) are alphanumeric uppercase string of 9 characters.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Current status of the project

[@OrkoHunter](https://github.com/OrkoHunter) maintains this repository and handles the configurations for KOSS slack channel.

He also gets annoyed with the constant `Unread Mentions` on the slack due to slackbot's messages for emails. But he uses
[Tampermonkey](https://tampermonkey.net/) and runs [this custom script](https://gist.github.com/OrkoHunter/09edb7ada76078f36f54f95ce0457a87)
to get rid of those.

And yes, Slack API sucks.
