//entrada7.c

int main(){
	int var = 3 * 3;
	for(int i = 0; i < 5; i++){
		var += 1;
		for(int j = 0; j < 3; j = j + 2){
			if(j==0){
				continue;
			}
			var += 1;
		}
	}
}