from decimal import Decimal, ROUND_HALF_UP
from typing import Dict
from enum import Enum


class CalculadoraRecaudacion:
    """
    Motor de cálculo financiero para las liquidaciones diarias.
    
    Centraliza toda la lógica de negocio, porcentajes y fórmulas matemáticas
    para asegurar consistencia en toda la aplicación. Evita utilizar fórmulas 
    en los routers o el frontend.
    
    **Constantes de Negocio:**
    - `Porcentaje.SUELDO` (29%): Parte de la recaudación bruta que corresponde al salario base.
    - `Porcentaje.APORTE` (19%): Cargas sociales aplicadas sobre el salario calculado.
    """

    class Porcentaje (Enum):
        SUELDO = Decimal("0.29")
        APORTE = Decimal("0.19")

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
        Procesa los datos crudos del turno y genera el desglose financiero completo.

        Realiza los siguientes cálculos secuenciales:
        
        1. **Salario**: $Recaudación * Porcentaje.SUELDO (0.29$)
        2. **Gastos Totales**: $Salario + Combustible + Otros$
        3. **Líquido**: $Recaudación - GastosTotales$
        4. **Aportes**: $Salario * Porcentaje.APORTE (0.19$)
        5. **SubTotal**: $Líquido + Aportes$
        6. **Total a Entregar**: $SubTotal - H13 - Crédito$
        
        Args:
            total_recaudado (Decimal): Dinero bruto ingresado por el reloj.
            combustible (Decimal): Gasto en combustible del turno.
            otros_gastos (Decimal): Lavados, pinchaduras, insumos.
            km_entrada (int): Odómetro al inicio.
            km_salida (int): Odómetro al final.
            h13 (Decimal): Descuentos por concepto H13 (pagos diferidos).
            credito (Decimal): Descuentos por débitos y créditos (POS).

        Returns:
            Dict[str, Decimal]: Diccionario con todas las claves calculadas 
            listas para ser inyectadas en el modelo `Recaudacion`.
        """

        salario = total_recaudado*CalculadoraRecaudacion.Porcentaje.SUELDO.value
        total_gastos = salario + combustible + otros_gastos
        liquido = total_recaudado - total_gastos
        aportes = salario * CalculadoraRecaudacion.Porcentaje.APORTE.value
        sub_total = liquido + aportes
        total_entregar = sub_total - h13 - credito

        km_totales = km_salida - km_entrada
        if km_totales > 0:
            rendimiento = total_recaudado / km_totales
        else:
            rendimiento = Decimal("0.00")

        return{
            "salario": salario.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "total_gastos" : total_gastos.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "liquido": liquido.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "aportes": aportes.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "sub_total": sub_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "total_entregar": total_entregar.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "km_totales": Decimal(km_totales).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "rendimiento": rendimiento.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
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