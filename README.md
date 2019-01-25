# Reading emails on slack

If your team works on a Slack workspace and the team has to maintain a bunch of different email ids and wish to
be notified of every email instantly on slack; there is a hack for you.

# How does it work ?
1. Set up a forwarding email. If you send any email to this address, it will appear as a file in your Direct Messaging channel with slackbot.
1. Add this address as a forwarding address of your email account. (For gmail find forwarding options from gmail settings)
1. Use Slack API to get notified about this.
1. Use Slack API to post the email on a channel you want to.

# Detailed steps
Step 1 and 2 are very easy and you can help yourself by searching the web enough.

For Step 3 and 4:

- Create a bot account for this purpose. Add it to your workspace.
- Go to api.slack.com/apps and create a new Slack app.
- After creating the app, navigate to the app dashboard and find "Event Subscriptions" in the sidebar.
- Subscribe to the event `message.im` which is the only event we need to be notified about.
- Go to "OAuth and Permissions" and add `files:read`, `im:history` and `incoming-webhood` scopes.
- Install it in your workspace
- Activate incoming webhook for a channel. This will let you easily post to a channel.
- Add the URL of your server (A heroku app which can be deployed from this repository)
- The payload is then recieved and parsed.
  - Slackbot uploads the email as a file.

# Description of environment variables used by the repository

| Config Variable                 | Description                                                          |
|---------------------------------|----------------------------------------------------------------------|
| `APP_ID`                        | You get this when you create the app                                 |
| `INCOMING_WEBHOOK_URL`          | You get this when you install the app on one channel                 |
| `TEAM_ID`                       | ID of your slack workspace. [See this](https://stackoverflow.com/questions/40940327/what-is-the-simplest-way-to-find-a-slack-team-id-and-a-channel-id)   |
| `USLACKBOT_CHANNEL`             | The ID of the direct messaging channel between you and @slackbot     |
| `VERIFICATION_TOKEN`            | You get this when you create the app                                 |

Note that the Slack IDs (for channel, users, files) are alphanumeric uppercase string of 9 characters.

Notes:
  - Slack creates a beautiful file for an email. But I could not find way to change file permissions which is shared privately with just the user. Hence, I have to customize and post the email. If there is a way to change file permissions from private to be shared in a team, that would be easy and the best way.
