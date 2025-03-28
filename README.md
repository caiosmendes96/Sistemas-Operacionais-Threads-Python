# Sistemas-Operacionais-Threads-Python
 Implementação de soluções para condições de corrida em jogos utilizando a linguagem de programação Python.

##

<h3>Introdução</h3>

O jogo é uma corrida apostada entre dois jogadores para escolher o vencedor.

Entre cinco cavalos em uma pista. Essa pista é uma matriz 11x5 onde os cavalos.

Começam em posições pré-definidas e cada um tem três tipos de ações: ”down”, ”right” e ”up”. 

No início do jogo, cada célula do jogo (excluindo a posição inicial de cada cavalo e a linha de chegada) tem a pontuação no valor de 2. A cada movimentação realizada, os cavalos vão somando pontos enquanto visitam as.

Células da pista e essas células recebem pontuações menores a cada vez que são visitadas. Ou seja, como cada cavalo é uma thread, pode ocorrer que um cavalo.

Visite a mesma célula que outro ao mesmo tempo e a concorrência pela pontuação ”compartilhada” se torna uma condição de corrida. Essas condições de
corrida foram solucionadas utilizando três métodos: exclusão mútua, semáforos e monitores.

##

<h3>Implementação e funcionalidades</h3>

Para cada solução de condições de corrida, houve alterações no código para que
Se mantivesse a funcionalidade correta do jogo.

Pontuação:

- Pontuação por pista: Cada célula na pista possui uma pontuação inicial.

  Quando uma thread passa por uma célula, ela recebe a pontuação associada, que é então diminuída para threads subsequentes.

- Pontuação por colocação: Além dos pontos obtidos ao percorrer a pista, as Threads recebem uma pontuação adicional com base na ordem de chegada. O primeiro lugar recebe a maior pontuação, e essa pontuação diminui para os próximos colocados.

##

<h3>Soluções para condição de corrida</h3>

- 3.1 Exclusão mútua:
    Para o caso em que um cavalo consiga acessar a região crítica, a posição recebe o bloqueio de acesso enquanto o cavalo executa sua ação. Enquanto isso, um outro cavalo tenta acessar a mesma posição, mas não consegue, pois ela ainda está bloqueada. Então, esse cavalo tem sua ação reiniciada e terá que realizar uma nova tentativa de acesso até que essa posição esteja desbloqueada.

- 3.2 Semáforos: Para o caso em que um cavalo consiga acessar a região crítica, a posição recebe o bloqueio de acesso enquanto o cavalo executa sua ação. Enquanto isso, outro cavalo tenta acessar a mesma posição, mas não consegue, pois ela ainda está bloqueada. Então, esse cavalo tem sua execução ”congelada” e terá que esperar o cavalo que acessou primeiro essa região crítica terminar sua execução e desbloquear a posição para que continue a sua ação. 

- 3.3 Monitores: Para o caso em que um cavalo consiga acessar a região crítica, a posição recebe o bloqueio de acesso enquanto o cavalo executa sua ação. Enquanto isso, um outro cavalo tenta acessar a mesma posição, mas não consegue, pois ela ainda está bloqueada. Então, esse cavalo tem sua ação reiniciada e terá que realizar uma nova tentativa de acesso até que essa posição esteja desbloqueada.

##

<h3>Testes</h3>

Os testes foram realizados com um conjunto de ações pré-definidas para garantir as condições de corrida, também foi adicionado um delay de 0.5 segundos para cada ação realizada do cavalo. Para fazer comparação das soluções, foi calculado o tempo para cada vez que um cavalo tem sua ação reiniciada (para exclusão mútua e monitores) ou ”congelada” (para semáforos) até que consiga acessar a posição requerida.


