from flask import request, render_template, send_file
import os
import io
import tempfile
import shutil
from werkzeug.utils import secure_filename
from src.color_utils import is_color_dominant, get_red_dominance
from src.pdf_generator import generate_pdf

def index():
    """"
    Обрабатывает запросы на главной странице и загружает изображения.

    Проверяет загруженные файлы, определяет порядок сортировки, ориентацию
    и целевой цвет изображений, а затем выполняет необходимые действия.

    :return: HTML-шаблон главной страницы с сообщением или pdf файл.
    """
    message = ""

    if request.method == 'POST':
        files = request.files.getlist('images')
        orientation = request.form.get('orientation')
        target_color = request.form.get('color')
        sort_order = request.form.get('sort_order')  # Получаем порядок сортировки

        if not files or files[0].filename == '':
            message = "Файлы не загружены."
        else:
            temp_dir = tempfile.mkdtemp(prefix="uploads_")
            folder_images = {}

            try:
                for file in files:
                    filepath = os.path.join(temp_dir, secure_filename(file.filename))
                    file.save(filepath)

                    folder_name = os.path.basename(temp_dir)
                    if is_color_dominant(filepath, target_color):
                        red_value = get_red_dominance(filepath)
                        if folder_name not in folder_images:
                            folder_images[folder_name] = []
                        folder_images[folder_name].append((filepath, red_value))

                if any(folder_images.values()):
                    pdf_data = generate_pdf(folder_images, orientation, sort_order)
                    return send_file(
                        io.BytesIO(pdf_data),
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name='images_by_color.pdf'
                    )
                else:
                    message = "Нет изображений с преобладающим цветом."
            finally:
                shutil.rmtree(temp_dir)

    return render_template('index.html', message=message)
