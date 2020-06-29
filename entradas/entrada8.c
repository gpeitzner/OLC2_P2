//entrada8.c

int metodo1(int &var){
	do{
		var += 1;
		if(var == 1){
			continue;
		}else{
			break;
		}
		var += 1;
	}while(var < 5);
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
	metodo1(var);
	var1 -= 1;
}