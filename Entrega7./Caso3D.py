from matplotlib.pylab import *
from numpy import *
from matplotlib import cm
import calor_de_hidratacion import Calor_de_hidratacion

#Geometria:
a = 1.  # Alto (y)
b = 1.  # Ancho (x)
c = 1.  # Largo (z)

Nx = 30 # N intervalos x
Ny = 30 # N intervalos y
Nz = 30 # N intervalos z

# Discretización:
dx = b/Nx # Discretización x
dy = a/Ny # Discretización y
dz = c/Nz # Discretización z

if dx != dy :
    print("ERROR!!...dx!=dy")
    exit(-1)

h = dx

# Calculo de coordenadas del punto (i,j,k) 
def coords(i,j,k) : return (dx*i,dy*j,dz*k)

# Testeo funcion coords:
x,y,z = coords(4,2,2)

print("x: ", x)
print("y: ", y)
print("z: ", z)

def imshowbien(u) :
    imshow(u.T[Nx::-1,:],cmap=cm.coolwarm,interpolation='bilinear')
    cbar = colorbar(extend='both', cmap=cm.coolwarm)
    ticks = arange(0,35,5)
    ticks_Text = ["{}".format(deg) for deg in ticks]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(ticks_Text)
    clim(0,30)

    xlabel('b')
    ylabel('a')
    xTicks_N = arange(0,Nx+1,3)
    yTicks_N = arange(0,Ny+1,3)
    xTicks = [coords(i,0)[0] for i in xTicks_N]
    yTicks = [coords(0,i)[1] for i in yTicks_N]
    xTicks_Text = ["{0:.2f}".format(tick) for tick in xTicks]
    yTicks_Text = ["{0:.2f}".format(tick) for tick in yTicks]
    xticks(xTicks_N,xTicks_Text,rotation='vertical')
    yticks(yTicks_N,yTicks_Text)
    margins(0.2)
    subplots_adjust(bottom=0.15)
    
# Arreglo solución
u_k = zeros((Nx+1,Ny+1,Nz+1), dtype=double)
u_km1 = zeros((Nx+1,Ny+1,Nz+1), dtype=double)

# Condiciones de temp. inicial
u_k[:,:,:] = 20.     # 20. grados inicial en todas partes

# Parametros problema
dt = 0.01 #s
k = 79.5  #m^2/s
c = 450.  #J/kg*C
rho = 7800. #kg/m^3
alpha = k*dt /(c*rho * dx**2)
DC = 360. #kg/m^3

# Informacion:
print(f"dt= {dt}")
print(f"dx= {dx}")
print(f"k= {k}")
print(f"c= {c}")
print(f"rho= {rho}")
print(f"alpha= {alpha}")

# Loop de tiempo:
minuto = 60.
hora = 3600.
dia = 24 *3600

dt = 1*minuto

dnext_t1 = 0.5 * hora
dnext_t2 = 0.5 * hora
dnext_t3 = 0.5 * hora

next_t1 = 0
framenum_1 = 0

next_t2 = 0
framenum_2 = 0

next_t3 = 0
framenum_3 = 0

T = 3*dia
Days = 1*T # Cantidad de dias a modelar

# Vectores para acumular la temperatura en lugares interesantes
u_1 = zeros(int32(Days/dt))
u_2 = zeros(int32(Days/dt))
u_3 = zeros(int32(Days/dt))
u_4 = zeros(int32(Days/dt))
u_5 = zeros(int32(Days/dt))
u_6 = zeros(int32(Days/dt))
u_7 = zeros(int32(Days/dt))
u_8 = zeros(int32(Days/dt))
u_9 = zeros(int32(Days/dt))
u_10 = zeros(int32(Days/dt))
u_11 = zeros(int32(Days/dt))
u_12 = zeros(int32(Days/dt))
u_13 = zeros(int32(Days/dt))
u_14 = zeros(int32(Days/dt))
u_15 = zeros(int32(Days/dt))

# Funcion para truncar números decimales:
def truncate(n,decimals=0) :
    multiplier = 10 ** decimals
    return int(n*multiplier)/multiplier

