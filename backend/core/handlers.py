from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


ERROR_MESSAGES = {
    "missing": "Este campo es obligatorio, no puede estar vacío.",
    "string_type": "El valor debe ser un texto.",
    "string_too_long": "El valor ingresado supera el límite permitido",
    "int_parsing": "El valor debe ser un número entero válido.",
    "float_parsing": "El valor debe ser un número decimal válido.",
    "bool_parsing": "El valor debe ser un booleano (true/false).",
    "greater_than": "El número es demasiado pequeño.",
    "less_than": "El número es demasiado grande.",
}

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler personalizado para errores de validación (422).
    Traduce los mensajes técnicos a español para no perder detalles del error.

    """

    errores_procesados: list = []

    for error in exc.errors():
        # error es un diccionario (dentro de una lista de diccionarios por cada error):
        # {
        #   'type': 'missing', 'loc': ('body', 'codigo_chofer'), 'msg': 'Field required', 'input': { 'nombre': '123123123', 'fecha_ingreso': '2026-02-03' } 
        # },

        # Guarda los valores entrantes
        tipo_error: str = error.get("type")
        mensaje_original: str = error.get("msg")
        
        # Cambia los errores que coinciden en tipo_error con ERROR_MESSAGES
        mensaje_final = ERROR_MESSAGES.get(tipo_error)

        if not mensaje_final:
            # Si no está dentro del diccionario de errores customs y
            # viene de una Validation del modelo, le quita el "Value error" que trae por defecto
            if "Value error," in mensaje_original:
                mensaje_final = mensaje_original.split("Value error, ")[1].strip()
            else:
                # Si no está queda el mensaje por defecto
                mensaje_final = mensaje_original

        # print(error["input"])

        # loc_error = error["loc"][-1]
        # campos_ingresados: dict = error["input"]

        # if loc_error in campos_ingresados.keys():
        #     input_final = campos_ingresados.get(error["input"])
        # else:
        #     input_final = ""
            
        # print(input_final)

        errores_procesados.append(
            {
                "type": tipo_error,
                "loc": error["loc"],
                "msg": mensaje_final,
                "input": error["input"]
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": errores_procesados, "body": exc.body}),
    )


def configure_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler) # type: ignore