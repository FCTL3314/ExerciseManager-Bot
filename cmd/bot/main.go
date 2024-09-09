package main

import (
	"ExerciseManagerBot/pkg/config"
	"ExerciseManagerBot/pkg/telegram"
	tele "gopkg.in/telebot.v3"
	"log"
	"time"
)

func main() {
	botConfig := config.NewBotConfig()

	b, err := initBot(botConfig)
	if err != nil {
		log.Fatal(err)
	}

	bot := telegram.NewBot(b, botConfig)
	bot.Start()
}

func initBot(bc *config.BotConfig) (*tele.Bot, error) {
	pref := tele.Settings{
		Token:  bc.Token,
		Poller: &tele.LongPoller{Timeout: 10 * time.Second},
	}

	b, err := tele.NewBot(pref)
	if err != nil {
		return nil, err
	}
	return b, nil
}
