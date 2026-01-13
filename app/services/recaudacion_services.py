from datetime import date
from enum import Enum
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.chofer import Chofer, EstadoChofer
from app.models.coche import Coche #, EstadoCoche
from app.models.recaudacion import Recaudacion, RecaudacionCreate


class RecaudacionService:
    """
    Gestor de lógica de negocio para Recaudaciones.

    Centraliza validacion de estado y la orquestación de cálculos financieros.
    """


    class Porcentaje(Enum):
        """
        **Constantes de Negocio:**
        - `Porcentaje.SUELDO` (29%): Parte de la recaudación bruta que corresponde al salario base.
        - `Porcentaje.APORTE` (19%): Cargas sociales aplicadas sobre el salario calculado.
        """
        SUELDO = Decimal("0.29")
        APORTE = Decimal("0.19")

    def __init__(self, session: AsyncSession):
        self.session = session


    @classmethod
    def calcular_liquidacion(
        cls,
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

        salario = total_recaudado*cls.Porcentaje.SUELDO.value
        total_gastos = salario + combustible + otros_gastos
        liquido = total_recaudado - total_gastos
        aportes = salario * cls.Porcentaje.APORTE.value
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
            "km_totales": Decimal(km_totales),
            "rendimiento": rendimiento.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        }


    async def crear_nueva_recaudacion(self, datos_entrada: RecaudacionCreate) -> Recaudacion:
        """
        Orquesta todo el proceso de creación.

        Pasos:
        1. Verificar existencia y estado de Chofer y Coche.
        2. Validar continuidad de kilometraje.
        3. Calcular montons financieros. Llamando a `calcular_liquidacion`
        4. Persisitir en BD.

        Args:
            **datos_entrada**: `RecaudacionCreate`

        Returns:
            **nueva_recaudacion**: `Recaudacion`

        Raises:
            HTTPException (400): Si hay inconsistencia de datos o estado.
            HTTPException (404): Si no existen las entidades relacionadas.
        """


        # 1. Validar Entidades y Estados
        chofer, coche = await self._validar_entidades(datos_entrada.chofer_id, datos_entrada.coche_id)

        # 2. Validar Conitnuidad de Kilometraje
        # await self._validar_continuidad_kilometraje(datos_entrada.chofer_id, datos_entrada.coche_id)

        # 3. Realizar Cálculos Financieros.
        liquidacion_calculada = self.calcular_liquidacion(
            total_recaudado=datos_entrada.total_recaudado,
            combustible=datos_entrada.combustible,
            otros_gastos=datos_entrada.otros_gastos,
            km_entrada=datos_entrada.km_entrada,
            km_salida=datos_entrada.km_salida,
            h13=datos_entrada.h13,
            credito=datos_entrada.credito,
        )

        liquidacon_completa = { # type: ignore
            **datos_entrada.model_dump(exclude={"id"}),
            **liquidacion_calculada,
            "fecha_recibida": date.today()
        }

        # 4. Crear Instancia y Guardar
        nueva_recaudacion = Recaudacion.model_validate(liquidacon_completa)

        try:
            self.session.add(nueva_recaudacion)

        except Exception as e:
            await self.session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la recaudación: {str(e)}"
            )

        # Actualizar el kilometraje del coche.
        if coche.kilometros < datos_entrada.km_salida:
            coche.kilometros = datos_entrada.km_salida
        self.session.add(coche)

        await self.session.commit()
        await self.session.refresh(nueva_recaudacion)

        return nueva_recaudacion


    async def _validar_entidades(self, chofer_id: int, coche_id: int) -> tuple[Chofer, Coche]:
        """
        Valida que las entidades existan y estén activos.
        Retorna las instancias.
        """
        chofer = await self.session.get(Chofer, chofer_id)
        if not chofer or chofer.estado != EstadoChofer.ACTIVO:
            raise HTTPException(
                status_code=400,
                detail=f"Chofer no válido")

        coche = await self.session.get(Coche, coche_id)
        if not coche: 
        # or Coche.estado != (EstadoCoche.ACTIVO or EstadoCoche.DISPONIBLE):
            raise HTTPException(
                status_code=400,
                detail=f"Coche no válido")

        return chofer, coche


    # async def _validar_continuidad_kilometraje(self, coche_id: int, km_entrada: int):
    #     pass