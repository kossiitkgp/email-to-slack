# Reading emails on slack

If your team works on a Slack workspace, and the team has to maintain a bunch of different email ids and wish to
be notified of every email instantly on slack; there is a hack for you.

# How does it work?

After setting up your Slackbot chat as a forward emailing address of your email account `(Steps expalined below)`
this bot watches for messages in the Slackbot chat and whenever a message arrives with an attached email, It forwards it to a channel as a message.

## Installation

> You can create a account for just emails as the emails appear in the DM of the user that sets up the app. If you want to avoid two notifications, one from the slackbot and one from this app, it is advised to use a secondary account to setup this app.

### Slack mail generation

1. Generate the email for forwarding to slack from "**Preferences -> Messages and Media -> Bring emails into Slack**"
   ex email: `[something]@[workspace].slack.com`
2. Setup forwarding in gmail.
   Gmail sends a email to slack with the link to confirm. This email shows up in the slackbot. Click on the link and accept forwarding.
3. Send a sample mail to account to test whether it gets forwarded correctly. This email should show up in the slackbot dm.

### Creating the Slack App

1. Go to api.slack.com/apps and create a new Slack app.
2. Save the following details:
   **App ID**
   **Verification token**
3. In "**Sidebar -> OAuth and Permissions**" give the permissions for:
   - `files:read`, `im:history` in User Token Scopes
   - and `incoming-webhook` in Bot Token Scopes
4. Then Install the app from "**Sidebar -> OAuth and Permissions**"

### Deploying the server

> Here we will deploy on heroku for simplicity. This can be deployed to any other hosting provider or the app can be self hosted if you choose to do so. Do note that though deployment on heroku is optional, deployment itself is not!
> If you have deployed the app elsewhere, please set the environment variables accordingly.

For heroku ensure: You have the `heroku-cli` installed. If you haven't logged in: `heroku login`

Then in the root of the repo:

```sh
$ heroku create # creates a new heroku app
$ git push heroku master:main # deploys the master branch
```

> _Aside_:
> One quick way to test that the deployment was semi-successful is to visit the deployed URL and it should redirect to the github's repo. The app processes the POST requests and all GET requests are forwarded to the repo's page.

Now time to configure the environment variables on heroku!

| Config Variable        | Description                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| `APP_ID`               | You get this when you create the app                             |
| `INCOMING_WEBHOOK_URL` | You get this when you install the app on one channel             |
| `TEAM_ID`              | ID of your slack workspace.                                      |
| `USLACKBOT_CHANNEL`    | The ID of the direct messaging channel between you and @slackbot |
| `VERIFICATION_TOKEN`   | You get this when you create the app                             |

Note that the Slack IDs (for channel, users, files) are alphanumeric uppercase string of 9 characters. In browser, if you have opened the chat with the slackbot the URL will be of the format:

```
https://app.slack.com/client/<TEAM_ID>/<USLACKBOT_CHANNEL>/
```

For more details on finding team and channel ID [see this question on stackoverflow](https://stackoverflow.com/questions/40940327/what-is-the-simplest-way-to-find-a-slack-team-id-and-a-channel-id).

You can set these variables either on the Heroku Dashboard or via cli:

```
$ heroku config:set APP_ID=xxxxxxxx
```

Do note the link to which server is deployed, we will set it up in slack settings in a moment.

### Setup of Event Subscription

1. Navigate to "**Sidebar -> Event Subscription**" and turn on.
2. Put the link to the deployed server in "Request URL".
3. Subscribe to `message.im` in **Subscribe to events on behalf of users**

Viola the setup is complete!

## Notes:

- Slack creates a beautiful file for an email. But I could not find way to change file permissions which is shared privately with just the user. Hence, I have to customize and post the email. If there is a way to change file permissions from private to be shared in a team, that would be easy and the best way.

# Alternative

A PHP version of [email-to-slack by Mehdi Chaouch](https://github.com/mehdichaouch/email-to-slack)

# Troubleshoot

**The deployment doesn't work?**

- [ ] Check if the permissions required are present.
- [ ] Check heroku logs.
- [ ] Check if the server deployment is live by sending a GET request

If these steps don't work please file an [Issue](https://github.com/kossiitkgp/email-to-slack/issues/new).
