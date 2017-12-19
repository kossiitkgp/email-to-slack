package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	_ "github.com/heroku/x/hmetrics/onload"
)

type E struct {
    Events string
}

type MessageIMEventJSON struct {
    EventType string `json:"type"`
    Channel string `json:"channel"`
    User string `json:"user"`
    Text string `json:"text"`
    TS string `json:"ts"`
}

func main() {
	port := os.Getenv("PORT")

	if port == "" {
		log.Fatal("$PORT must be set")
	}

	router := gin.New()
	router.Use(gin.Logger())

    router.POST("/", func(c *gin.Context) {

        var json MessageIMEventJSON

        data := &E{}


        if c.Bind(&json) == nil {
            log.Println("EventType ", json.EventType)
            log.Println("Channel ", json.Channel)
            log.Println("User ", json.User)
            log.Println("Text ", json.Text)
            log.Println("TS ", json.TS)
            c.JSON(200, gin.H{"a": "a"})
        } else if c.Bind(data) == nil {
            log.Println(data)
        } else {
            log.Println("Could not fucking decode")
        }

    })

	router.Run(":" + port)
}
