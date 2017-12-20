package main

import (
	"log"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	_ "github.com/heroku/x/hmetrics/onload"
	"github.com/nlopes/slack"
)

type MessageIMEventJSON struct {
	EventType string `json:"type"`
	Channel   string `json:"channel"`
	User      string `json:"user"`
	Text      string `json:"text"`
	TS        string `json:"ts"`
}

type SlackPayloadJSON struct {
	Token    string             `json:"token"`
	TeamID   string             `json:"team_id"`
	APIAppID string             `json:"api_app_id"`
	EventID  string             `json:"event_id"`
	Event    MessageIMEventJSON `json:"event"`
}

func authenticate(payloadjson *SlackPayloadJSON) bool {
	credentials := [4]string{
		os.Getenv("SLACK_PAYLOAD_TOKEN"),
		os.Getenv("TEAM_ID"),
		os.Getenv("APP_ID"),
		os.Getenv("MY_DM_CHANNEL"),
	}

	received_credentials := [4]string{
		payloadjson.Token,
		payloadjson.TeamID,
		payloadjson.APIAppID,
		payloadjson.Event.Channel,
	}

	return credentials == received_credentials
}

func main() {
	port := os.Getenv("PORT")

	if port == "" {
		log.Fatal("$PORT must be set")
	}

	router := gin.New()
	router.Use(gin.Logger())

	router.POST("/", func(c *gin.Context) {

		var payloadjson SlackPayloadJSON

		bind_err := c.Bind(&payloadjson)
		valid_req := authenticate(&payloadjson)

		if bind_err == nil && valid_req {
			log.Println("Token", payloadjson.Token)
			log.Println("TeamID", payloadjson.TeamID)
			log.Println("APIAppID", payloadjson.APIAppID)
			log.Println("EventID", payloadjson.EventID)
			log.Println("Event", payloadjson.Event)

			log.Println("EventType ", payloadjson.Event.EventType)
			log.Println("Channel ", payloadjson.Event.Channel)
			log.Println("User ", payloadjson.Event.User)
			log.Println("Text ", payloadjson.Event.Text)
			log.Println("TS ", payloadjson.Event.TS)

			// Prepare the message to be sent
			slackbot_message := strings.Split(payloadjson.Event.Text, "|")[0]
			link := strings.Split(slackbot_message, " ")
			message_to_send := `Received a new email. Content : ` + link[len(link)-1][1:]
			log.Println(message_to_send)

			// Send the message
			api := slack.New(os.Getenv("SLACK_BOT_TOKEN"))
			params := slack.NewPostMessageParameters()
			params.Text = message_to_send
			params.Username = "bhattu"
			params.AsUser = true
			params.Parse = "full"

			api.PostMessage(os.Getenv("CHANNEL_ID"), message_to_send, params)

			c.JSON(200, gin.H{"success": true})
		} else {
			c.JSON(404, gin.H{"success": false})
		}
	})

	router.Run(":" + port)
}
