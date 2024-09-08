package config

import (
	"github.com/spf13/viper"
	"log"
)

type Responses struct {
	CommandStart string `mapstructure:"command_start"`
}

type Errors struct {
	Default string `mapstructure:"default"`
}

type Messages struct {
	Responses
	Errors
}

type BotConfig struct {
	// From env files
	BotToken string `mapstructure:"bot_token"`

	// From config files
	BotUrl string `mapstructure:"bot_url"`
	Messages
}

func NewBotConfig() *BotConfig {
	bc := &BotConfig{}
	if err := bc.LoadEnv("./.env"); err != nil {
		log.Fatal(
			"Error loading .env file. Check that the file exists and is filled out without errors.",
		)
	}

	if err := bc.LoadYml("configs/main.yml"); err != nil {
		log.Fatal(
			"Error loading config file main.yml. Check that the files exist and are filled in without errors.",
		)
	}

	return bc
}

func (bc *BotConfig) setupViper(Path string, ConfigType string) error {
	viper.SetConfigFile(Path)
	viper.SetConfigType(ConfigType)

	if err := viper.ReadInConfig(); err != nil {
		return err
	}
	return nil
}

func (bc *BotConfig) loadFromFile(Path string, ConfigType string) error {
	if err := bc.setupViper(Path, ConfigType); err != nil {
		return err
	}

	if err := viper.Unmarshal(&bc); err != nil {
		return err
	}

	return nil
}

func (bc *BotConfig) LoadEnv(Path string) error {
	if err := bc.loadFromFile(Path, "env"); err != nil {
		return err
	}

	return nil
}

func (bc *BotConfig) LoadYml(Path string) error {
	if err := bc.loadFromFile(Path, "yml"); err != nil {
		return err
	}

	return nil
}
