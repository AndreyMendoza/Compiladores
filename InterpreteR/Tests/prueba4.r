ast = funcion(n)
{
    x = numeric(n);
    x[1:2] = c(1,1);

    para(i en 3:n)
    {
        x[i] = x[i-1] + x[i-2];
    }
    retedsrrerurn(x);
}
print(ast(3))