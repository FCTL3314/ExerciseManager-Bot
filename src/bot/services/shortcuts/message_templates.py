from aiogram import html

from src.bot.services.shortcuts.commands import (
    ADD_WORKOUT_COMMAND,
    LOGIN_COMMAND,
    REGISTER_COMMAND,
)

# Start
START_MESSAGE = (
    f"Привет 👋, {html.bold("{name}")}!\n\n"
    "Я твой личный фитнес-ассистент 🤸🏻‍♀️️. "
    "Вместе мы создадим эффективные тренировочные программы, добавим упражнения 🏃‍♂️ и будем отслеживать твой прогресс 📊. "
    "Я напомню, когда нужно сделать перерыв 🛌, и подскажу, когда пора продолжать 🏃‍♀️.\n\n"
    "Готов начать тренировки? 🎯 "
    f"Для этого зарегистрируйся с помощью команды {html.bold(REGISTER_COMMAND)} или войди через {html.bold(LOGIN_COMMAND)}"
)

# Validation
INVALID_USERNAME_MESSAGE = (
    f"❌ Имя пользователя должно быть от {html.bold("{min_length}")} до {html.bold("{max_length}")} символов. "
    f"Пожалуйста, попробуйте снова:"
)
INVALID_PASSWORD_MESSAGE = (
    f"❌ Пароль должен быть от {html.bold("{min_length}")} до {html.bold("{max_length}")} символов. "
    f"Пожалуйста, попробуйте снова:"
)
INVALID_WORKOUT_NAME_MESSAGE = (
    f"❌ Название тренировки должно быть от {html.bold("{min_length}")} до {html.bold("{max_length}")} символов. "
    f"Пожалуйста, попробуйте снова:"
)
INVALID_EXERCISE_NAME_MESSAGE = (
    f"❌ Название упражнения должно быть от {html.bold("{min_length}")} до {html.bold("{max_length}")} символов. "
    f"Пожалуйста, попробуйте снова:"
)

# User action requests
ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE = (
    "📋 Пожалуйста, выберите тренировку, к которой вы хотите добавить упражнение:"
)
START_WORKOUT_WORKOUT_SELECTION_MESSAGE = (
    "📋 Пожалуйста, выберите тренировку, которую вы хотите начать:"
)

# State notifications
_BASE_NOT_WORKOUTS_MESSAGE = "❌ У вас пока нет созданных тренировок."
ADD_EXERCISE_NO_WORKOUTS_MESSAGE = (
    f"{_BASE_NOT_WORKOUTS_MESSAGE} "
    f"Пожалуйста, создайте тренировку перед добавлением упражнений с помощью команды {html.bold(ADD_WORKOUT_COMMAND)}."
)
START_WORKOUT_NO_WORKOUTS_MESSAGE = (
    f"{_BASE_NOT_WORKOUTS_MESSAGE} "
    f"Пожалуйста, создайте тренировку, которую вы хотите начать, используя команду {html.bold(ADD_WORKOUT_COMMAND)}."
)
CANCELED_MESSAGE = (
    "✅ Отменено. " "Если хотите начать заново, введите соответствующую команду."
)

# Exercises
EXERCISE_DESCRIPTION_MESSAGE = (
    "<b>🏋️ Упражнение:</b> {name}\n"
    "<b>📄 Описание:</b> {description}\n"
    "<b>⏱️ Продолжительность:</b> {duration} секунд\n"
)
EXERCISE_COMPLETED_MESSAGE = "✅ Упражнение <b>{name}</b> выполнено!"
REST_PERIOD_TIMER_MESSAGE = "💤 Отдыхайте, осталось {seconds_left} секунд..."
WORKOUT_EXERCISE_TIMER_MESSAGE = (
    "🔥 Выполняйте упражнение, осталось {seconds_left} секунд..."
)
WORKOUT_COMPLETED_MESSAGE = "🎉 Тренировка закончена, ты молодец!"
