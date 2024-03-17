class PozaPrzedzialem(Exception):
    pass


def tryb_programu():
    while True:
        try:
            tryb = int(input("Wybierz tryb:\n1. Zobaczyć wszystkie hasła,\n"
                             "2. Zobaczyć konkretne hasło,\n3. Dodać nowe hasło,\n"
                             "4. Edytować hasło,\n5. Usunąć jakieś hasło,\n6. Wyjście\n"))

            if 0 < tryb < 7:
                return tryb
            else:
                raise PozaPrzedzialem("Niepoprawny tryb. Podaj liczbę całkowitą odpowiadającą "
                                      "danemu trybowi 1, 2, 3, 4, 5 lub 6!")
        except ValueError:
            print("Błąd: Podaj liczbę odpowiadającą danemu trybowi 1, 2, 3, 4, 5 lub 6!")
        except PozaPrzedzialem as e:
            print(f"Błąd: {e}")
        except KeyboardInterrupt:
            print("Aplikacja została przerwana przez użytkownika")
            quit()


def otworz_plik():
    try:
        with open("hasla.txt", 'r') as dokument:
            return [linia.replace('\n', '').split() for linia in dokument.readlines()]
    except FileNotFoundError:
        print("Błąd: Plik 'hasla.txt' nie istnieje. Upewnij się, że zapisałeś jakieś hasła"
              "przed uruchomieniem tego trybu.")


def zobacz_wszystkie():
    linie = otworz_plik()
    for linia in linie:
        print(linia[0] + " --> " + linia[1] + " : " + linia[2])


def zobacz_konkretne(strona):
    strona = strona.lower()
    strony = []
    linie = otworz_plik()
    for linia in linie:
        strony.append(linia[0])
        if linia[0] == strona:
            print("login: " + linia[1] + ", hasło: " + linia[2])
            return
    print("Nie znaleziono strony")


def dodaj():
    try:
        strona = input("Podaj nazwę strony: ").lower()
        login = input(f"Podaj login do {strona}: ").lower()
        haslo = input("Podaj hasło: ").lower()
        if not strona or not login or not haslo:
            print("Błąd: Wszystkie pola (nazwa strony, login i hasło) muszą być wypełnione.")
            return
        with open("hasla.txt", 'a') as dokument:
            dokument.write(strona + " " + login + " " + haslo + "\n")
        print("Dodano pomyślnie hasło!")
    except IOError as e:
        print(f"Błąd, nie można dodać hasła: {e}")


def edytuj_haslo(strona):
    linie = otworz_plik()
    for i, linia in enumerate(linie):
        if linia[0] == strona:
            print(f"Aktualny login: {linia[1]}, Aktualne hasło: {linia[2]}")
            nowy_login = input("Podaj nowy login: ")
            nowe_haslo = input("Podaj nowe hasło: ")
            if not nowy_login and not nowe_haslo:
                print("Błąd: Musisz podać nowy login lub nowe hasło, aby dokonać edycji.")
                return
            linie[i] = [strona, nowy_login, nowe_haslo]
            with open("hasla.txt", 'w') as dokument:
                for l in linie:
                    dokument.write(" ".join(l) + "\n")
            print("Hasło zostało zaktualizowane.")
            return
    print("Nie znaleziono strony")


def usun(strona):
    try:
        nieznaleziono = True
        with open("hasla.txt", "r") as my_input:
            linie = my_input.readlines()
        for linia in linie:
            if linia.split()[0] == strona:
                nieznaleziono = False
        if nieznaleziono:
            print("Nie znaleziono strony")
            return
        with open("hasla.txt", "w") as my_output:
            for linia in linie:
                if linia.split()[0] != strona:
                    my_output.write(linia)
        print("Usunięto hasło pomyślnie")
    except FileNotFoundError:
        print("Błąd: Plik 'hasla.txt' nie istnieje. Upewnij się, że zapisałeś jakieś"
              "hasła przed uruchomieniem tego trybu.")
    except IOError as e:
        print(f"Błąd, nie można usunąć hasła: {e}")


def main():
    print("Witaj w menadżerze haseł")
    while True:
        try:
            print("---------------------------------------------------------------")
            match tryb_programu():
                case 1:
                    print("Wyświetlam wszystkie hasła poniżej")
                    zobacz_wszystkie()
                case 2:
                    strona = input("Podaj nazwę strony dla której wyświetlić hasło: ")
                    zobacz_konkretne(strona)
                case 3:
                    print("Proszę o podanie danych do wprowadzenia nowego hasła")
                    dodaj()
                case 4:
                    strona = input("Podaj stronę której hasło chcesz edytować: ")
                    edytuj_haslo(strona)
                case 5:
                    strona = input("Podaj nazwę strony dla której usunąć hasło: ")
                    usun(strona)
                case 6:
                    print("Dziękuję za skorzystanie z menadżera haseł!")
                    quit()
        except KeyboardInterrupt:
            print("Tryb zakończony przez użytkownika.")


if __name__ == "__main__":
    main()
