from matplotlib.pylab import *
from numpy import *
from matplotlib import cm

#Geometria:
a = 1.  # Alto
b = 1.  # Ancho
Nx = 30 # N intervalos x
Ny = 30 # N intervalos y

# Discretización
dx = b/Nx 
dy = a/Ny

if dx != dy :
    print("ERROR!!...dx!=dy")
    exit(-1)

h = dx
#coords = lambda i,j:(dx*i,dy*j)
    
def coords(i,j) : return (dx*i,dy*j)

x,y = coords(4,2)

print("x: ", x)
print("y: ", y)

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
u_k = zeros((Nx+1,Ny+1), dtype=double)
u_km1 = zeros((Nx+1,Ny+1), dtype=double)

# Condiciones de temp. inicial
u_k[:,:] = 30.     # 30 grados inicial en todas partes

# Parametros problema
dt = 0.01 #s
k = 79.5  #m^2/s
c = 450.  #J/kg*C
rho = 7800. #kg/m^3
alpha = k*dt /(c*rho * dx**2)

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
dnext_t = 0.5 * hora

next_t = 0
framenum = 0

T = 1*dia
Days = 1*T

# Vectores para acumular la temperatura en lugares interesantes
u_1 = zeros(int32(Days/dt))
u_2 = zeros(int32(Days/dt))
u_3 = zeros(int32(Days/dt))

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
    u_k[0,:] = 10.  #Izq.

    u_k[-1,:] = u_k[-2,:] - 0*dx # Der. gradiente 0
    u_k[:,-1] = u_k[:,-2] - 0*dy # Sup. gradiente 0
    u_k[:,0] = u_k[:,1] - 0*dy # Inf. gradiente 0

    # Loop en el espacio:
    for i in range(1,Nx):
        for j in range(1,Ny):
            nabla_u_k = (u_k[i-1,j] + u_k[i+1,j] +u_k[i,j-1] + u_k[i,j+1] - 4 * u_k[i,j])/h**2

            u_km1[i,j] = u_k[i,j] + alpha *nabla_u_k

    u_k = u_km1

    # CB de nuevo para asegurar cumplimiento:
    u_k[0,:] = 10.  #Izq.

    u_k[-1,:] = u_k[-2,:] - 0*dx # Der. gradiente 0
    u_k[:,-1] = u_k[:,-2] - 0*dy # Sup. gradiente 0
    u_k[:,0] = u_k[:,1] - 0*dy # Inf. gradiente 0

    # Encontrar la temperatura en lugares interesantes
    u_1[k] = u_k[int(Nx/2),int(Ny/2)]
    u_2[k] = u_k[int(Nx/2),int(3*Ny/4)]
    u_3[k] = u_k[int(3*Nx/4),int(3*Ny/4)]

    if t > next_t :
        figure(1)
        imshowbien(u_k)
        title(titulo)
        savefig("Ejemplo/frame_{0:04.0f}.png".format(framenum))
        framenum += 1
        next_t += dnext_t
        close(1)

# plot historia de temperaturasen puntos interes

figure(2)
plot(range(int32(Days/dt)), u_1, label='P1')
plot(range(int32(Days/dt)), u_2, label='P2')
plot(range(int32(Days/dt)), u_3, label='P3')
title("Evolucion de temperatura en puntos")
legend()
show()
