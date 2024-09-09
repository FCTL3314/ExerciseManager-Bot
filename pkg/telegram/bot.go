package telegram

import (
	"ExerciseManagerBot/pkg/config"
	"ExerciseManagerBot/pkg/telegram/handlers"
	"fmt"
	tele "gopkg.in/telebot.v3"
)

type Bot struct {
	Client          *tele.Bot
	Config          *config.BotConfig
	handlersManager handlers.Definer
}

func NewBot(client *tele.Bot, config *config.BotConfig) *Bot {
	handlersManager := handlers.NewDefaultManager(client, config)
	return &Bot{
		Client:          client,
		Config:          config,
		handlersManager: handlersManager,
	}
}

func (b *Bot) Start() {
	b.handlersManager.Define()

	fmt.Println("Bot is now running. Press CTRL-C to exit.")
	b.Client.Start()
}
