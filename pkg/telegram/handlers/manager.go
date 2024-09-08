package handlers

import (
	"ExerciseManagerBot/pkg/config"
	tele "gopkg.in/telebot.v3"
)

type Manager struct {
	client *tele.Bot
	config *config.BotConfig
}

func NewManager(client *tele.Bot, config *config.BotConfig) *Manager {
	return &Manager{client: client, config: config}
}

func (m *Manager) DefineHandlers() {
	m.defineCommandHandlers()
}

func (m *Manager) defineCommandHandlers() {
	m.client.Handle(StartCommand, m.startCommandHandler)
	m.client.Handle(HelpCommand, m.helpCommandHandler)
}
