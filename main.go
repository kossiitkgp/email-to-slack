package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	_ "github.com/heroku/x/hmetrics/onload"
)

func main() {
	port := os.Getenv("PORT")

	if port == "" {
		log.Fatal("$PORT must be set")
	}

	router := gin.New()
	router.Use(gin.Logger())

    router.POST("/", func(c *gin.Context) {

        var json struct {
            Value string `json:"challenge" binding:"required"`
        }

        if c.Bind(&json) == nil {
            c.JSON(200, gin.H{"challenge": json.Value})
        }

    })

	router.Run(":" + port)
}
