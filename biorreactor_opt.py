## Código Python

A continuación se muestra el código completo del script:

```python

import math

T=2.1974;#(diametro biorreactor m)
H=6.5922;#(altura biorreactor m)
K11=11;#(constante para rushton del modelo de Otto y Mentzer)
k1=40.48583072/1000;#(Constante obtenida a partir de Regresión Pa s^n)
µ_max=0.25;#(h-1)
rho=1000; #(densidad kg/m^3)
D_impulsor=0.7325;#(m)
Fa=0.125;#(m^3/s)(esta es a 0.25 vvm)
num_imp=4;#(número de impulsores)
Vop=15;#(Volumen operativo [m^3])
AT=3.792356;#area transversal(m^2)
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
Y_entalpia_mol=175.48;#(entalpia de la biomasa kJ/mol)
Y_rendimiento=0.53;#(rendimiento de la biomasa g_biomasa/g_glucosa)(lo que se obtiene de glucosa por biomasa, si metes 1 g de glucosa, obtienes 0.53 de biomasa)(paper)
PM_biomasa=24.92; #PM de biomasa(g/mol)
PM_glucosa=180; #(g/mol)
Rendimiento_gmol=Y_rendimiento*PM_glucosa; #(g_biomasa)(gramos totales de biomasa obtenidos)
mol_biomasa=Rendimiento_gmol/PM_biomasa; #(mol)(moles que obtienes de biomasa)
Entalpia_comb=2800-(mol_biomasa*(Y_entalpia_mol)) #(kJ)
Entalpia_esp=Entalpia_comb/Rendimiento_gmol; #(kJ/g biomasa)(entalpia necesaria para el calculo de calor)


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
A_tanque=A_chaqueta/(Vop);


kla_d= (µ_max*x)/(Y*(Co_max-Co_min))
print(f"kla de diseño: {kla_d:.4f} h-1")

while Ni <= 10000000.0: 
    
    sher_rate = K11 * Ni
       
    µ = k1 * (sher_rate**(n - 1))
    
    Re = (rho * Ni * D_impulsor**2) / µ
   
    Na = Fa / (Ni * D_impulsor**3)
    
    P = Np * rho * (Ni**3) * (D_impulsor**5) * num_imp
    
    Pg_calculado = 1.1192 * ((Na*100)**(-0.502)) * P

    hi=(0.36*(Re**0.67)*(((µ*cp)/(k_agua))**0.33)*k_agua)/D_impulsor
    
    U=((0.005/k_acero)+(1/hi)+0)**-1;

    A_calculada= (Entalpia_esp*1000*(µ_max/3600)*x*1000)/((U/1000)*delta_T)

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
            Qmet=(Entalpia_esp*1000*(µ_max/3600)*(Vop)*x*1000);
            Calor_extraido=(U_optimo*A_chaqueta*(delta_T))/1000;
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
    print(f"A volumetrica real: {A_tanque:.4f} m^2/m^3")
    print(f"A volumetrica calculada: {A_optimo:.4f} m^2/m^3")
    print(f"Qmet: {Qmet:.2f} kW")
    print(f"Calor extraido: {Calor_extraido:.2f} kW")

else:
    print("No se encontraron Ni que cumplan con las condiciones dadas.")

   
    
