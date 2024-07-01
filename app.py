from PIL import Image
import os
import math

def create_tiff_from_images(folder_path, output_file, padding=10):
    # Получаем список всех файлов в папке
    images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    if not images:
        print(f"Нет изображений в папке: {folder_path}")
        return
    
    # Открываем все изображения и получаем их размеры
    opened_images = [Image.open(image) for image in images]
    widths, heights = zip(*(i.size for i in opened_images))

    # Определяем размеры сетки
    num_images = len(opened_images)
    grid_size = math.ceil(math.sqrt(num_images))
    max_width = max(widths)
    max_height = max(heights)

    # Создаем пустое изображение для результирующего файла с учетом отступов
    total_width = grid_size * max_width + (grid_size + 1) * padding
    total_height = grid_size * max_height + (grid_size + 1) * padding
    result_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))

    # Располагаем изображения в результирующем файле
    for index, image in enumerate(opened_images):
        x_offset = (index % grid_size) * (max_width + padding) + padding
        y_offset = (index // grid_size) * (max_height + padding) + padding
        result_image.paste(image, (x_offset, y_offset))

    # Сохраняем результирующий файл
    result_image.save(output_file, format='TIFF', save_all=True)
    print(f"Файл сохранен как {output_file}")

def process_all_folders_in_directory(base_directory):
    # Получаем список всех папок в текущем каталоге
    folders = [f for f in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, f))]
    
    for index, folder in enumerate(folders, start=1):
        folder_path = os.path.join(base_directory, folder)
        output_file = os.path.join(base_directory, f"Result{index}.tif")
        create_tiff_from_images(folder_path, output_file)

if __name__ == "__main__":
    base_directory = os.path.dirname(os.path.abspath(__file__))
    process_all_folders_in_directory(base_directory)
