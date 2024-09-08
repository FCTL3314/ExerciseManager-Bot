package telegram

import (
	"ExerciseManagerBot/pkg/config"
	"ExerciseManagerBot/pkg/telegram/handlers"
	"fmt"
	tele "gopkg.in/telebot.v3"
)

type Bot struct {
	Client *tele.Bot
	Config *config.BotConfig
}

func NewBot(client *tele.Bot, config *config.BotConfig) *Bot {
	return &Bot{
		Client: client,
		Config: config,
	}
}

func (b *Bot) Start() {
	hm := handlers.NewManager(b.Client, b.Config)
	hm.DefineHandlers()

	fmt.Println("Bot is now running. Press CTRL-C to exit.")
	b.Client.Start()
}
