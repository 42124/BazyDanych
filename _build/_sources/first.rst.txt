.. Sprawozdanie z Baz danych 1 documentation master file, created by
   sphinx-quickstart on Wed Jun 21 11:25:05 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

1. Partycjonowanie danych
==================================================


.. toctree::
    :maxdepth: 2

:Authors:
    Eryk Mika,
    Michał Łabowicz

:Version: 1.0 of 1.06.2023
:Course: Databases I


Partycjonowanie danych
------------------------

1. Cele stosowania partycjonowania danych

2. Zastosowanie partycjonowania

3. Zalety i wady partycjonowania

4. Implementacja partycjonowania w PostgreSQL


Wstęp teoretyczny
---------------------

Partycjonowanie danych wykorzystuje podzielenie zasobów bazy danych na wiele fizycznych urządzeń. Jest to rozwiązanie podobne do replikacji, lecz w tym przypadku współdzielona jest jedna kopia danych. Partycjonowanie danych może być używane do skalowania bazy danych poprzez dodawanie nowych serwerów lub wirtualnych maszyn, co pozwala na łatwe rozszerzenie przetwarzania danych. Poza tym partycjonowanie może pomóc w minimalizacji ryzyka utraty danych, gdyż w przypadku awarii jednego serwera dane z pozostałych partycji mogą być nadal dostępne. Prowadzi to do tego, że nie tylko jedna maszyna musi poradzić sobie z zapisami i odczytami. Dla przykładu, mając dane na jednym węźle, który obsługuje 100 zapytań na sekundę, to dzieląc dane na 10 węzłów, przynajmniej w teorii będziemy obsługiwać 1000 zapytań na sekundę. Zależy to jednak od faktu, czy dane są równomiernie rozłożone. Podziału tego można dokonać na wiele sposobów.

PostgreSQL wspiera podstawowe partycjonowanie tabel. Oferowane jest wsparcie dla następujących metod:

1. **Podział zakresu** - tabela jest podzielona na zakresy kluczy, które są przydzielone na daną fizyczną partycję, bez nakładania się zakresów. Przedział zakresów jest domknięty po lewej stronie i otwarty po prawej, tzn. np. [10,20).

2. **Partycjonowanie listowe** - tabela jest podzielona "z góry" na podstawie, jakie klucze trafiają na daną partycję.

3. **Partycjonowanie haszowane** - mamy określony dzielnik i resztę z dzielenia dla każdej partycji - przydzielamy klucze do nich na podstawie reszty z dzielenia przez ten dzielnik.

1. Cele stosowania partycjonowania danych
------------------------------------------------
Cele partycjonowania danych w bazach danych mogą obejmować:


**Poprawę wydajności**: Partycjonowanie danych może poprawić wydajność zapytań, ponieważ bazy danych będą przeszukiwać tylko te partycje, które zawierają potrzebne dane, a nie całą bazę danych.

**Zwiększenie dostępności**: Partycjonowanie danych może również poprawić dostępność systemu, ponieważ jeśli jedna partycja ulegnie awarii, to pozostałe partycje nadal będą działać.

**Ułatwienie zarządzania**: Partycjonowanie danych może ułatwić zarządzanie bazą danych, ponieważ można skoncentrować się tylko na potrzebnych partycjach i wykonywać operacje na nich, zamiast na całej bazie danych.

**Optymalizacja archiwizacji i backupów**: Partycjonowanie danych umożliwia lepsze zarządzanie archiwizacją i backupami, ponieważ można archiwizować i backupować tylko te partycje, które się zmieniły, a nie całą bazę danych.

**Umożliwienie równoległego przetwarzania**: Partycjonowanie danych umożliwia równoległe przetwarzanie danych, co może skrócić czas wykonywania zadań.

**Optymalizacja wykorzystania pamięci**: Partycjonowanie danych może zmniejszyć zużycie pamięci, ponieważ dane są dzielone na mniejsze części, co może zwiększyć wykorzystanie pamięci podręcznej.


2. Zastosowanie partycjonowania
----------------------------------
1. **Poprawa wydajności**: Partycjonowanie może poprawić wydajność zapytań do bazy danych, ponieważ zamiast przeszukiwania całej tabeli, system może skupić się na mniejszych partycjach, co zmniejsza czas przetwarzania zapytań.

2. **Ułatwienie zarządzania danymi**: Partycjonowanie ułatwia zarządzanie dużymi tabelami, ponieważ można zarządzać każdą partycją jako odrębną jednostkę, co ułatwia ich indeksowanie, optymalizację, przywracanie i archiwizację.

3. **Poprawa dostępności**: Dzięki partycjonowaniu można zmniejszyć wpływ awarii na całą bazę danych. Jeśli jedna partycja ulegnie awarii, pozostałe partycje wciąż będą działać, a system będzie mógł działać dalej.

4. **Zwiększenie skalowalności**: Partycjonowanie może pomóc w zwiększeniu skalowalności bazy danych, ponieważ pozwala na dodawanie i usuwanie partycji w miarę potrzeby, co umożliwia dostosowanie bazy danych do zmieniających się potrzeb biznesowych.

