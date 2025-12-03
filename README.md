# Bioreactor-Design-Optimization-Tool
# Herramienta de Optimización para el Diseño de Biorreactores

Este repositorio contiene un script de Python diseñado para determinar las **condiciones de operación óptimas** (principalmente la velocidad de agitación, $N_i$) en un biorreactor, asegurando que se cumplan las **restricciones de transferencia de calor** y los **límites de potencia de agitación**.

El programa es crucial para procesos que involucran fluidos no Newtonianos y requieren un estricto control térmico para la cinética microbiana, como la producción de biomasa.

## Metodología de Optimización

El script realiza un proceso iterativo de la velocidad de agitación ($N_i$) y se detiene cuando se cumplen dos criterios de diseño:

1.  **Restricción de Transferencia de Calor:** El Área de Enfriamiento Requerida ($A_{\text{requerida}}$) para remover el calor metabólico debe ser menor o igual al Área Real de la Chaqueta Disponible ($A_{\text{real}}$).
2.  **Restricción de Potencia:** La Potencia Gaseada calculada ($P_g$) debe estar dentro de los límites operativos definidos ($P_{g, \text{Mín}} \leq P_g \leq P_{g, \text{Máx}}$).

### Ecuaciones y Correlaciones Clave

El cálculo involucra las siguientes relaciones fundamentales:

* **Viscosidad Aparente ($\mu$):** Se modela como una función de la velocidad de cizalla (shear rate) del impulsor de Rushton.
* **Número de Reynolds ($N_{Re}$):** Utiliza la viscosidad aparente para clasificar el régimen de flujo.
* **Área de Enfriamiento Requerida ($A_{\text{requerida}}$):** Calculada a partir del flujo de calor metabólico (basado en el coeficiente de entalpía y la cinética de crecimiento) y la transferencia de calor del sistema ($U$ y $\Delta T$).
* **Potencia Gaseada ($P_g$):** Determinada a partir del Número de Potencia ($N_p$) y el Número de Aireación ($N_a$).
* **Coeficiente Volumétrico de Oxígeno ($k_{La}$):** Calculado a partir de la $P_g$ óptima y la velocidad superficial del gas ($U_g$) para verificar el cumplimiento del requerimiento de oxígeno.

## Uso y Ejecución del Script

### Requisitos

El script es compatible con Python 3 y solo requiere la librería estándar `math`.

```bash
# No se requiere instalación de paquetes adicionales.

