# Optimización de Condiciones de Operación en Biorreactor

Este script en Python está diseñado para calcular y optimizar la velocidad de agitación ($N_i$) en un biorreactor agitado y aireado, asegurando que se cumplan las condiciones de **transferencia de calor** y los **límites de potencia** de aireación.

---

## Variables del Modelo

El script inicializa una serie de constantes y parámetros físicos y de diseño del biorreactor:

| Variable | Descripción | Unidad |
| :--- | :--- | :--- |
| `T` | Diámetro del biorreactor | $m$ |
| `H` | Altura del biorreactor | $m$ |
| `Vop` | Volumen operativo | $m^3$ |
| `rho` | Densidad del fluido (agua) | $kg/m^3$ |
| `D_impulsor` | Diámetro del impulsor | $m$ |
| `num_imp` | Número de impulsores | - |
| `Fa` | Flujo de aireación | $m^3/s$ |
| `Pg_Min`, `Pg_Max` | Límites de potencia gaseada | $W$ |
| `µ_max` | Velocidad de crecimiento máxima | $h^{-1}$ |
| `x` | Máxima concentración de biomasa | $kg_{biomasa}/L$ |
| `Y` | Coeficiente de rendimiento $\frac{kg_{biomasa}}{kg_{oxígeno}}$ | - |
| `Co_max`, `Co_min` | Concentración de oxígeno disuelto ($\frac{kg}{L}$) | - |
| `k1`, `n` | Constantes para la viscosidad aparente (ley de potencias) | $\frac{Pa \cdot s^n}{(s^{-1})^{n-1}}$, - |
| `Np` | Número de potencia | - |
| `k_acero`, `k_agua` | Conductividad térmica (acero, agua) | $W/m \cdot °C$ |
| `cp` | Calor específico del agua | $J/kg \cdot °C$ |
| `delta_T` | Máxima diferencia de temperatura ($T_{interna} - T_{salmuera}$) | $°C$ |
| `Y_entalpia`, `Entalpia_esp` | Entalpías de la biomasa/combustión | $kJ/kg$, $kJ/g$ |

---

## Metodología de Cálculo

El script realiza una iteración sobre la velocidad de agitación ($N_i$), incrementándola en pasos pequeños (`paso = 0.001` revoluciones por segundo, $rps$), para encontrar la $N_i$ óptima.

1.  **Cálculo de Variables Dependientes de $N_i$**: En cada paso se calculan:
    * `sher_rate` (Velocidad de cizalla)
    * `µ` (Viscosidad aparente)
    * `Re` (Número de Reynolds)
    * `Na` (Número de aireación)
    * `P` (Potencia sin gas)
    * `Pg_calculado` (Potencia con gas, usando una correlación)
    * `U` (Coeficiente global de transferencia de calor)
    * `A_calculada` (Área de transferencia de calor requerida)

2.  **Condiciones de Optimización**: La $N_i$ se considera óptima si se cumplen simultáneamente las siguientes condiciones:
    * **Transferencia de Calor**: El área de transferencia de calor requerida (`A_calculada`) es menor o igual al área real del tanque (`A_tanque`).
    * **Límites de Potencia**: La potencia gaseada calculada (`Pg_calculado`) se encuentra dentro del rango permitido (`Pg_Min` $\le Pg \le$ `Pg_Max`).

3.  **Cálculos Finales**: Una vez encontrada la $N_i$ óptima, se calcula el coeficiente volumétrico de transferencia de oxígeno (`kLa_final`) utilizando una correlación dependiente de la Potencia Gaseada y la Velocidad Superficial de Gas ($U_g$).

---


