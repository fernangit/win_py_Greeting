cd E:\work\webGL_Greeting\WebGL
start "" E:\work\webGL_Greeting\WebGL\unisrv.exe
timeout /t 5 > nul
start "" microsoft-edge:http://localhost:5000
timeout /t 5 > nul
cd E:\work\win_py_Greeting
E:\work\win_py_Greeting\activate.vbs msedge.exe
timeout /t 10 > nul
E:\work\win_py_Greeting\venv\Scripts\python motion.py 5
