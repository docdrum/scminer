import PySimpleGUI as sg

import constdata as cd

class RockCalculator:
    def show(self):
        mass_row = [
            sg.Text("Mass"),
            sg.In(enable_events=True, key="-MASS-")
        ]

        mineral_percentage_row = [
            sg.Text("Mineral %"),
            sg.In(enable_events=True, key="-PERCENT-")
        ]

        mineral_names = tuple(cd.minerals.keys())
        num_minerals = len(mineral_names)
        mineral_row = [
            sg.Text("Mineral"),
            sg.Listbox(mineral_names, enable_events=True, size=(num_minerals, num_minerals),
                key="-MINERAL-", default_values="Quantainium")
        ]

        mineral_mass_row = [
            sg.Text("Mineral mass"),
            sg.In(disabled=True, key="-MASS-OUT-")
        ]

        value_row = [
            sg.Text("Mineral value"),
            sg.In(disabled=True, key="-VALUE-OUT-")
        ]

        layout = [
            mass_row,
            mineral_percentage_row,
            mineral_row,
            mineral_mass_row,
            value_row
        ]

        window = sg.Window("Rock Calculator", layout)

        def calc_mineral_mass(values):
            mineral_mass = 0
            mineral_percent = 0.0
            try:
                mineral_mass = int(values["-MASS-"])
                mineral_percent = float(values["-PERCENT-"])
            except ValueError:
                pass
            return mineral_mass * mineral_percent / 100.0
                
        while True:
            event, values = window.read()
            if event == "-EXIT-" or event == sg.WIN_CLOSED:
                break

            if event == "-MASS-" or event == "-PERCENT-" or event == "-MINERAL-":
                mineral_mass = calc_mineral_mass(values)
                window["-MASS-OUT-"].update(mineral_mass)
                mineral_value = 0
                try:
                    mineral_value = cd.minerals[values["-MINERAL-"][0]]
                except KeyError:
                    pass
                window["-VALUE-OUT-"].update(mineral_value * mineral_mass)

        window.close()

rc = RockCalculator()
rc.show()