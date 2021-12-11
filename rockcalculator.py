import PySimpleGUI as sg

minerals = {
    "Quantanium": 88.0,
    "Bexalite": 40.66,
    "Taranite": 32.58,
    "Borase": 32.58,
    "Laranite": 31.02,
    "Agricium": 27.50,
    "Hephaestanite": 14.76,
    "Titanium": 8.94,
    "Diamond": 7.36,
    "Gold": 6.4,
    "Copper": 5.74,
    "Beryl": 4.42,
    "Tungsten": 4.1,
    "Corundum": 2.7,
    "Quartz": 1.56,
    "Aluminium": 1.34
}

mass_row = [
    sg.Text("Mass"),
    sg.In(enable_events=True, key="-MASS-")
]

mineral_percentage_row = [
    sg.Text("Mineral %"),
    sg.In(enable_events=True, key="-PERCENT-")
]

mineral_names = tuple(minerals.keys())
mineral_row = [
    sg.Text("Mineral"),
    sg.Listbox(mineral_names, enable_events=True, size=(len(mineral_names),len(mineral_names)), key="-MINERAL-", default_values="Quantainium")
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
            mineral_value = minerals[values["-MINERAL-"][0]]
        except KeyError:
            pass
        window["-VALUE-OUT-"].update(mineral_value * mineral_mass)

window.close()