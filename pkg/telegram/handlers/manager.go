package handlers

import (
	"ExerciseManagerBot/pkg/config"
	tele "gopkg.in/telebot.v3"
)

type Definer interface {
	Define()
}

type Manager struct {
	client *tele.Bot
	config *config.BotConfig
}

func NewDefaultManager(client *tele.Bot, config *config.BotConfig) *Manager {
	return &Manager{client: client, config: config}
}

func (m *Manager) Define() {
	m.defineCommands()
}

func (m *Manager) defineCommands() {
	m.client.Handle(StartCommand, m.startCommandHandler)
	m.client.Handle(HelpCommand, m.helpCommandHandler)
}
