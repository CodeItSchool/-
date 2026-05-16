import cv2
import numpy as np
from collections import Counter


def get_color_name(hsv_color):
    """
    Определяет название цвета по значениям HSV.
    """
    h, s, v = hsv_color

    # Если насыщенность слишком низкая — считаем оттенком серого/белого/черного
    if s < 30:
        if v < 50:
            return "Черный"
        elif v > 200:
            return "Белый"
        else:
            return "Серый"

    # Определяем цвет по оттенку (Hue)
    if 0 <= h < 10 or 170 <= h <= 180:
        return "Красный"
    elif 10 <= h < 25:
        return "Оранжевый"
    elif 25 <= h < 35:
        return "Желтый"
    elif 35 <= h < 78:
        return "Зеленый"
    elif 78 <= h < 100:
        return "Бирюзовый"
    elif 100 <= h < 130:
        return "Синий"
    elif 130 <= h < 150:
        return "Фиолетовый"
    elif 150 <= h < 170:
        return "Розовый"
    else:
        return "Другой"


def analyze_image_palette(image_path, top_colors=5):
    """
    Анализирует цветовую палитру изображения.

    :param image_path: путь к изображению
    :param top_colors: сколько основных цветов вывести
    """
    # Загружаем изображение
    image = cv2.imread(image_path)

    if image is None:
        print(f"Ошибка: не удалось загрузить изображение '{image_path}'")
        print("Убедитесь, что файл существует и путь указан правильно.")
        return

    print(f"Изображение: {image_path}")
    print(f"Размер: {image.shape[1]}x{image.shape[0]} пикселей")
    print("-" * 40)

    # Преобразуем из BGR в HSV (лучше для анализа цветов)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Уменьшаем размер для ускорения анализа (опционально)
    # Масштабируем до 100 пикселей по меньшей стороне
    scale = 100 / min(image.shape[:2])
    if scale < 1:
        new_width = int(image.shape[1] * scale)
        new_height = int(image.shape[0] * scale)
        hsv_image = cv2.resize(hsv_image, (new_width, new_height))

    # Собираем все пиксели
    pixels = hsv_image.reshape(-1, 3)

    # Определяем название цвета для каждого пикселя
    color_names = [get_color_name(pixel) for pixel in pixels]

    # Считаем частоту каждого цвета
    color_counts = Counter(color_names)
    total_pixels = len(color_names)

    # Сортируем по убыванию частоты
    most_common = color_counts.most_common()

    print("ЦВЕТОВАЯ ПАЛИТРА:")
    print("=" * 40)

    for color, count in most_common[:top_colors]:
        percentage = (count / total_pixels) * 100
        bar = "█" * int(percentage / 2)  # Визуальная шкала
        print(f"{color:12} | {percentage:6.2f}% | {bar}")

    print("=" * 40)

    # Показываем все остальные цвета (если есть)
    other_colors = most_common[top_colors:]
    if other_colors:
        other_count = sum(count for _, count in other_colors)
        other_percentage = (other_count / total_pixels) * 100
        print(f"{'Другие':12} | {other_percentage:6.2f}%")

    # Показываем изображение (опционально)
    cv2.imshow("Image", image)
    print("\nНажмите любую клавишу, чтобы закрыть окно...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# === ЗАПУСК ===
if __name__ == "__main__":
    # Укажите путь к вашему изображению
    # Если файл в той же папке, что и скрипт:
    image_path = "Image.png"

    # Или полный путь:
    # image_path = r"C:\Users\YourName\Projects\MyProject\Image.png"

    # Анализируем топ-7 цветов
    analyze_image_palette(image_path, top_colors=7)