# sitemap_to_titleDescription_list_parser
Для использования скрипта нужно выполнить несколько шагов:
1. Установите git  и клонируйте этот репозиторий
    git clone git@github.com:Enderw12/sitemap_to_titleDescription_list_parser.git
или скачайте архив и распакуйте где ни будь в вашей файловой системе.
2. Установите pipenv — https://pypi.org/project/pipenv/
3. откройте терминал вашей OS и перейдите в каталог с парсером
4. введите команду pipenv sync для установки всех зависимостей
5. введите команду  для активации виртуального окружения
    pipenv shell
6. введите для вывода подсказки
    python parseMeta.py --help

Пример использования скрипта:
    python parseMeta.py --sitemap https://foo.bar/sitemap.xml --threads 10 --timeout 2000
где https://foo.bar/sitemap.xml — ссылка на sitemap.xml
содержащий страницы сайта с которых нужно собрать МЕТА-теги title и description;

параметр --threads число указывает на количество потоков выполнения,
ускоряет сбор, но может "перегрузить" некоторые сайты при больших значениях.
Значение по умолчанию 5;

параметр --timeout число указывает на время ожидания в миллисекундах
между запросами каждого потока в отдельности.
Значение по умолчанию 1000 (1 секунда).

Результатом парсинга будет xlsx документ с МЕТА-тегами og:title, og:description, og:url
