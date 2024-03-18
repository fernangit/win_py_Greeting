cd D:\work\webGL_Greeting\WebGL
start "" D:\work\webGL_Greeting\WebGL\unisrv.exe
timeout /t 5 > nul
start "" microsoft-edge:http://localhost:5000
timeout /t 5 > nul
cd D:\work\win_py_Greeting
.\activate.vbs msedge.exe
timeout /t 10 > nul
python motion.py 0
timeout /t 3 > nul
python motion.py 1
timeout /t 3 > nul
python motion.py 2
timeout /t 3 > nul
python motion.py 3
timeout /t 3 > nul
python motion.py 4
timeout /t 3 > nul
python motion.py 5
timeout /t 3 > nul
python motion.py 6
timeout /t 3 > nul
python motion.py 7
