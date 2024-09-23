# -*- coding: utf-8 -*-
# with open('../data/entrada.txt', 'r') as f:
#     lines = f.readlines()
#
# with open('../data/salida.txt', 'w') as f:
#     for line in lines:
#         data = line.strip().split(', ')
#         if len(data) == 8:  # verificar que la línea tenga exactamente 8 valores
#             date = '23/04/2023'
#             league = data[0].strip()
#             team1 = data[1].strip()
#             team2 = data[2].strip()
#             value1 = data[3].strip()
#             bet = data[4].strip()
#             odd1 = data[5].strip()
#             odd2 = data[6].strip()
#             stake = data[7].strip()
#             new_line = f"{date};{league};{team1};{team2};{value1};{bet};{odd1};{odd2};{stake}\n"
#             f.write(new_line)
#         else:
#             print(f"Línea inválida: {line}")

with open('../data/entrada.txt', 'r') as f:
    lines = f.readlines()
with open('../data/salida.txt', 'w') as f:
    for line in lines:
        data = line.strip().split(', ')
        if len(data) == 11:  # verificar que la línea tenga exactamente 8 valores
            date = '04/05/2023'
            competicion = data[0].strip()
            local = data[7].strip()
            visitante = data[8].strip()
            minuto = data[3].strip()
            cornersActuales = ""
            media = data[10].strip()
            linea = data[4].strip()
            cuota = data[5].strip()
            probabilidad = data[6].strip()
            partidos = data[9].strip()
            cornersFinales = ""
            resultadoApuesta = ""
            new_line = f"{date};{competicion};{local};{visitante};{minuto};{cornersActuales};{media};{linea};{cuota};{probabilidad};{partidos};{cornersFinales};{resultadoApuesta}\n"
            f.write(new_line)
        else:
            print(f"Línea inválida: {line}")