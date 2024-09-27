from aiogram import html

from src.bot.services.shortcuts.commands import ADD_WORKOUT_COMMAND

# Validation
INVALID_USERNAME_MESSAGE = "❌ Имя пользователя должно быть от {min_length} до {max_length} символов. Пожалуйста, попробуйте снова:"
INVALID_PASSWORD_MESSAGE = "❌ Пароль должен быть от {min_length} до {max_length} символов. Пожалуйста, попробуйте снова:"
INVALID_WORKOUT_NAME_MESSAGE = "❌ Название тренировки должно быть от {min_length} до {max_length} символов. Пожалуйста, попробуйте снова:"
INVALID_EXERCISE_NAME_MESSAGE = "❌ Название упражнения должно быть от {min_length} до {max_length} символов. Пожалуйста, попробуйте снова:"

# User action requests
ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE = (
    "📋 Пожалуйста, выберите тренировку, к которой вы хотите добавить упражнение:"
)
SELECT_WORKOUT_MESSAGE = "📋 Пожалуйста, выберите тренировку, которую вы хотите начать:"

# State notifications
_BASE_NOT_WORKOUTS_MESSAGE = "❌ У вас пока нет созданных тренировок."
ADD_EXERCISE_NO_WORKOUTS_MESSAGE = f"{_BASE_NOT_WORKOUTS_MESSAGE} Пожалуйста, создайте тренировку перед добавлением упражнений с помощью команды {html.bold(ADD_WORKOUT_COMMAND)}."
NO_WORKOUTS_MESSAGE = f"{_BASE_NOT_WORKOUTS_MESSAGE} Пожалуйста, создайте тренировку, которую вы хотите начать, используя команду {html.bold(ADD_WORKOUT_COMMAND)}."
