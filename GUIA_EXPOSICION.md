# Guía de exposición y estudio

## Introducción

Una posible presentación, que puedes adaptar a tus motivos reales:

> Este proyecto incluye una calculadora multifuncional y Python Bank, un simulador de cajero. La calculadora resuelve operaciones y conserva resultados; el banco permite registrar entradas y salidas de dinero ficticio. Son ejemplos cotidianos con los que puedo mostrar funciones, condicionales, ciclos, estructuras de datos y archivos.

Agrega con tus palabras por qué elegiste estos programas. No es necesario afirmar experiencias o aprendizajes que todavía no has tenido. Primero ejecútalos, sigue los datos y practica modificar una función pequeña.

## Funcionamiento general

### Calculadora

1. `main()` carga el TXT; si no existe, recibe una lista vacía.
2. El menú se repite con `while True` hasta seleccionar `0`.
3. En un cálculo, `pedir_numero()` valida los operandos; `M` obtiene el último resultado.
4. Una función matemática retorna el resultado y `validar_resultado()` comprueba que sea finito.
5. `registrar_operacion()` prepara una tupla, guarda la nueva lista y después modifica el historial en memoria.
6. Las consultas leen esa lista. La memoria y las estadísticas siempre se calculan a partir de ella.
7. Una entrada incorrecta informa del problema; la opción de salir muestra la despedida.

### Python Bank

1. `crear_cuenta()` prepara el diccionario con datos ficticios.
2. `cargar_movimientos()` verifica cada línea y recupera el saldo. Un TXT inválido impide continuar.
3. `iniciar_sesion()` devuelve `True` si las credenciales coinciden; tres fallos producen `False` y finalizan el programa.
4. El menú permite consultar, depositar, retirar, proyectar ahorro y generar comprobantes.
5. Depósitos y retiros requieren una cantidad válida y confirmación. El retiro también requiere fondos suficientes.
6. Se guarda antes de actualizar saldo y movimientos en memoria.
7. Cerrar sesión cambia el booleano `sesion_activa` a `False`; el siguiente ciclo solicita las credenciales nuevamente. Salir termina el ciclo.

## Funciones más importantes

### Calculadora

| Función | Parámetros | Retorno y responsabilidad |
| --- | --- | --- |
| `sumar`, `restar`, `multiplicar`, `dividir`, `division_entera`, `calcular_modulo`, `calcular_potencia` | `a`, `b` | Devuelven el cálculo; algunas rechazan dominios inválidos con `ValueError` |
| `raiz_cuadrada` | `numero` | Devuelve la raíz de un número no negativo |
| `calcular_porcentaje` | `numero`, `porcentaje` | Devuelve la parte correspondiente al porcentaje |
| `pedir_numero` | `mensaje`, `memoria=None` | Devuelve un número finito o la memoria; repite la pregunta ante entradas inválidas |
| `validar_resultado` | `resultado` | Devuelve el mismo número si es finito; en caso contrario lanza `ValueError` |
| `realizar_operacion` | `opcion`, `historial`, `ruta` | Coordina entrada, función matemática, guardado e impresión; no retorna un resultado útil |
| `analizar_lista` | `numeros` | Devuelve un diccionario de estadísticas; no imprime ni modifica la lista |
| `tabla_multiplicar` | `numero` | Devuelve una lista de diez tuplas con multiplicador y producto |
| `cargar_historial` | `ruta` | Devuelve una lista de registros validados |
| `registrar_operacion` | `historial`, `tipo`, `expresion`, `resultado`, `ruta` | Guarda y luego modifica la lista; no retorna un resultado útil |
| `guardar_historial` | `ruta`, `historial` | Escribe el temporal y sustituye el TXT; comunica un fallo mediante una excepción |
| `obtener_memoria` | `historial` | Devuelve el último resultado o `None` |
| `obtener_estadisticas` | `historial` | Devuelve el diccionario de conteos |
| `borrar_historial` | `historial`, `ruta` | Pide confirmación y vacía archivo y lista si se acepta y se logra guardar |

### Banco

| Función | Parámetros | Retorno y responsabilidad |
| --- | --- | --- |
| `crear_cuenta` | Ninguno | Devuelve un nuevo diccionario con datos de demostración |
| `iniciar_sesion` | `cuenta` | Devuelve un booleano; controla los tres intentos |
| `pedir_cantidad` | `mensaje` | Devuelve un entero positivo |
| `cargar_movimientos` | `ruta`, `saldo_inicial` | Devuelve dos valores: lista de movimientos y saldo recuperado |
| `depositar`, `retirar` | `cuenta`, `movimientos`, `ruta` | Solicitan y confirman la operación, llaman al registro e imprimen; no retornan un resultado útil |
| `registrar_movimiento` | `cuenta`, `movimientos`, `tipo`, `cantidad`, `ruta` | Devuelve la tupla guardada; actualiza lista y cuenta después de guardar |
| `guardar_movimientos` | `ruta`, `movimientos` | Guarda la copia completa de forma controlada; un fallo se comunica con una excepción |
| `filtrar_movimientos` | `movimientos`, `tipo` | Devuelve una nueva lista del tipo solicitado |
| `calcular_resumen` | `movimientos` | Devuelve un diccionario con totales, conteos, máximos y promedios |
| `proyectar_ahorro` | `saldo`, `cantidad_mensual`, `meses` | Devuelve una lista de pares `(mes, saldo_proyectado)` |
| `generar_comprobante` | `cuenta`, `movimientos`, `ruta` | Devuelve `True` si escribió y `False` si no hay movimientos; errores de archivo se atienden en `main()` |

