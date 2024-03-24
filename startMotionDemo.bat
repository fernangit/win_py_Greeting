cd D:\work\webGL_Greeting\WebGL
start "" D:\work\webGL_Greeting\WebGL\unisrv.exe
timeout /t 5 > nul
start "" microsoft-edge:http://localhost:5000
timeout /t 5 > nul
cd D:\work\win_py_Greeting
.\activate.vbs msedge.exe
timeout /t 10 > nul
python motion.py 4

