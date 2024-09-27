from aiogram import html

from src.bot.services.shortcuts.commands import ADD_WORKOUT_COMMAND

INVALID_USERNAME_TEMPLATE = "❌ Имя пользователя должно быть от {min_length} до {max_length} символов. Пожалуйста, попробуйте снова:"
INVALID_PASSWORD_TEMPLATE = "❌ Пароль должен быть от {min_length} до {max_length} символов. Пожалуйста, попробуйте снова:"

INVALID_WORKOUT_NAME_TEMPLATE = "❌ Название тренировки должно быть от {min_length} до {max_length} символов. Пожалуйста, попробуйте снова:"

INVALID_EXERCISE_NAME_TEMPLATE = "❌ Название упражнения должно быть от {min_length} до {max_length} символов. Пожалуйста, попробуйте снова:"

SELECT_WORKOUT_MESSAGE = "📋 Выберите тренировку, к которой хотите добавить упражнение:"
NO_WORKOUTS_MESSAGE = f"❌ У вас пока нет созданных тренировок. Пожалуйста, создайте тренировку перед добавлением упражнений, используя команду {html.bold(ADD_WORKOUT_COMMAND)}."
