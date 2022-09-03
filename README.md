# professor-matching

Aluno: Felipe Gomes Paradas
Matricula: 17/0009840

## Como Rodar

Para rodar o código, é necessário possuir o pacote pprint, além da plataforma python. A instalação é possível por:

 ```sh
 pip3 install pprint
 ```

Após garantir que o pacote está instalado, basta rodar

```sh
python3 src/main.py input.txt
```

Foi fornecido o arquivo de entrada do projeto como input.txt, porém ele aceita qualquer arquivo no mesmo formato especificado.

## Algoritmo

1. Lê o arquivo de entrada e carrega as listas de preferencia

2. Limpa as listas de preferências dos professores removendo escolas que não possuem vaga para a qualificação dele e cria as listas de preferências das escolar, sendo todos os professores que possuem pelo menos a qualificação necessária para aquela vaga específica

3. Inicia todos os professores, escolas e vagas livres

4. Para cada escola livre (sem nenhum match):

    1. se o professor não estiver em nenhum outro match, cria o match

    2. caso contrario, cria o match com a escola que o professor tem maior preferencia e remove o match de menor preferencia

5. Para cada posição livre, repete o mesmo algoritmo de 4, porém a escola apenas perde seu professor caso ela já possua outra alocação, mantendo as 50 escolas com pelo menos 1 professor.

## References

https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.95.9251&rep=rep1&type=pdf