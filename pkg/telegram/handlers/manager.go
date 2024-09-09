package handlers

import (
	"ExerciseManagerBot/pkg/config"
	tele "gopkg.in/telebot.v3"
)

type Definer interface {
	Define()
}

type Manager struct {
	botClient *tele.Bot
	config    *config.BotConfig
}

func NewDefaultManager(botClient *tele.Bot, config *config.BotConfig) *Manager {
	return &Manager{botClient: botClient, config: config}
}

func (m *Manager) Define() {
	m.defineCommands()
}

func (m *Manager) defineCommands() {
	m.botClient.Handle(StartCommand, m.startCommandHandler)
	m.botClient.Handle(HelpCommand, m.helpCommandHandler)
}
