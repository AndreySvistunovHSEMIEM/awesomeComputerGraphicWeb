import os
import tempfile
from fpdf import FPDF
from PIL import Image


def generate_pdf(folder_images, orientation, sort_order):
    """
    Генерирует PDF-файл, содержащий изображения, сгруппированные по папкам.
    :param folder_images: Словарь, где ключи - названия папок, а значения - списки путей к изображениям.
    :param orientation: Ориентация страницы ('P' для портретной, 'L' для альбомной).
    :param sort_order: Порядок сортировки ('ascending' или 'descending').
    :return: Данные PDF-файла в байтовом формате.
    """

    pdf = FPDF(orientation=orientation)
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    max_y_position = 277 if orientation == 'P' else 195
    images_per_row = 6 if orientation == 'L' else 3  # 6 изображений в альбомной и 3 в портретной
    image_width = 100 if orientation == 'L' else 60  # Ширина изображений зависит от ориентации
    image_height = 80 if orientation == 'L' else 60  # Высота изображений зависит от ориентации

    for folder, images in folder_images.items():
        # Сортируем изображения в зависимости от порядка
        images.sort(key=lambda x: x[1], reverse=(sort_order == 'descending'))

        pdf.cell(0, 10, txt=f"{folder}", ln=True)
        pdf.ln(5)  # Добавляем небольшое пространство между заголовком и изображениями
        current_y_position = pdf.get_y()

        for i, (image_path, _) in enumerate(images):
            try:
                with Image.open(image_path) as img:
                    img.thumbnail((image_width, image_height))  # Изменяем размеры изображения

                    # Проверяем, нужно ли добавлять новую страницу
                    if current_y_position + image_height + 10 > max_y_position:
                        pdf.add_page()  # Добавление новой страницы при необходимости
                        current_y_position = 10  # Сброс y позиции на новой странице

                    # Устанавливаем положение для изображения
                    x_position = (i % images_per_row) * (image_width + 10) + 10
                    pdf.image(image_path, x=x_position, y=current_y_position, w=image_width, h=image_height)

                    # Переход на следующую позицию y
                    if (i + 1) % images_per_row == 0:
                        current_y_position += image_height + 15  # Переход на следующую строку + дополнительно пространство
                    else:
                        current_y_position += 0  # Сброс y позиции, чтобы оставалась на том же уровне

            except Exception as e:
                print(f"Ошибка при добавлении изображения {image_path}: {e}")
                continue

        current_y_position += 10  # Дополнительное пространство перед следующей папкой
        pdf.ln(10)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf_file:
        tmp_pdf_path = tmp_pdf_file.name
        pdf.output(tmp_pdf_path)

    with open(tmp_pdf_path, "rb") as f:
        pdf_data = f.read()

    os.remove(tmp_pdf_path)  # Удаляем временный файл

    return pdf_data