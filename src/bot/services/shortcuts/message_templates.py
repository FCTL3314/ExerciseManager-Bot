from aiogram import html

from src.bot.services.shortcuts.commands import (
    ADD_WORKOUT_COMMAND,
    LOGIN_COMMAND,
    REGISTER_COMMAND,
    ADD_EXERCISE_COMMAND,
)
from src.services.text import generate_progress_bar

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
INVALID_URL_MESSAGE = (
    "❌ Введённый URL недействителен. Пожалуйста, убедитесь, что ссылка начинается с "
    f"{html.bold("http://")} или {html.bold("https://")} и попробуйте снова:"
)

# User action requests
ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE = (
    "📋 Пожалуйста, выберите тренировку, к которой вы хотите добавить упражнение:"
)
START_WORKOUT_WORKOUT_SELECTION_MESSAGE = (
    "📋 Пожалуйста, выберите тренировку, которую вы хотите начать:"
)

# State notifications
_BASE_NO_WORKOUTS_MESSAGE = "❌ У вас пока нет созданных тренировок."
ADD_EXERCISE_NO_WORKOUTS_MESSAGE = (
    f"{_BASE_NO_WORKOUTS_MESSAGE} "
    f"Пожалуйста, создайте тренировку перед добавлением упражнений с помощью команды {html.bold(ADD_WORKOUT_COMMAND)}."
)
START_WORKOUT_NO_WORKOUTS_MESSAGE = (
    f"{_BASE_NO_WORKOUTS_MESSAGE} "
    f"Пожалуйста, создайте тренировку, которую вы хотите начать, используя команду {html.bold(ADD_WORKOUT_COMMAND)}."
)
NO_EXERCISES_MESSAGE = (
    "❌ У вас пока нет упражнений для этой тренировки тренировок."
    f"Пожалуйста, добавьте упражнения, используя команду {html.bold(ADD_EXERCISE_COMMAND)}."
)
CANCELED_MESSAGE = (
    "✅ Отменено. " "Если хотите начать заново, введите соответствующую команду."
)

# Exercises
EXERCISE_DESCRIPTION_MESSAGE = (
    "<b>🏋️ Упражнение:</b> {name}\n"
    "<b>📄 Описание:</b> {description}\n"
    "<b>⏱️ Продолжительность:</b> {duration}\n"
)
EXERCISE_COMPLETED_MESSAGE = "✅ Упражнение <b>{name}</b> выполнено!"
WORKOUT_REST_TIMER_MESSAGE = (
    f"💤 Отдыхайте, осталось {html.bold("{seconds_left}")} секунд..."
)
WORKOUT_EXERCISE_TIMER_MESSAGE = (
    f"🔥 Выполняйте упражнение, осталось {html.bold("{seconds_left}")} секунд..."
)
WORKOUT_REST_PROGRESS_MESSAGE = (
    f"💤 Отдыхайте - {html.bold("{progress}%")}\n\n{{progress_bar}}"
)
WORKOUT_EXERCISE_PROGRESS_MESSAGE = (
    f"🔥 Выполняйте упражнение - {html.bold("{progress}%")}\n\n{{progress_bar}}"
)
WORKOUT_COMPLETED_MESSAGE = "🎉 Тренировка закончена, ты молодец!"
FAILED_TO_SEND_EXERCISE_IMAGE_MESSAGE = (
    "❕ Не удалось отправить изображение. Пожалуйста, проверьте "
    "ссылку — возможно, она устарела или была указана некорректно. "
    "Попробуйте обновить ссылку на актуальную."
)


def get_workout_rest_progress_bar(progress: int) -> str:
    progress_bar = generate_progress_bar(
        progress,
        bar_length=12,
        filled_symbol=" 🌕 ",
        partial_symbol="🌗",
        empty_symbol=" 🌑 ",
    )
    return WORKOUT_REST_PROGRESS_MESSAGE.format(
        progress_bar=progress_bar,
        progress=progress,
    )


def get_workout_exercise_progress_bar(progress: int) -> str:
    progress_bar = generate_progress_bar(
        progress,
        bar_length=12,
        filled_symbol=" 🌕 ",
        partial_symbol="🌗",
        empty_symbol=" 🌑 ",
    )
    return WORKOUT_EXERCISE_PROGRESS_MESSAGE.format(
        progress_bar=progress_bar,
        progress=progress,
    )
