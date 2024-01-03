# API systemowe (*SYS_API*)
Branch zawiera cały kod źródłowy, stworzonego jako część mikroserwisu API typu REST. Odpowiada ono za bezpośrednią komunikację z każdym z testowanych silników bazodanowych, nawiązywanie i utrzymywanie połączenia, wykonywania operacji oraz obsługę potencjalnych wyjątków i błędów. 
### Opis struktury
1. `main.py` - główny plik wykonawczy, inicjalizuje serwer http, scala zdekomponowane rutery obsługujące konkretna zapytania znajdujące się w folderze `routes`
2. `config.py` - główny plik konfiguracyjny
3. `Dockerfile` - plik konfuguracyjny aplikacji *Docker* wykorzystywany w procesie wdrażania aplikacji jako kontener
4. `SQL_engines` - folder zawierający customową nakładkę stworzoną w celu obsługiwania połączeń z bazami *SQLite* oraz *Postgres* z wykorzystaniem odpowiednich bibliotek
4. `models` - folder zawierający wszystkie stałe struktury i modele takie jak przykłady zapytań stworzone za pomocą biblioteki *Pydantic*, dostosowane opisy zwracanych błędów *HTTP*, przykładowe wartości wykorzystywane przy generowaniu interaktywnej dokumentacji *OpenAPI* etc.
5. `routes` - folder zawierające szczegółową obsługę wszystkich endpointów, podzielonych ze względu na docelową baze danych, implementujących wszystkie funkcjonalności związane z konkretnym silnikiem bazodanowym
6. `utilities` -  folder zawierający pliki pomocniczę, takie jak `functions.py` z funkcjami wykorzystywanymi globalnie w obrębie całej aplikacji

### Wdrażanie API
API zostało wdrożone jako integralna część systemu mikroserwisowego na podstawie dostarczonego pliku `Dockerfile` przy użyciu pliku `compose.yaml` znajdującego się w branchu **main**.