La separación permite leer el menú sin mezclarlo con todos los detalles y comprobar cálculos sin escribir respuestas en consola. Las funciones de presentación imprimen; las de cálculo retornan. Una función sin `return` explícito devuelve `None`.

## Demostración de la calculadora

Para empezar desde cero sin borrar tus datos habituales, copia `Calculadora/calculadora.py` a una carpeta de demostración vacía. Su historial se creará junto a esa copia.

1. Ejecuta `python Calculadora/calculadora.py` desde la raíz, o la ruta de tu copia.
2. Elige `1`, escribe `8` y `2`: resultado `10`.
3. Elige `15`: memoria `10`. Elige `3`, escribe `M` y `3`: resultado `30`.
4. Elige `4`, escribe `10` y `0`: se informa el error; no se agrega un registro.
5. Elige `10`, escribe `7`: muestra desde `7 x 1` hasta `7 x 10 = 70`.
6. Elige `12`, cantidad `4`, números `1`, `2`, `2`, `7`: total `12`, promedio `3`, mayor `7`, menor `1`, superiores `[7.0]` y tres valores únicos.
7. Elige `13` y `1`: muestra suma y multiplicación. Elige `13` y `2` para explicar las últimas cinco.
8. Elige `14`: total `2`, una suma y una multiplicación. Las dos empatan como más utilizadas. La división fallida no cuenta.
9. Elige `0`, vuelve a abrir y consulta `13`, `14` y `15`: permanecen el historial, los conteos y la memoria `30`.
10. Opcionalmente, en tu copia de demostración, elige `16`, responde primero `NO` y después repite con `SI`. Explica que se reinician historial, memoria y estadísticas juntos.

Los resultados esperados suponen que la carpeta de demostración empezó sin historial. El orden visual de un set no es parte del resultado: importa qué valores contiene.

## Demostración del cajero

Para garantizar el saldo inicial, copia `Cajero/cajero.py` a otra carpeta de demostración vacía. No borres movimientos de uso habitual para preparar la exposición.

1. Ejecuta `python Cajero/cajero.py` desde la raíz, o la ruta de tu copia. Ingresa `cliente01` y `1234`.
2. Elige `1`: saldo inicial `$1,000 MXN`.
3. Elige `2`, cantidad `500`, confirma `SI`: saldo `$1,500 MXN`.
4. Elige `3`, cantidad `200`, confirma `SI`: saldo `$1,300 MXN`.
5. Elige `3` e intenta retirar `2000`: fondos insuficientes, sin cambios.
6. Elige `4` y prueba las consultas `1`, `2`, `3` y `4`, regresando al menú principal entre ellas.
7. Elige `6`: depositado `500`, retirado `200`, dos movimientos, máximo y promedio de depósitos `500`, máximo y promedio de retiros `200`.
8. Elige `7`, ahorro mensual `100`, meses `3`: proyecciones `1400`, `1500`, `1600`. Consulta el saldo con `1`: sigue siendo `1300`.
9. Elige `8` y abre `comprobante.txt` junto al programa: corresponde al retiro de `200` y saldo de `1300`.
10. Elige `9` para cerrar sesión y vuelve a entrar. Después elige `0`, reinicia el programa y comprueba que conserva `1300` y los dos movimientos.

Puedes mostrar los tres intentos fallidos en una ejecución adicional. El límite se aplica a cada proceso de autenticación, no es un bloqueo permanente de la cuenta.

## Preguntas del profesor y respuestas para comprender

**¿Por qué utilizaste `while` para el menú?**

No sabemos cuántas operaciones hará la persona. El ciclo repite el menú y termina con `break` cuando elige salir. No usa recursividad.

**¿Cuál es la diferencia entre `for` y `while`?**

`for` recorre una colección o un rango: diez productos en la calculadora o tres intentos de acceso. `while` repite mientras se cumpla una condición: se usa para el menú y para volver a pedir una entrada válida.

**¿Por qué utilizaste listas para el historial?**

Necesito conservar el orden y agregar registros con `append()`. También puedo recorrerlos y seleccionar los últimos cinco con `historial[-5:]`.

**¿Por qué cada movimiento se representa mediante una tupla?**

Tiene cinco campos que describen un evento ya registrado. Su estructura fija facilita desempaquetarlos como `tipo, cantidad, fecha, hora, saldo`. No necesito editar esos campos durante el uso normal.

**¿Cuál es la diferencia entre una lista y una tupla?**

