//entrada6.c

int var = 0;

int main(){
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
