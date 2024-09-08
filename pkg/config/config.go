package config

import (
	"github.com/joho/godotenv"
	"github.com/spf13/viper"
	"log"
	"os"
	"strings"
)

type EnvLoader interface {
	LoadEnv(Path string) error
}

type YmlLoader interface {
	LoadYml(Path string) error
}

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
	BotToken string

	// From config files
	BotUrl string `mapstructure:"bot_url"`
	Messages
}

func NewBotConfig() *BotConfig {
	bc := &BotConfig{}
	if err := bc.LoadEnv("./.env"); err != nil {
		log.Fatal("Error loading .env file. Check if the file exists.")
	}

	if err := bc.LoadYml("configs/main.yml"); err != nil {
		log.Fatal("Error loading config file main.yml. Check if all config files exists.")
	}

	return bc
}

func (bc *BotConfig) LoadEnv(Path string) error {
	if err := godotenv.Load(Path); err != nil {
		return err
	}

	bc.BotToken = os.Getenv("BOT_TOKEN")

	return nil
}

func (bc *BotConfig) LoadYml(Path string) error {
	parts := strings.Split(Path, "/")
	Directory := strings.Join(parts[:len(parts)-1], "/")
	FileName := parts[len(parts)-1]

	viper.AddConfigPath(Directory)
	viper.SetConfigName(FileName)
	viper.SetConfigType("yml")

	if err := viper.ReadInConfig(); err != nil {
		return err
	}

	if err := viper.Unmarshal(&bc); err != nil {
		return err
	}

	if err := viper.UnmarshalKey("messages.response", &bc.Messages.Responses); err != nil {
		return err
	}
	if err := viper.UnmarshalKey("messages.errors", &bc.Messages.Errors); err != nil {
		return err
	}

	return nil
}
