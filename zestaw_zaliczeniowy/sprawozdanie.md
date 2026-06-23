# Sprawozdanie — Architektura Aplikacji w Pythonie Radosław Kaczmarczyk 14280

## Lab 1 — Dekoratory

Zaimplementowano dekoratory `retry` oraz `cache_to_disk`. Mechanizm ponawiania wykorzystywał exponential backoff, a wynik poprawnego wywołania był zapisywany w pliku JSON. Dla pięciu prób teoretyczne prawdopodobieństwo sukcesu wynosi:

[
1 - 0.5^5 = 96{,}875%
]

W eksperymencie powodzeniem zakończyło się 96 ze 100 wywołań, czyli 96%. Drugie wywołanie z tym samym argumentem nie zwiększyło licznika wykonań funkcji, co potwierdziło poprawne działanie cache.

## Lab 2 — Współbieżność i równoległość

Porównano wersję sekwencyjną, `ThreadPoolExecutor` oraz `multiprocessing.Pool` podczas obliczania sentymentu 5000 recenzji. Uzyskano następujące czasy:

* sekwencyjnie: 0,491 s,
* ThreadPool: 0,554 s,
* multiprocessing: 0,600 s.

W tym pomiarze najszybsza była wersja sekwencyjna. Obliczenie pojedynczej recenzji było krótkie, dlatego koszt tworzenia procesów i przesyłania danych przewyższył korzyści z równoległości. ThreadPool również nie przyspieszył zadania CPU-bound z powodu ograniczenia GIL.

## Lab 3 — Testowanie z pytest

Zaimplementowano klasę `Tokenizer` obsługującą usuwanie HTML, zamianę tekstu na małe litery, filtrowanie długości tokenów oraz budowę słownika. Przygotowano testy z użyciem fixtures, parametryzacji i `xfail`.

Wynik testów:

* 11 testów zaliczonych,
* 1 test oznaczony jako oczekiwana porażka.

Dla dziesięciu grup po 100 recenzji średnia liczba unikalnych tokenów wyniosła około 4654. Wynik pokazuje duże zróżnicowanie języka naturalnego oraz wpływ nazw własnych, literówek i rzadkich słów.

## Lab 4 — SQLite i kolumna JSON

Porównano klasyczny schemat relacyjny z tabelą zawierającą dokumenty JSON. Dla 2000 rekordów otrzymano:

* rozmiar bazy SQL: 3 215 360 bajtów,
* rozmiar bazy JSON: 3 518 464 bajtów,
* zapis SQL: 44,4 ms,
* zapis JSON: 145,6 ms,
* odczyt SQL: 3,78 ms,
* odczyt JSON: 22,70 ms.

Schemat relacyjny był mniejszy oraz szybszy przy zapisie i odczycie. W tym przypadku dane mają stałą strukturę, dlatego osobne, typowane kolumny są lepszym rozwiązaniem. Kolumna JSON byłaby bardziej przydatna dla danych zmiennych lub niejednorodnych.

## Lab 5 — PySpark Window Functions

Wykorzystano funkcje okienkowe do ustalenia rankingu najdłuższych recenzji w obrębie każdej klasy, obliczenia różnicy od średniej klasowej oraz średniej ruchomej z 50 rekordów.

Wyznaczono top 3 najdłuższe recenzje dla obu klas i przygotowano wykres średniej ruchomej. Ponieważ dane były wcześniej wymieszane, identyfikator `id` nie reprezentował czasu ani naturalnej kolejności. Średnia ruchoma oscylowała więc wokół średniej klasowej bez oczekiwanego trendu.

## Lab 6 — Data Quality Framework

Zaimplementowano klasy `DataContract` oraz `DataValidator`. Kontrakt zawierał reguły dotyczące braków danych, poprawności etykiet, długości recenzji, duplikatów i balansu klas.

Wszystkie reguły krytyczne zakończyły się sukcesem. Reguła `no_html_tags` wykryła HTML w 1189 recenzjach i otrzymała status `warning`, dlatego nie przerwała walidacji. Raport wraz z timestampem został zapisany do pliku `data_quality_report.json`.
