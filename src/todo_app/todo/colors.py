def get_task_css_classes(task) -> str:
    """Return correct CSS classes for the given task based on the weather data.

    Arguments:
        task (todo_app.todo.models.Task): Task to get the CSS classes for.

    Returns:
        (str): CSS classes for the given task.
    """
    if task.weather is None:
        return "border"

    temperature = task.weather.temperature
    main = task.weather.main

    if temperature < 0 or main == "Rain":
        return "border-indigo bg-indigo-100"

    if (temperature >= 0 and temperature < 15) or main == "Clouds":
        return "border-orange bg-orange-100"

    if temperature >= 15 or main == "Clear":
        return "border-red bg-red-100"
