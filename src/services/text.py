def generate_progress_bar(
    progress: int,
    bar_length: int = 20,
    filled_symbol: str = "█",
    partial_symbol: str | None = None,
    empty_symbol: str = "░",
) -> str:
    """
    Generates a progress bar string based on the specified percentage.

    :param progress: Percentage of completion (from 0 to 100).
    :param bar_length: Total length of the progress bar in characters.
    :param filled_symbol: Symbol for the filled part of the progress bar.
    :param partial_symbol: Symbol indicating half fullness.
    :param empty_symbol: Symbol for the empty part of the progress bar.
    :return: A string representing the progress bar.
    """
    if partial_symbol is None:
        partial_symbol = empty_symbol

    total_units = bar_length

    progress_units = (progress / 100) * total_units

    bar = ""
    for i in range(1, total_units + 1):
        if progress_units >= i:
            bar += filled_symbol
        elif progress_units >= i - 0.5:
            bar += partial_symbol
        else:
            bar += empty_symbol

    return bar
