# C-to-Python-_-V2

No código em C++ é realizada a aquisição de dados com o esp32 com multiprocessamento (dois loops). No loop1 é realizada a leitura de 4 canais AD (frequência de 1000 Hz) e armazenamento em um buffer (200 linhas) do tipo Json. O loop2 envia o buffer via sockets para ser recebido no código em Python. 
**Importante.: foi utilizada a versão 5.13.5 do Json. 

O código em python recebe os dados do Esp32 (via sockets), armazena em um arquivo de texto e também apresenta o gráfico dos dados (5 Hz - 1 amostra de cada buffer).  

