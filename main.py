import global_functions
import trasa
import nextbike


def wyznacz_trase():
    trasa.start_app(chosen_city, station_names, station_localizations)


def wyznacz_stację():
    nextbike.start_app(chosen_city, station_names, station_localizations)


chosen_city, station_names, station_localizations = global_functions.main()

main_options = {
    'SPRAWDŹ LICZBĘ ROWERÓW': wyznacz_stację,
    'ZNAJDŹ TRASĘ': wyznacz_trase
}

print('Co chcesz zrobić:')
main_options[global_functions.choice(list(main_options), False)]()