3. Zalety i wady partycjonowania
-----------------------------------
Partycjonowanie danych ma swoje wady i zalety, które należy rozróżnić ze względu na rodzaj partycjonowania - możemy mieć do czynienia z partycjonowaniem poziomym, gdzie krotki dzielimy ze względu na np. klucz główny i partycjonowaniem pionowym, gdzie tabele (relacje) dzielimy na mniejsze, z których każda posiada pewien podzbiór kolumn wyjściowej tabeli. Należy jednak przy tym zaznaczyć, że w PostgreSQL nie mamy do dyspozycji poleceń, które umożliwiają przeprowadzić ostatni typ partycjonowania "wprost".


**Poziomy podział**
********************
Poziomy podział, znany także jako podział wierszy lub sharding, to proces podziału tabeli na wiele mniejszych tabel na podstawie klucza partycji, takiego jak identyfikator klienta, zakres daty lub region geograficzny. Każda partycja zawiera podzbiór wierszy z oryginalnej tabeli, ale wszystkie kolumny są zachowane. Na przykład, można podzielić tabelę sprzedaży na podstawie miesiąca, tak aby każda partycja zawierała rekordy sprzedaży dla określonego miesiąca. Poziomy podział może oferować kilka korzyści, takich jak szybsze zapytania ze względu na zmniejszenie rozmiaru danych oraz wyższą dostępność i skalowalność dzięki dystrybucji danych. Jednakże ma także pewne wady, takie jak złożoność projektowania bazy danych, administracji i utrzymania, a także nierównomierny rozkład danych powodujący nierównowagę danych. Nierównomierny rozkład danych może prowadzić do problemów wydajnościowych, punktów gorących lub nierównowagi w systemie. Dlatego konieczne jest staranne planowanie i wdrożenie schematu partycjonowania, aby zapewnić optymalne rezultaty.

**Pionowy podział**
********************
Pionowy podział, znany także jako podział kolumn lub normalizacja, polega na podziale tabeli na wiele mniejszych tabel na podstawie podzbioru kolumn, a nie wierszy. Każda partycja zawiera wszystkie wiersze z oryginalnej tabeli, ale tylko niektóre kolumny. Na przykład, można oddzielić dane klienta od preferencji klienta w tabeli klientów. Ten proces może oferować kilka korzyści, takich jak redukcja nadmiaru danych, poprawa wydajności i zwiększona bezpieczeństwo. Jednak może także wprowadzać złożoność do projektowania bazy danych i obniżać wydajność zapytań. Pionowy podział może redukować nadmiarowość poprzez eliminację zduplikowanych lub niepotrzebnych kolumn z każdej tabeli oraz poprawiać wydajność poprzez zmniejszenie szerokości każdej tabeli. Dodatkowo, może poprawić jakość i spójność danych oraz umożliwić przechowywanie kolumnowe dla szybszego kompresowania, indeksowania i agregacji danych. Ponadto, pionowy podział może zwiększać bezpieczeństwo poprzez oddzielenie poufnych kolumn od mniej poufnych lub publicznych kolumn oraz ułatwiać szyfrowanie lub maskowanie danych. Z drugiej strony, może zwiększać złożoność projektowania bazy danych i administracji, a także komplikować logikę aplikacji i optymalizację zapytań. Może również obniżać wydajność zapytań poprzez zwiększenie liczby tabel i łączeń w systemie bazodanowym.

4. Implementacja partycjonowania w PostgreSQL
-----------------------------------------------

**1.** Należy utworzyć tabelę "master", z której wszystkie partycje będą dziedziczyć.

**2.** Ta tabela nie powinna zawierać żadnych danych. Nie należy definiować żadnych ograniczeń sprawdzających (check constraints) na tej tabeli, chyba że mają one być stosowane równie dla wszystkich partycji. Nie ma sensu również definiować na niej żadnych indeksów ani unikalnych ograniczeń.

**3.** Należy utworzyć kilka "dziecięcych" tabel dziedziczących po tabeli "master". Zazwyczaj te tabele nie powinny dodawać żadnych kolumn do zestawu dziedziczonych po tabeli "master".

**4.** Będziemy odnosić się do tych tabel jako partycji, choć są one w każdym calu normalnymi tabelami PostgreSQL.

**5.** Należy dodać ograniczenia tabeli (table constraints) do tabel partycji, aby zdefiniować dozwolone wartości kluczy w każdej partycji.

**6.** Dla każdej partycji należy utworzyć indeks na kolumnie(i) klucza oraz ewentualnie inne indeksy, które mogą być potrzebne. (Indeks klucza nie jest konieczny, ale w większości scenariuszy jest pomocny. Jeśli zamierzamy, że wartości kluczy będą unikalne, należy zawsze tworzyć unikalne lub klucz główny dla każdej partycji.)

**7.** Opcjonalnie można zdefiniować wyzwalacz (trigger) lub regułę (rule), które przekierują dane wprowadzane do tabeli "master" do odpowiedniej partycji.

**8.** Należy upewnić się, że parametr konfiguracji "constraint_exclusion" nie jest wyłączony w pliku postgresql.conf. Jeśli jest wyłączony, zapytania nie będą zoptymalizowane zgodnie z oczekiwaniami.