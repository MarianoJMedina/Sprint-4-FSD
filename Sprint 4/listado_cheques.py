"""

SPRING 4 CORREGIDO 20/08/2022

"""

import sys
import csv
import os
from datetime import datetime

parametros = sys.argv[1:]
nombre_archivo = parametros[0]
dni = parametros[1]
salida = parametros[2]
tipo_cheque = parametros[3]
estado = None
rango_fecha = None

if len(parametros) == 5:
    opcion = parametros[4]
    tipo_estado = ["PENDIENTE", "APROBADO", "RECHAZADO"]
    if opcion in tipo_estado:
        estado = opcion
    else:
        rango_fecha = opcion.split(':')
elif len(parametros) == 6:
    estado = parametros[4]
    rango_fecha = parametros[5].split(':')


if rango_fecha:
    rango_fecha_inicio = datetime.timestamp(
        datetime.strftime(rango_fecha[0], '%d-%m-%Y'))
    rango_fecha_fin = datetime.timestamp(
        datetime.strftime(rango_fecha[1], '%d-%m-%Y'))
res = []

with open(nombre_archivo, 'r') as archivo_csv:
    csv_reader = csv.reader(archivo_csv, delimiter=',')
    for fila in csv_reader:
        dni_aux = fila[8]
        tipo_cheque_aux = fila[9]
        estado_aux = fila[10]
        fecha = fila[6]

        if dni_aux != dni or tipo_cheque_aux != tipo_cheque:
            continue
        if estado is not None and estado != estado_aux:
            continue
        if rango_fecha and (fecha < rango_fecha_inicio or fecha > rango_fecha_fin):
            continue

        res.append(fila)

vistos = set()
for nro_fila, fila in enumerate(res):
    nro_cheque = fila[0]
    nro_cuenta = fila[3]
    dni_aux = fila[8]
    if(nro_cheque, nro_cuenta, dni_aux) in vistos:
        res.append(
            f"Se repiten los datos en dos cheques. Se lo puede ver en la fila {nro_fila}")
    else:
        vistos.add((nro_cheque, nro_cuenta, dni_aux))


if salida == "PANTALLA":
    os.system('cls')
    for fila in res:
        print(','.join(fila))
elif salida == "CSV":
    datos_filtrados = [[(fila[3], fila[5], fila[6], fila[7]) for fila in res]]
    dt = datetime.now()
    dt = dt.strftime("%d-%m-%Y")
    with open(f'{fila[8]}-{dt}.csv', 'w', newline='') as archivo_salida_csv:
        writer = csv.writer(archivo_salida_csv)
        writer.writerows(datos_filtrados)
