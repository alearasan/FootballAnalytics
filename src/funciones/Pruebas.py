import csv

# result = [('Huracán', '2023-03-10 00:00', 'Sporting Cristal', 'https://cornerprobet.com/analysis/Huracan-Sporting-Cristal/qgo8j'),
#           ('Deportes Tolima', '2023-03-10 00:00', 'Junior', 'https://cornerprobet.com/analysis/Deportes-Tolima-Junior/qf77r'),
#           ('Emelec', '2023-03-10 00:00', 'Deportivo Cuenca', 'https://cornerprobet.com/analysis/Emelec-Deportivo-Cuenca/qf781'),
#           ('SWA Sharks', '2023-03-10 00:00', 'Teachers', 'https://cornerprobet.com/analysis/SWA-Sharks-Teachers/qgsm5'),
#           ('Fanalamanga', '2023-03-10 00:00', 'COSFA', 'https://cornerprobet.com/analysis/Fanalamanga-COSFA/qe03a'),
#           ('Santos', '2023-03-10 00:30', 'Iguatu', 'https://cornerprobet.com/analysis/Santos-Iguatu/qgecm'),
#           ('Diriangén', '2023-03-10 01:00', 'Matagalpa', 'https://cornerprobet.com/analysis/Diriangen-Matagalpa/qgrm0'),
#           ('Real Estelí', '2023-03-10 01:00', 'Jalapa', 'https://cornerprobet.com/analysis/Real-Esteli-Jalapa/qgrls'),
#           ('Alianza Petrolera', '2023-03-10 01:00', 'Deportivo Pasto', 'https://cornerprobet.com/analysis/Alianza-Petrolera-Deportivo-Pasto/qfomk')]
#
# # abrir el archivo csv en modo escritura
# with open('Encuentros(10-03-2023).csv', mode='w', newline='') as archivo_csv:
#     # crear un objeto writer usando el separador ";"
#     writer = csv.writer(archivo_csv, delimiter=';')
#     # escribir las tuplas en el archivo csv
#     writer.writerows(result)

#Numero de corners mitad asiatico bet365
selector_mitad_asiatico = "body > div:nth-child(1) > div > div.wc-WebConsoleModule_SiteContainer > div.wc-PageView > div.wc-PageView_Main.wc-InPlayPageResponsive_PageViewMain > div > div > div > div > div > div.ipe-EventViewView_Center.ipe-EventViewDetail > div > div.ipe-EventViewDetail_ContentContainer > div.ipe-EventViewDetail_MarketGrid.gl-MarketGrid.gl-MarketGrid-wide > div:nth-child(21) > div.gl-MarketGroup_Wrapper > div > div.gl-Market.gl-Market_General.gl-Market_General-columnheader.gl-Market_General-haslabels.gl-Market_General-pwidth25 > div.srb-ParticipantLabelCentered.gl-Market_General-cn1 > div"

#Si selector_mitad_asiatico <= x corners mande alerta 

with open("../data/Encuentros(13-03-2023).csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    header = next(reader)  # Leer la primera fila (encabezado)

    # Encontrar el índice de la columna "Analisis" en el encabezado
    analisis_index = header.index("Analisis")

    # Abrir el nuevo archivo CSV y escribir el encabezado
    with open("../data/Analisis(13-03-2023).csv", "w", newline="", encoding="utf-8") as fw:
        writer = csv.writer(fw)
        writer.writerow(["Analisis"])

        # Leer las filas del archivo original y escribir solo la columna "Analisis"
        for row in reader:
            analisis = row[analisis_index]
            writer.writerow([analisis])