package handlers

import (
	tele "gopkg.in/telebot.v3"
)

func (m *Manager) startCommandHandler(c tele.Context) error {
	return c.Send(m.config.Messages.CommandStart)
}

func (m *Manager) helpCommandHandler(c tele.Context) error {
	return c.Send(m.config.Messages.CommandHelp)
}
