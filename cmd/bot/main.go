package main

import (
	"ExerciseManagerBot/pkg/config"
	"fmt"
)

func main() {
	BotConfig := config.NewBotConfig()

	fmt.Println(BotConfig)

}
