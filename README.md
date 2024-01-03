# API prezentacyjne (*EXP_API*)
Branch zawiera cały kod źródłowy, stworzonego jako część mikroserwisu API typu REST. Odpowiada ono za obsługę bezpośrednich żądań pochodzących z zewnątrz mikroserwisu, walidowaniu ich, oraz zapewnianiu podstaw bezpieczeństwa. 
### Opis struktury
1. `main.py` - główny plik wykonawczy, inicjalizuje serwer http, scala zdekomponowane rutery obsługujące konkretna zapytania znajdujące się w folderze `routes`
2. `config.py` - główny plik konfiguracyjny
3. `cache.py` - plik implementujący system buforowania zawartości, stworzony do dalszego rozwoju aplikacji
4. `Dockerfile` - plik konfuguracyjny aplikacji *Docker* wykorzystywany w procesie wdrażania aplikacji jako kontener
5. `models` - folder zawierający wszystkie stałe struktury i modele takie jak przykłady zapytań stworzone za pomocą biblioteki *Pydantic*, dostosowane opisy zwracanych błędów *HTTP*, przykładowe wartości wykorzystywane przy generowaniu interaktywnej dokumentacji *OpenAPI* etc.
6. `routes` - folder zawierające szczegółową obsługę oraz implementujący logikę wszystkich endpointów, wyodrębnionych do oddzielnych plików na podstawie dostarczanych funkcjonalności
7. `utilities` -  folder zawierający pliki pomocniczę, takie jak `functions.py` z funkcjami wykorzystywanymi globalnie w obrębie całej aplikacji

### Wdrażanie API
API zostało wdrożone jako integralna część systemu mikroserwisowego na podstawie dostarczonego pliku `Dockerfile` przy użyciu pliku `compose.yaml` znajdującego się w branchu **main**.
