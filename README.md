# rasppi-cam-viewer

Projekt wykorzystujący komputer RaspberryPi służący do aktywnego wyświetlania materiału video pochodzącego z kamery
IP. Powodem wykorzystania dokładnie RaspberryPi wynika z wysokiej energooszczędności w porównaniu ze zwykłym PC.
Projekt zakłada także wykorzystanie trzech przycisków i trzech diod LED służących do interrakcji z użytkownikiem.

Wyświetlanie materiału video pochodzącego z kamery IP (po protokole RTSP), dokonywane jest przy pomocy programu omxplayer,
będącym unikalnym składnikiem systemu Raspbian. Wbudowany w komputer rdzeń graficzny jest w pełni wykorzystywany przez 
ten program, co pozwala na dekodowanie materiału HD.

Projekt ten składa się zaledwie z trzech plików:

displayCameras - skrypt bashowy, który musi zostać zamontowany do katalogu /etc/init.d/ . Wykorzystany zostanie
  do uruchamiania programu omxplayer. Zarządza ponadto tym, jak jest wyświetlany materiał video na ekranie.
skrypt.py - Program napisany w pythonie służący do wyświetlania komunikatów na ekranie i interrakcji z użytkownikiem
  przy pomocy przycisków i diód. SKrypt ten wywołuje odpowiednie komendy z pliku displayCameras
plik.bash - Bezpośredni wsad do uruchamiania omxplayera, wykorzystywany przez displayCameras.

Aby projekt mógł być uruchamiany podczas startu systemu, wystarczy dodać polecenie uruchamiające 'skrypt.py' do pliku .bashrc
  
