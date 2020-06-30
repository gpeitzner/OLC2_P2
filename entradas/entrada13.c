//entrada13.c

struct carro{
	int llantas;
	char color[];
	float puertas[];
};

int main(){
	struct carro carros[];
	carros[0].llantas = 4;
	carros[0].color = "verde";
	carros[0].puertas[0] = 13.37;
	carros[0].puertas[1] = 19.25;
	carros[1].llantas = 4;
	carros[1].color = "azul";
	carros[1].puertas[0] = 69.39;
	carros[1].puertas[1] = 27.30;
}