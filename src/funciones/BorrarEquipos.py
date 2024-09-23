
from Lectura import * 



if __name__ == '__main__':
    encuentros = lee_encuentros_selenium("../data/Encuentros(16-03-2023).csv")

    juanma = []
    with open("../data/TextoJuanma.txt", 'r',encoding = "utf-8") as archivo:
        for linea in archivo:
            juanma.append(linea.split(", ")[3][1:-1])
    
    # print(juanma)
    
    filtrado = [e for e in encuentros if e.local not in juanma]
    
    print(filtrado)
    
    with open("../data/EncuentrosFiltrados(16-03-2023).csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter = ";")
        writer.writerow(["Local", "Tiempo", "Visitante", "Analisis"])
        for elemento in filtrado:
            print(elemento)
            writer.writerow(elemento)
















