//entrada5.c

int var = 0;

int main(){
	while(var < 5){
		var++;
		if(var < 5){
			continue;
		} else {
			var += 1;
			break;
		}
		var = var + 1;
	}
}