La lista es mutable: agrego movimientos. La tupla es inmutable: no reasigno uno de sus elementos. Esto no protege el archivo frente a una edición externa; solo expresa cómo trato los datos en Python.

**¿Para qué utilizaste sets?**

Eliminan repetidos. En la calculadora obtengo valores únicos y tipos usados; `set(OPERACIONES) - utilizados` muestra lo que falta probar. En el banco muestro los tipos presentes en la consulta sin repetirlos.

**¿Por qué utilizaste diccionarios?**

Las claves dan significado a cada valor. `cuenta['saldo']` es más claro que recordar una posición numérica. Las estadísticas relacionan el nombre de una operación con su conteo.

**¿Cuál es la diferencia entre `print()` y `return`?**

`print()` muestra información. `return` entrega un valor a quien llamó la función. `sumar(8, 2)` devuelve `10`; otra función puede guardarlo, imprimirlo o usarlo en una prueba.

**¿Qué es una variable local?**

Una variable creada dentro de una función. `saldo_proyectado` pertenece a `proyectar_ahorro()` y no cambia `cuenta['saldo']`. En cambio, una lista o diccionario pasado como argumento puede modificarse desde la función: por eso el registro actualiza esos datos solo después de guardar.

**¿Cómo evitas dividir entre cero?**

`dividir()`, `division_entera()` y `calcular_modulo()` revisan si `b == 0` y lanzan `ValueError`. `main()` muestra el mensaje; no se llega a `registrar_operacion()`.

**¿Cómo evitas retirar más dinero del disponible?**

`retirar()` compara la cantidad con el saldo antes de confirmar. `registrar_movimiento()` vuelve a verificarlo porque también puede llamarse directamente. La validación central evita registrar un retiro inválido por otro recorrido del código.

**¿Cómo se conserva el saldo al cerrar?**

Cada movimiento guarda cantidad y saldo resultante. Al iniciar se recorre `movimientos.txt`, se parte de `1000` y se verifica cada saldo. No existe un segundo archivo de saldo que pueda quedar desactualizado.

**¿Qué diferencia existe entre `r`, `w` y `a`?**

`r` lee, `w` escribe reemplazando y `a` agrega al final. Aquí se lee con `r` y se usa `w` sobre una copia temporal completa. No usamos `a` para los historiales porque un fallo durante una adición podría dejar el último registro incompleto. El comprobante usa `w` porque solo conservamos el último solicitado.

**¿Para qué sirve `try/except`?**

Permite responder a errores previstos. Por ejemplo, convertir `hola` con `int()` produce `ValueError`; el programa lo captura y vuelve a pedir una cantidad. Un `FileNotFoundError` durante la primera carga significa que todavía no hay datos guardados.

**¿Por qué utilizaste funciones?**

Cada función concentra una tarea que puedo explicar, reutilizar y comprobar. Cambiar el formato monetario se hace en `formato_pesos()` sin reescribir todos los menús.

**¿Por qué no utilizaste una base de datos?**

El alcance es pequeño y académico. Los archivos TXT permiten practicar apertura, escritura, lectura y excepciones con las herramientas del semestre, sin dependencias.

**¿Por qué corresponde a programación estructurada?**

El flujo se construye con secuencias, decisiones `if/elif/else`, ciclos `for/while` y funciones. No se definieron clases, interfaces gráficas ni frameworks.

**¿Qué ocurre si falla el guardado?**

Se escribe primero un TXT temporal. Solo al terminar se sustituye el archivo principal y se actualiza la memoria. Si falla la escritura o la sustitución, el menú informa del error y no confirma un movimiento. Las pruebas simulan esos fallos y comprueban saldo, lista y archivo anterior.

**¿Para qué sirve `if __name__ == '__main__'`?**

Llama a `main()` cuando ejecuto el archivo directamente. Al importarlo desde `pruebas.py`, puedo probar sus funciones sin que aparezca el menú automáticamente.

**¿Por qué la calculadora usa decimales y el banco enteros?**

La calculadora necesita operar con números como `2.5`. El banco trabaja deliberadamente con pesos completos para evitar aproximaciones en los movimientos. Sus promedios sí pueden ser decimales, pero no modifican el saldo.

## Preparación y retroalimentación

- Ejecuta `python pruebas.py` antes de presentar. Las herramientas `subprocess` y `unittest.mock` pertenecen al archivo auxiliar de pruebas, no a la lógica de las aplicaciones.
- Abre los dos fuentes y localiza `main()`, una función que retorna valores, un ciclo, una lista, una tupla, un set, un diccionario y un bloque `with open()`.
- Explica el recorrido de un depósito desde la entrada hasta el TXT y el de una división inválida hasta el mensaje de error.
- Practica la demostración con copias vacías y conserva tus archivos habituales.
- Anota la sugerencia del profesor, identifica la función afectada, realiza el cambio y repite las pruebas pertinentes.

Registro para completar: **sugerencia recibida → función o documento afectado → cambio realizado → resultado de la comprobación**.
