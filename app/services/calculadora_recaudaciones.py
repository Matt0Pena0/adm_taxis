from decimal import Decimal
from typing import Dict


class CalculadoraRecaudacion:
    PORCENTAJE_SUELDO = Decimal("0.29")
    PORCENTAJE_APORTE = Decimal("0.19")

    @staticmethod
    def calcular_liquidacion(
        total_recaudado: Decimal,
        combustible: Decimal,
        otros_gastos: Decimal,
        km_entrada: int,
        km_salida: int,
        h13: Decimal,
        credito: Decimal
    ) -> Dict[str, Decimal]:
        """
        Recibe los valores y retorna un diccionario
        con el desglose financiero listo para guardar en BD.
        """

        salario = total_recaudado*CalculadoraRecaudacion.PORCENTAJE_SUELDO
        total_gastos = salario + combustible + otros_gastos
        liquido = total_recaudado - total_gastos
        aportes = salario * CalculadoraRecaudacion.PORCENTAJE_APORTE
        sub_total = liquido + aportes
        total_entregar = sub_total - h13 - credito

        km_totales = km_salida - km_entrada
        if km_totales > 0:
            rendimiento = total_recaudado / km_totales
        else:
            rendimiento = Decimal("0.00")

        return{
            "salario": salario,
            "total_gastos" : total_gastos,
            "liquido": liquido,
            "aportes": aportes,
            "sub_total": sub_total,
            "total_entregar": total_entregar,
            "km_totales": Decimal(km_totales),
            "rendimiento": rendimiento
        }


# res = CalculadoraRecaudacion.calcular_liquidacion(
#     total_recaudado=Decimal("5000"),
#     combustible=Decimal("1500"),
#     otros_gastos=Decimal("0"),
#     km_entrada=1000,
#     km_salida=1150, # 150km recorridos
#     h13=Decimal("0"),
#     credito=Decimal("0")
# )
# print(f"Total a Entregar: {res['total_entregar']}") 
# print(f"Rendimiento $/km: {res['rendimiento']:.2f}")