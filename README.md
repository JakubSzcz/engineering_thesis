# API procesowe (*PROC_API*)
Branch zawiera cały kod źródłowy, stworzonego jako część mikroserwisu API typu REST. Odpowiada ono za szczegółowe walidowanie, transformowanie, przetwarzanie oraz forwardowanie zapytań w zależności od docelowej bazy danych. Dodatkowo, gra kluczową rolę w procesie uwierzytelniania oraz tworzenia nowych użytkowników poprzez tworzenie haseł, oraz sprawdzanie ich poprawności z skrótem zapisanym w bazie danych. 
### Opis struktury
1. `main.py` - główny plik wykonawczy, inicjalizuje serwer http, scala zdekomponowane rutery obsługujące konkretna zapytania znajdujące się w folderze `routes`
2. `config.py` - główny plik konfiguracyjny
3. `Dockerfile` - plik konfuguracyjny aplikacji *Docker* wykorzystywany w procesie wdrażania aplikacji jako kontener
4. `models` - folder zawierający wszystkie stałe struktury i modele takie jak przykłady zapytań stworzone za pomocą biblioteki *Pydantic*, dostosowane opisy zwracanych błędów *HTTP*, przykładowe wartości wykorzystywane przy generowaniu interaktywnej dokumentacji *OpenAPI* etc.
5. `routes` - folder zawierające szczegółową obsługę wszystkich endpointów, wyodrębnionych do oddzielnych plików na podstawie dostarczanych funkcjonalności. Implementuje m. in. proces transormacji oraz reforwardowania zapytań, znaczną część procesu uwierzytelniania oraz tworzenia użytkownika np. tworzenie tokenów *JWT*, tworzenie skrótów haseł przed ich zapisaniem w bazie etc. 
6. `utilities` -  folder zawierający pliki pomocniczę, takie jak `functions.py` z funkcjami wykorzystywanymi globalnie w obrębie całej aplikacji

### Wdrażanie API
API zostało wdrożone jako integralna część systemu mikroserwisowego na podstawie dostarczonego pliku `Dockerfile` przy użyciu pliku `compose.yaml` znajdującego się w branchu **main**.
