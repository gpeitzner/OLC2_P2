int a = 1;
int b = a++;

int main(){
	int b = 100;
	printf("%d\n",b);
	b += 10;
	printf("%d\n",b);
	b -= 10;
	printf("%d\n",b);
	b /= 10;
	printf("%d\n",b);
	b *= 10;
	printf("%d\n",b);
	b %=10;
	printf("%d\n",b);
	b <<=10;
	printf("%d\n",b);
	b >>=10;
	printf("%d\n",b);
	b &=10;
	printf("%d\n",b);
	b ^=10;
	printf("%d\n",b);
	b |=10;
	printf("%d\n",b);
	b++;
	printf("%d\n",b);
	b--;
	printf("%d\n",b);
	--b;
	printf("%d\n",b);
	++b;
	printf("%d\n",b);
}