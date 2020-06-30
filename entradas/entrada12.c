//entrada12.c

int var1[5] = {5,4,3,4,5};
int var2[2][5] = {{1,2,3,4,5},{6,7,8,9,10}};

int main(){
	for(int i = 0; i < 5; i++){
		printf("var1[%i]=%i\n", i, var1[i]);
	}
}