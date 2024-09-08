package telegram

import (
	"ExerciseManagerBot/pkg/config"
	"fmt"
	tele "gopkg.in/telebot.v3"
)

type Bot struct {
	client *tele.Bot

	messages config.Messages
}

func NewBot(client *tele.Bot, messages config.Messages) *Bot {
	return &Bot{
		client:   client,
		messages: messages,
	}
}

func (b *Bot) Start() {
	b.defineHandlers()

	fmt.Println("Bot is now running. Press CTRL-C to exit.")
	b.client.Start()
}

func (b *Bot) defineHandlers() {
	b.defineCommandHandlers()
}

func (b *Bot) defineCommandHandlers() {
	b.client.Handle(startCommand, b.startCommandHandler)
}
