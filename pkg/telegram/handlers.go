package telegram

import (
	tele "gopkg.in/telebot.v3"
)

func (b *Bot) startCommandHandler(c tele.Context) error {
	return c.Send(b.messages.CommandStart)
}
