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

	router.GET("/", func(c *gin.Context) {
		c.String(200, "Hello")
	})

    router.POST("/", func(c *gin.Context) {
        c.JSON(200, gin.H{"challenge": c.PostForm("challenge")})
    })

	router.Run(":" + port)
}
