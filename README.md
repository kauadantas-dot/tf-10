# MiniGit — Análise de Leitura x Escrita em Estruturas de Dados

## Tabela de Medição

```text
commits   passos do commitar   passos do log
10        2                     10
100       2                     100
1000      2                     1000
```

## Respostas

**1. Por que o `commitar` gasta sempre 2 passos, e o `log` gasta mais conforme o histórico cresce? (leitura x escrita)**
A escrita no `commitar` apenas registra o novo nó nos dicionários apontando para o commit atual e atualiza o ponteiro da branch, o que tem custo fixo $O(1)$ de 2 passos independentemente do tamanho do repositório. Já a leitura no `log` precisa reconstruir a trajetória seguindo os ponteiros de pai em pai com uma fila até chegar na origem, visitando todos os commits alcançáveis e crescendo de forma linear $O(n)$.

**2. Por que `mensagem(commit)` gasta 1 passo e `buscar(texto)` pode gastar muitos? O que o dicionário ganha quando se procura pela chave, e o que ele não ajuda quando se procura pelo valor?**
Em `mensagem(commit)`, a consulta é feita diretamente pela chave do dicionário, que calcula o hash do identificador e acessa a posição de memória de imediato em 1 passo ($O(1)$). Como a função de espalhamento só indexa as chaves, procurar um trecho de texto dentro dos valores em `buscar(texto)` obriga a percorrer os commits um por um sequencialmente ($O(n)$) até encontrar ou esgotar o histórico.

**3. Por que o `merge` é um commit com dois pais, e por que isso faz do histórico um grafo, e não uma lista?**
O `merge` une duas linhas de desenvolvimento paralelas (a branch atual e a branch mesclada), precisando guardar a referência do último commit de ambas para preservar todo o histórico que veio de cada caminho. Em uma lista encadeada cada elemento aponta para no máximo um antecessor linear, enquanto a possibilidade de bifurcar em branches e convergir com dois pais transforma a estrutura em um grafo dirigido acíclico (DAG).

**4. Por que o método `pais` devolve uma tupla, e não a lista que está guardada dentro do dicionário?**
Se o método devolvesse a própria lista armazenada no atributo privado, qualquer código externo poderia alterá-la com métodos como `append()` ou `pop()`, corrompendo o histórico do repositório e quebrando o encapsulamento. Ao converter o retorno para uma tupla, que é imutável, garantimos que quem consulta os pais possa apenas ler os dados sem modificar a estrutura interna da classe.
