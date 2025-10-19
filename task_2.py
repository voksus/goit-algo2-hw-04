from trie import Trie

# Очищуємо консоль
print('\033c', end='', flush=True)

# --- Налаштування кольорів для консолі ---
RESET  = '\033[0m'
BOLD   = '\033[1m'
GREEN  = '\033[48;2;0;127;31m'
BLUE   = '\033[44m'
RED    = '\033[31m'

class Homework:
    def __init__(self):
        # Trie для звичайного прямого пошуку (наприклад, для префіксів)
        self.forward_trie = Trie() 
        # Trie для зворотного пошуку (відповідно для 'count_words_with_suffix')
        self.reverse_trie = Trie() 

    def put(self, key, value=None):
        self.forward_trie.put(key, value)
        # Вставляємо слово у зворотному порядку (для суфіксів)
        self.reverse_trie.put(key[::-1], value)

    # Логіка практично скопійована з конспекту за прикладом методу `count_words_with_prefix`,
    # але тут просто використали додатковий інвертовані Trie і рядок для пошуку
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError(f'Illegal argument for countWordsWithSuffix: prefix = {pattern} must be a string')

        reverse_pattern = pattern[::-1]
        current = self.reverse_trie.root
        for char in reverse_pattern:
            if char not in current.children:
                return 0
            current = current.children[char]

        return self._count_words(current)

    def _count_words(self, node):
        count = 1 if node.value is not None else 0
        for child in node.children.values():
            count += self._count_words(child)
        return count

    def has_prefix(self, prefix) -> bool:
        current = self.forward_trie.root
        for char in prefix:
            if char not in current.children:
                return False # Немає такого шляху
            current = current.children[char]

        return True

if __name__ == '__main__':
    trie = Homework()
    words = ['apple', 'application', 'banana', 'cat']
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка
    try:
        # Кількість слів, що закінчуються на заданий суфікс
        suffixes = {'e': 1, 'ion': 1, 'a': 1, 'at': 1}
        for suffix, count in suffixes.items():
            assert trie.count_words_with_suffix(suffix) == count
            print(f'{BOLD+GREEN} Ok {RESET} Суфікс "{suffix}" знайдено')

        # Наявність префікса
        prefixes = {'app': True, 'bat': False, 'ban': True, 'ca': True}
        for prefix, exists in prefixes.items():
            assert trie.has_prefix(prefix) == exists
            print(f'{BOLD+GREEN} Ok {RESET} Префікс "{prefix}" ', end='')
            if exists:
                print('знайдено')
            else:
                print('не знайдено')

        print(f'\n{BLUE} Всі тести успішно пройдені! {RESET}')
    except AssertionError as e:
        print(f'{BOLD+RED}Помилка в тестах!{RESET} {e}')