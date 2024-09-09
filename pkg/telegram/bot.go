package telegram

import (
	"ExerciseManagerBot/pkg/config"
	"ExerciseManagerBot/pkg/telegram/handlers"
	"fmt"
	tele "gopkg.in/telebot.v3"
)

type Bot struct {
	botClient       *tele.Bot
	config          *config.BotConfig
	handlersManager handlers.Definer
}

func NewBot(botClient *tele.Bot, config *config.BotConfig) *Bot {
	handlersManager := handlers.NewDefaultManager(botClient, config)
	return &Bot{
		botClient:       botClient,
		config:          config,
		handlersManager: handlersManager,
	}
}

func (b *Bot) Start() {
	b.handlersManager.Define()

	fmt.Println("Bot is now running. Press CTRL-C to exit.")
	b.botClient.Start()
}