# Loop de tiempo:
for k in range(int32(Days/dt)) :
    t = dt *(k+1)
    dias = truncate(t/dia,0)
    horas = truncate((t-dias*dia)/hora,0)
    minutos = truncate((t-dias*dia-horas*hora)/minuto,0)
    titulo = "k = {0:05.0f}".format(k) + "t = {0:02.0f}d {1:02.0f}h {2:02.0f}m".format(dias,horas,minutos)
    print(titulo)
    
    # CB esenciales:

        # Temp. ambiente:
    u_ambiente = 20. + 10*sin((2*pi/T)*t)

        # Temp. cara sup:
    u_k[:,:,-1] = u_ambiente

        # Temp. cara inf:
    u_k[ : , : , 0 ] = u_k[ : , : ,-2 ]-0*dy
    
        # Temp. cara der:
    u_k[ : ,-1 , : ] = u_k[ : ,-2 , : ]-0*dx
    
        # Temp. cara izq:
    u_k[ : , 0 , : ] = u_k[ : ,1 , : ]-0*dx
    
        # Temp. cara frente:
    u_k[-1 , : , : ] = u_k[-2 , : , : ]-0*dz
    
        # Temp. cara atras:
    u_k[ 0 , : , : ] = u_k[ 1 , : , : ]-0*dz

    # Loop en el espacio:
    for i in range(1,Nx):
        for j in range(1,Ny):
            for k in range(1,Nz):
                nabla_u_k = (u_k[i-1,j,k] + u_k[i+1,j,k] +u_k[i,j-1,k] + u_k[i,j+1] + u_k[i,j,k-1] + u_k[i,j,k+1] - 6 * u_k[i,j,k])

                u_km1[i,j,k] = u_k[i,j,k] + alpha * nabla_u_k + Calor_de_hidratacion(t) * dt/(c*ρ)*1000.

    u_k = u_km1

    # CB de nuevo para asegurar cumplimiento:

        # Temp. ambiente:
    u_ambiente = 20. + 10*sin((2*pi/T)*t)

        # Temp. cara sup:
    u_k[:,:,-1] = u_ambiente

        # Temp. cara inf:
    u_k[ : , : , 0 ] = u_k[ : , : ,-2 ]-0*dy # Gradiente 0
    
        # Temp. cara der:
    u_k[ : ,-1 , : ] = u_k[ : ,-2 , : ]-0*dx # Gradiente 0
    
        # Temp. cara izq:
    u_k[ : , 0 , : ] = u_k[ : ,1 , : ]-0*dx # Gradiente 0
    
        # Temp. cara frente:
    u_k[-1 , : , : ] = u_k[-2 , : , : ]-0*dz # Gradiente 0
    
        # Temp. cara atras:
    u_k[ 0 , : , : ] = u_k[ 1 , : , : ]-0*dz # Gradiente 0


    # Encontrar la temperatura en lugares interesantes CC
    u_1[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_2[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_3[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_4[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_5[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_6[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_7[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_8[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_9[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_10[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_11[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_12[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_13[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_14[k] = u_k[int(Nx),int(Ny),int(Nz)]
    u_15[k] = u_k[int(Nx),int(Ny),int(Nz)]
    
    if t > next_t1 :
        figure(1)
        imshowbien(u_k)
        title(titulo)
        savefig("Ejemplo/frame_{0:04.0f}.png".format(framenum))
        framenum += 1
        next_t += dnext_t
        close(1)

    if t> next_t1:
        plt.figure(1)
        imshowbienxy(u_k[:,:,int(Nz/2)],int(Nz/2))
        plt.title(titulo)
        plt.savefig("fig/caso_xy_{0:04.0f}.png".format(framenum1))
        framenum1+=1
        next_t1+= dnext_t1
        plt.close(1)
    if t> next_t2:
        plt.figure(2)
        imshowbienxz(u_k[:,int(Ny/2),:],int(Ny/2))
        plt.title(titulo)
        plt.savefig("fig/caso_xz_{0:04.0f}.png".format(framenum2))
        framenum2+=1
        next_t2+= dnext_t2
        plt.close(2)
    if t> next_t3:
        plt.figure(3)
        imshowbienyz(u_k[int(Nx/2),:,:],int(Nx/2))
        plt.title(titulo)
        plt.savefig("fig/caso_yz_{0:04.0f}.png".format(framenum3))
        framenum3+=1
        next_t3+= dnext_t3
        plt.close(3)
        
# Plot historia de temperaturasen puntos interes

plt.figure(4)

plot(range(np.int32(Days / dt)), u_1, label='Sensor 1')
plot(range(np.int32(Days / dt)), u_2, label='Sensor 2')
plot(range(np.int32(Days / dt)), u_3, label='Sensor 3')
plot(range(np.int32(Days / dt)), u_4, label='Sensor 4')
plot(range(np.int32(Days / dt)), u_5, label='Sensor 5')
plot(range(np.int32(Days / dt)), u_6, label='Sensor 6')
plot(range(np.int32(Days / dt)), u_7, label='Sensor 7')
plot(range(np.int32(Days / dt)), u_8, label='Sensor 8')
plot(range(np.int32(Days / dt)), u_9, label='Sensor 9')
plot(range(np.int32(Days / dt)), u_10, label='Sensor 10')
plot(range(np.int32(Days / dt)), u_11, label='Sensor 11')
plot(range(np.int32(Days / dt)), u_12, label='Sensor 12')
plot(range(np.int32(Days / dt)), u_13, label='Sensor 13')
plot(range(np.int32(Days / dt)), u_14, label='Sensor 14')
plot(range(np.int32(Days / dt)), u_15, label='Sensor 15')
xlabel("t [minutos]")
ylabel("Temperatura [°C]")
title("Evolucion de temperatura")
legend()
savefig("EvolucionT_caso_1.png")
show()
