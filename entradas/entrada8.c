//entrada8.c

int metodo1(int &var2, int var1){
	do{
		var2 += 1;
		if(var2 == 1){
			continue;
		}else{
			break;
		}
		var2 += 1;
	}while(var2 < 5);
}

int main(){
	int var = 3 * 3;
	int var1 = 3;
	for(int i = 0; i < 5; i++){
		var += 1;
		for(int j = 0; j < 3; j = j + 2){
			if(j==0){
				continue;
			}
			var += 1;
		}
	}
	printf("VAR:%s VAR1:%s\n", var, var1);
	metodo1(var, var1);
	printf("VAR:%s VAR1:%s\n", var, var1);
	var1 -= 1;
}