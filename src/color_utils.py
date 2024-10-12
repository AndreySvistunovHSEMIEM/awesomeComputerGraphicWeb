from colorthief import ColorThief


def is_color_dominant(image_path, target_color):
    """
    Определяет, является ли заданный цвет доминирующим в изображении.
    :param image_path: Путь к изображению (строка).
    :param target_color: Цвет для проверки ('red', 'green', 'blue').
    :return: True, если заданный цвет является доминирующим, иначе False.
    """
    try:
        color_thief = ColorThief(image_path)
        dominant_color = color_thief.get_color(quality=1)
        if target_color == 'red':
            return dominant_color[0] > dominant_color[1] and dominant_color[0] > dominant_color[2]
        elif target_color == 'green':
            return dominant_color[1] > dominant_color[0] and dominant_color[1] > dominant_color[2]
        elif target_color == 'blue':
            return dominant_color[2] > dominant_color[0] and dominant_color[2] > dominant_color[1]
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}: {e}")
        return False


def get_red_dominance(image_path):
    """
    Возвращает среднее значение красного цвета в изображении.
    :param image_path: Путь к изображению (строка).
    :return: Среднее значение красного цвета (0-255).
    """
    try:
        color_thief = ColorThief(image_path)
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color[0]  # Красный компонент
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}: {e}")
        return 0
