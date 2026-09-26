import os
from pathlib import Path
from tkinter import Tk, filedialog
from markitdown import MarkItDown

# Список расширений, которые поддерживает MarkItDown
# (взято из официальной документации и примеров)
SUPPORTED_EXTENSIONS = {
    '.pdf', '.docx', '.pptx', '.xlsx', '.xls',
    '.jpg', '.jpeg', '.png', '.gif', '.webp',
    '.html', '.htm', '.csv', '.json', '.xml',
    '.txt', '.md', '.epub', '.zip'
}


def convert_folder_to_markdown():
    """
    Запрашивает у пользователя папку, конвертирует все поддерживаемые
    файлы в ней в Markdown и сохраняет их рядом с исходными файлами.
    """
    # Создаём скрытое окно Tkinter для вызова диалога выбора папки
    root = Tk()
    root.withdraw()  # Скрываем основное окно

    print("Пожалуйста, выберите папку с файлами...")
    folder_path = filedialog.askdirectory(
        title="Выберите папку для конвертации в Markdown"
    )

    if not folder_path:
        print("Папка не выбрана. Выход.")
        return

    # Преобразуем в объект Path для удобной работы
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f"Ошибка: '{folder}' не является папкой.")
        return

    print(f"\nНачинаю конвертацию файлов в папке: {folder}\n")

    # Инициализируем конвертер
    md_converter = MarkItDown()

    converted_count = 0
    error_count = 0

    # Проходим по всем файлам в выбранной папке (без подпапок)
    for file_path in folder.iterdir():
        # Пропускаем папки и файлы с неподдерживаемыми расширениями
        if file_path.is_dir():
            continue

        ext = file_path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            print(f"[Пропуск] {file_path.name} (формат не поддерживается)")
            continue

        print(f"[Конвертация] {file_path.name} ...")

        try:
            # Выполняем конвертацию
            result = md_converter.convert(str(file_path))

            # Формируем имя выходного файла (заменяем расширение на .md)
            output_path = file_path.with_suffix('.md')

            # Записываем результат
            # Важно: используем encoding='utf-8' для корректной работы с кириллицей
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.text_content)

            print(f"  -> Успешно сохранён: {output_path.name}")
            converted_count += 1

        except Exception as e:
            print(f"  -> Ошибка при конвертации {file_path.name}: {e}")
            error_count += 1

    # Итоговая статистика
    print("\n" + "=" * 50)
    print(f"Конвертация завершена!")
    print(f"Успешно сконвертировано файлов: {converted_count}")
    if error_count > 0:
        print(f"Файлов с ошибками: {error_count}")
    print("=" * 50)


if __name__ == "__main__":
    convert_folder_to_markdown()