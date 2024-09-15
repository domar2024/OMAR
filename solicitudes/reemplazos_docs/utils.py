def hora_completa_24_a_12_horas_y_minutos(hora24):  # 21:00:00 - 9:00 PM
    lista_3_tiempos = hora24.split(':')
    horas = int(lista_3_tiempos[0])
    if (horas > 12):
        r_horas = horas - 12
        meridiano = "PM"
    else:
        r_horas = horas
        meridiano = "AM"

    return f"{str(r_horas)}:{lista_3_tiempos[1]} {meridiano}"
