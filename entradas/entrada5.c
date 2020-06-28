//entrada5.c

int var = 0;

int main(){
	while(var < 5){
		var = var + 1;
		if(var < 5){
			continue;
		} else {
			var = var + 1;
			break;
		}
		var = var + 1;
	}
}
