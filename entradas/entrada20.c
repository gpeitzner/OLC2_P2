//entrada20.c
int main(){
	int a[100], n, i, j, position, swap;
	printf("Insertar n�mero de elementos: ");
	n = scanf();
	printf("Insertar %d n�meros:\n", n);
	for(i = 0; i < n; i++){
		a[i] = scanf();
	}
	for(i = 0; i < n - 1; i++){
		position=i;
		for(j = i + 1; j < n; j++){
			if(a[position] > a[j]){
				position=j;
			}
		}
		if(position != i){
			swap=a[i];
			a[i]=a[position];
			a[position]=swap;
		}
	}
	printf("N�meros ordenados:\n");
	for(i = 0; i < n; i++){
		printf("%d\n", a[i]);
	}
	return 0;
}