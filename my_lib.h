// funcao de potencia para c
double potencia(double base, int expoente) {
    double resultado = 1.0;
    int positivo_expoente = expoente > 0 ? expoente : -expoente;

    for (int i = 0; i < positivo_expoente; i++) {
        resultado *= base;
    }

    // Se o expoente for negativo, invertemos o resultado
    if (expoente < 0) {
        resultado = 1.0 / resultado;
    }

    return resultado;
}