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

## Código Python

A continuación se muestra el código completo del script:

```python
import math

T=2.1974;#(diametro biorreactor m)
H=6.5922;#(altura biorreactor m)
K11=11;#(constante para rushton del modelo de Otto y el otro wey)
k1=40.48583072/1000;#(Constante obtenida a partir de Regresión Pa s^n)
µ_max=0.2166;#(h-1)
rho=1000; #(densidad kg/m^3)
D_impulsor=0.7325;#(m)
Fa=0.06875;#(m^3/s)
num_imp=4;#(número de impulsores)
Vop=15;#(Volumen operativo [m^3])
AT=3.792356;#(m^2)
Y=1.69;#(Coeficiente de Rendimiento kg biomasa /kg oxígeno)
Co_max=7/1000000; #(Concentración de Oxígeno Disuelto de Saturación kg/L)
Co_min=0.7/1000000; #(Concentración Real de Oxígeno Disuelto kg/L)
n=0.1525847; #(Constante de la correlacion para µ aparente)
Np=6;#(Número de potencia)
Pg_Min=15435; #(Potencia gaseada mínima W)
Pg_Max = 150000 #(Potencia gaseada máxima W)
k_acero=15;#(conductividad termica acero W/m °C)
k_agua=0.6;#(conductividad termica agua W/m °C)
µ_agua=0.001;#(h-1)
cp=4186;#(Calor especifico del agua J/kg °C)
x=0.02;#(Máxima Concentración de Biomasa kg biomasa/L)
delta_T=22.5;#(Temperatura de T-Ta °C, considerando salmuera que entra a 5 y no puede rebasar los 10)
Y_entalpia=-548660;#(entalpia de la biomasa kJ/kg)
Y_entalpia_mol=632940;#(entalpia de la biomasa kJ/mol)
Y_rendimiento=0.53;#(rendimiento de la biomasa g_biomasa/mol)
PM=24.92; #(g/mol)
PM_glucosa=180; #(g/mol)
Rendimiento_gmol=Y_rendimiento*PM_glucosa; #(g_biomasa/mol)
mol_biomasa=Rendimiento_gmol/PM; #(mol)
Entalpia_comb=2800-(mol_biomasa*(Y_entalpia_mol/1000)) #(kJ/mol)
Entalpia_esp=Entalpia_comb/Rendimiento_gmol; #(kJ/g)


Ni=0.1
paso=0.001
Pg_actual = 0.0
kLa_final = 0.0
Ni_optimo = 0.0
Pg_optima = 0.0
A_optimo = 0.0
Ni_encontrado = False 

#Para calcular el A real del tanque
A_cilindro=(math.pi)*T*H;
A_chaqueta=A_cilindro*0.6;
A_tanque=A_chaqueta/(Vop/0.6);


kla_d= (µ_max*x)/(Y*(Co_max-Co_min))
print(f"kla de diseño: {kla_d} h-1")

while Ni <= 1000.0: 
    
    sher_rate = K11 * Ni
       
    µ = k1 * (sher_rate**(n - 1))
    
    Re = (rho * Ni * D_impulsor**2) / µ
   
    Na = Fa / (Ni * D_impulsor**3)
    
    P = Np * rho * (Ni**3) * (D_impulsor**5) * num_imp
    
    Pg_calculado = 1.1274 * (Na**(-0.502)) * P
    
  
    U=((0.005/k_acero)+(D_impulsor/(0.36*(Re**0.67)*(((µ*cp)/(k_agua))**0.33)*k_agua))+0)**-1;

    A_calculada= (Y_entalpia*(µ_max/3600)*x*1000)/((U/1000)*delta_T)

    if A_calculada <= A_tanque:
        if Pg_Min <= Pg_calculado <= Pg_Max:
            Ni_optimo = Ni
            Pg_optima = Pg_calculado
            A_optimo = A_calculada
            U_optimo = U
            µ_optimo = µ
            Re_optimo = Re
            Na_optimo = Na
            P_optimo = P
            Ni_encontrado = True
            Qmet=(Entalpia_esp*µ_max*(Vop*1000)*x*1000)/3600;
            Calor_extraido=(U_optimo*A_tanque*(delta_T))/1000;
            break
        elif Pg_calculado > Pg_Max:
             print("Este Ni que cumple con A_calculada <= A_real excede la potencia máxima permitida.")
             print(f"Ni actual: {Ni*60:.2f} rpm, Pg calculada: {Pg_calculado:.2f} W, A requerida: {A_calculada:.4f} m^2")
             break 
    
    Ni += paso


if Ni_encontrado:
    Ug = Fa / AT
    kLa_final = 0.002 * ((Pg_optima / Vop)**0.7) * (Ug**0.2)*3600
    Ni_final=Ni_optimo*60 

    print(f"Ni: {Ni_final:.2f} rpm")
    print(f"µ app: {µ_optimo:.6f} Pa s")
    print(f"Reynolds: {Re_optimo:.2f}")
    print(f"P: {P_optimo:.2f} W")
    print(f"Na: {Na_optimo:.4f} ")
    print(f"Pg: {Pg_optima:.2f} W")
    print(f"kla: {kLa_final:.4f} h-1")
    print(f"U: {U_optimo:.2f} W/m^2 °C")
    print(f"A real: {A_tanque:.4f} m^2/m^3")
    print(f"A: {A_optimo:.4f} m^2/m^3")
    print(f"Qmet: {Qmet:.2f} kW")
    print(f"Calor extraido: {Calor_extraido:.2f} kW")

else:
    print("No se encontraron Ni que cumplan con las condiciones dadas.")
