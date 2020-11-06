# MCOC2020-P3

CONDICIONES DE BORDE NATURALES AL CASO 1-D:

Para obtener la condición de borde natural en el lado izquierdo, se aplico la siguiente condicion de borde:

<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\partial&space;}{\partial&space;x}\left(t,0\right)=&space;5" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\frac{\partial&space;}{\partial&space;x}\left(t,0\right)=&space;5" title="\frac{\partial }{\partial x}\left(t,0\right)= 5" /></a>

Aproximando la condición de borde por medio de sus diferencias finitas de primer orden para el tiempo constante, fijandonos en el puesto 0 y comparandolo con el puesto 1:

<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\partial&space;}{\partial&space;x}\left(t,0\right)\approx&space;\frac{u\left&space;[&space;k,1&space;\right&space;]-u\left&space;[&space;k,0&space;\right&space;]}{dx}=&space;5" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\frac{\partial&space;}{\partial&space;x}\left(t,0\right)\approx&space;\frac{u\left&space;[&space;k,1&space;\right&space;]-u\left&space;[&space;k,0&space;\right&space;]}{dx}=&space;5" title="\frac{\partial }{\partial x}\left(t,0\right)\approx \frac{u\left [ k,1 \right ]-u\left [ k,0 \right ]}{dx}= 5" /></a>

Al reordenar la ecuación:

<a href="https://www.codecogs.com/eqnedit.php?latex=u\left&space;[&space;k,0&space;\right&space;]=&space;-5&space;&plus;&space;u\left&space;[&space;k,1&space;\right&space;]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?u\left&space;[&space;k,0&space;\right&space;]=&space;-5&space;&plus;&space;u\left&space;[&space;k,1&space;\right&space;]" title="u\left [ k,0 \right ]= -5 + u\left [ k,1 \right ]" /></a>

De esta forma obtenemos un nuevo stencil de diferencias finitas (pequeño) que nos permite completar el valor faltante.

Despues de agregar la linea anterior al codigo y usando los mismos parámetros de los ejemplos de clases. Para el caso de la siguiente imagen: 

 ![Problema](ProblemaE3.png)

Se realizo el gráfico con un paso de integración dt = 2s y curvas de evolución térmica cada 1000 pasos hasta llegar a 50000 pasos. Los resultados se presenta a continuación:

 ![Grafico](Grafico_E3_Evolución_Termica.png)

Al analizar el gráfico se puede ver como al final la solución converge ya que las últimas curvas son rectas practicamente estables.

Las condiciones de borde natural de el tipo estudiado hasta ahora, pueden ser utilizadas cuando se tiene continuidad de piezas de hormigón, es decir cando se tiene una piexa con ciertas temperaturas adyacente a otra con temperaturas distintas. De esta forma se evitará tener un salto en las temperaturas ya que las tangemtes coincidiran.  

CASOS 2-D PARA VERIFICAR:

Las conciones de borde para el caso 2D son de la forma:

u_k[:,:] = TEMPERATURA INICIAL EN TODAS PARTES

u_k[0,:] = TEMPERATURA IZQUIERDA

u_k[-1,:] =  TEMPERATURA DERECHA

u_k[:,0] =  TEMPERATURA INFERIOR

u_k[:,-1] = TEMPERTURA SUPERIOR


u_k[0,:] = u_k[1,:] - (GRADIENTE T IZQUIERA) * dx

u_k[-1,:] = u_k[-2,:] - (GRADIENTE T DERECHA) * dx

u_k[:,0] = u_k[:,1] - (GRADIENTE T INFERIOR) * dy

u_k[:,-1] = u_k[:,-2] - (GRADIENTE T SUPERIOR) * dy


