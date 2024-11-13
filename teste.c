// Arquivo de teste: teste.c

#include <stdio.h>
#include <stdlib.h>
#include "my_lib.h"

// Função que calcula o quadrado de um número
int quadrado(int x) {
    return x * x;
}

/*
    Função principal
    Realiza algumas operações matemáticas
*/
int main() {
    printf("2^2 = %0.f\n", pow(2,2));
    printf("This is a test\n");
    int a = 5;
    int b = 10;
    int resultado = 0;

    // Calcula o quadrado de 'a' e 'b'
    resultado = quadrado(a) + quadrado(b);
    printf("Resultado: %d\n", resultado);

    // Condicional e loop para testes de espaços e sintaxe
    if (resultado > 50) {
        for (int i = 0; i < 5; i++) {
            printf("Iteração: %d\n", i);
        }
    }

    return 0;
}