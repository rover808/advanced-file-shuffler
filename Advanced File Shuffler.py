import random
import os
import sys
import argparse
from tqdm import tqdm
from collections import Counter


class AdvancedFileShuffler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Профессиональный инструмент перемешивания строк')
        self.setup_arguments()
        self.args = self.parser.parse_args()

        # Автоматически активируем удаление дубликатов
        self.remove_duplicates = True  # Всегда активно
        self.duplicates_removed = 0   # Счетчик удаленных дубликатов

    def setup_arguments(self):
        """Настройка аргументов командной строки"""
        self.parser.add_argument(
            '-i', '--input', default='input.txt', help='Входной файл')
        self.parser.add_argument(
            '-o', '--output', default='output.txt', help='Выходной файл')
        self.parser.add_argument('-n', '--intensity', type=int, default=5,
                                 help='Интенсивность перемешивания (3-10)')
        self.parser.add_argument('-e', '--keep-empty', action='store_true',
                                 help='Сохранять пустые строки')
        self.parser.add_argument('-c', '--crypto', action='store_true',
                                 help='Криптографически стойкое перемешивание')
        self.parser.add_argument('--no-progress', action='store_true',
                                 help='Отключить индикатор прогресса')

    def read_and_filter(self):
        """Чтение и предварительная обработка файла"""
        try:
            with open(self.args.input, 'r', encoding='utf-8') as f:
                lines = [line.strip('\n') if self.args.keep_empty else line.strip()
                         for line in f]

                if not self.args.keep_empty:
                    lines = [line for line in lines if line]

                return lines
        except Exception as e:
            print(f"❌ Ошибка чтения файла: {e}")
            sys.exit(1)

    def remove_duplicate_lines(self, lines):
        """Удаление дубликатов с сохранением порядка"""
        seen = set()
        unique_lines = []

        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
            else:
                self.duplicates_removed += 1

        print(f"\n🔍 Удалено дубликатов: {self.duplicates_removed}")
        print(f"🔍 Уникальных строк сохранено: {len(unique_lines)}")
        return unique_lines

    def enhanced_shuffle(self, lines):
        """Улучшенный алгоритм перемешивания"""
        if self.args.crypto:
            random.seed(os.urandom(16))

        shuffled = lines.copy()

        for _ in tqdm(range(self.args.intensity),
                      desc="🌀 Перемешивание",
                      disable=self.args.no_progress):

            random.shuffle(shuffled)

            for i in range(len(shuffled)-1, 0, -1):
                j = random.randint(0, i)
                shuffled[i], shuffled[j] = shuffled[j], shuffled[i]

        return shuffled

    def analyze_results(self, original, processed):
        """Расширенный анализ результатов"""
        same_pos = sum(1 for o, s in zip(original, processed) if o == s)
        changed = len(original) - same_pos

        print("\n" + "="*60)
        print("📊 ДЕТАЛЬНАЯ СТАТИСТИКА".center(60))
        print("="*60)
        print(f"{'▪ Всего строк в исходном файле:':<35} {len(original):>10,}")
        print(f"{'▪ Удалено дубликатов:':<35} {self.duplicates_removed:>10,}")
        print(f"{'▪ Сохранено уникальных строк:':<35} {len(processed):>10,}")
        print(
            f"{'▪ Осталось на месте:':<35} {same_pos:>10} ({same_pos/len(original):.2%})")
        print(
            f"{'▪ Изменено позиций:':<35} {changed:>10} ({changed/len(original):.2%})")
        print(
            f"{'▪ Интенсивность перемешивания:':<35} {self.args.intensity:>10} раундов")
        print("="*60)

    def save_results(self, data):
        """Сохранение результатов с проверкой"""
        try:
            with open(self.args.output, 'w', encoding='utf-8') as f:
                f.write('\n'.join(data))
            print(f"\n✅ Результат сохранен в '{self.args.output}'")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            sys.exit(1)

    def run(self):
        """Основной процесс выполнения"""
        print("\n" + "="*60)
        print("=== УЛУЧШЕННЫЙ ИНСТРУМЕНТ ПЕРЕМЕШИВАНИЯ ===".center(60))
        print("="*60)

        # 1. Чтение файла
        print(f"\n📖 Чтение файла '{self.args.input}'...")
        original_lines = self.read_and_filter()
        print(f"✔ Прочитано строк: {len(original_lines):,}")

        # 2. Автоматическое удаление дубликатов
        print("\n🔍 Поиск и удаление дубликатов...")
        processed_lines = self.remove_duplicate_lines(original_lines)

        # 3. Перемешивание
        print("\n🔀 Начало перемешивания...")
        shuffled_lines = self.enhanced_shuffle(processed_lines)

        # 4. Сохранение результатов
        print(f"\n💾 Сохранение результатов...")
        self.save_results(shuffled_lines)

        # 5. Анализ
        self.analyze_results(original_lines, shuffled_lines)

        print("\n✨ Обработка завершена. Нажмите Enter для выхода...")


if __name__ == "__main__":
    shuffler = AdvancedFileShuffler()
    shuffler.run()
    input("Нажмите Enter для выхода...")
