import argparse
import math
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np

#definicion de variables de entrada
parser = argparse.ArgumentParser(description="Programa para el cálculo de presión en una tuberia de dos tramos con diametro distinto.")
parser.add_argument("-d1","--diametro1",type=float, help="Diametro de primer tramo. (m)")
parser.add_argument("-d2","--diametro2",type=float, help="Diametro de segundo tramo. (m)")
parser.add_argument("-q","--caudal",type=float, help="Caudal en la tuberia. (m^3/s)")
parser.add_argument("-z1","--altura1",type=float, help="Altura de tramo 1. (m)")
parser.add_argument("-z2","--altura2",type=float, help="Altura de tramo 2. (m)")
parser.add_argument("-l1","--longitud1",type=float, help="Longitud de tramo 1. (m)")
parser.add_argument("-l2","--longitud2",type=float, help="Longitud de tramo 2. (m)")
args = parser.parse_args()

#definicion variables predeterminadas
p1=180*(10**3)
densidad=997
g=9.81

#coeficientes de cada material
coef={"Pead":150,"Polipropileno":140,"AceroGalvanizado":120,"Concreto":130}

#calculo de areas
area1=math.pi*(args.diametro1**2)/4
area2=math.pi*(args.diametro2**2)/4
print("El area del primer tramo es igual a: {:10.4f} m^2".format(area1))
print("El area del segundo tramo es igual a: {:10.4f} m^2\n".format(area2))


#calculo de velocidades
v1=args.caudal/area1
v2=args.caudal/area2
print("El velocidad del primer tramo es igual a: {:10.4f} m/s".format(v1))
print("El velocidad del segundo tramo es igual a: {:10.4f} m/s\n".format(v2))

#primer tramo
p1pg=(p1/(densidad*g))
v12g=(0.5*(v1**2)/g)

#segundo tramo
v22g=(0.5*(v2**2)/g)

#calculo de presion y guardado en diccionario de resultados
resultados={}
for c1 in coef:
	for c2 in coef:
		hf1=args.longitud1*(args.caudal**1.851)/((0.279*coef[c1]*(args.diametro1**2.63)))**1.851
		hf2=args.longitud2*(args.caudal**1.851)/((0.279*coef[c2]*(args.diametro2**2.63)))**1.851
		hftotal=hf2+hf1

		p2=(p1pg+args.altura1+v12g-args.altura2-v22g-hftotal)*densidad*g

		resultados[c1+"-"+c2]={"p2":p2,"hf1":hf1,"hf2":hf2,"deltahf":hftotal}

print("P2 para las distintas combinaciones:")


tabla = PrettyTable(['Combinación', 'Presión 2',"Hf1","Hf2","DeltaHf"])

for key in resultados:
	tabla.add_row([key,'{:10.4f}'.format(resultados[key]["p2"]),'{:10.4f}'.format(resultados[key]["hf1"]),'{:10.4f}'.format(resultados[key]["hf2"]),'{:10.4f}'.format(resultados[key]["deltahf"])])
print(tabla)

x1=[]
i=0
while i<((int(args.longitud1)*100)+1):
	x1.append(int(i))
	i+=1

x2=[]
i=(args.longitud1*100)+20
while i<((int(args.longitud2)*100)+(int(args.longitud1)*100)+21):
	x2.append(int(i))
	i+=1

x=x1+x2

i=1
for key in resultados:

	#arrays para graficas
	z1y=np.array(([args.altura1]*(int(args.longitud1)*100+1))+([args.altura2]*(int(args.longitud2)*100+1)))
	ppg=np.array(([p1pg]*(int(args.longitud1)*100+1))+([resultados[key]["p2"]/(densidad*g)]*(int(args.longitud2)*100+1)))
	v2g=np.array(([v12g]*(int(args.longitud1)*100+1))+([v22g]*(int(args.longitud2)*100+1)))
	hfcon=np.array(([0]*(int(args.longitud1)*100+1))+([resultados[key]["deltahf"]]*(int(args.longitud2)*100+1)))


	plt.figure(i)
	plt.suptitle(key)
	plt.subplot(4,1,1)
	plt.title("Altura+P/(p*g)+V/(2*g)+Delta Hf")
	plt.ylabel("(m)")
	plt.xlabel("Distancia a extremo izquierdo de tuberia. (m)")
	plt.plot(x,z1y+ppg+v2g+hfcon , '-o',markersize=0.1,color="blue")

	plt.subplot(4,1,2)
	plt.title("Altura+P/(p*g)+V/(2*g)")
	plt.ylabel("(m)")
	plt.xlabel("Distancia a extremo izquierdo de tuberia. (m)")
	plt.plot(x, z1y+ppg+v2g, '-o',markersize=0.1,color="green")

	plt.subplot(4,1,3)
	plt.title("Altura+P/(p*g)")
	plt.ylabel("(m)")
	plt.xlabel("Distancia a extremo izquierdo de tuberia. (m)")
	plt.plot(x, z1y+ppg, '-o',markersize=0.1,color="red")

	plt.subplot(4,1,4)
	plt.title("Altura")
	plt.ylabel("(m)")
	plt.xlabel("Distancia a extremo izquierdo de tuberia. (m)")
	plt.plot(x, z1y, '-o',markersize=0.1,color="brown")
	
	i+=1
	plt.tight_layout()
plt.show()




