cd D:\work\webGL_Greeting\WebGL
start "" D:\work\webGL_Greeting\WebGL\unisrv.exe
timeout /t 5 > nul
start "" python D:\work\webGL_Greeting\WebGL\startServer.py
timeout /t 5 > nul
start "" microsoft-edge:http://localhost:5000
timeout /t 5 > nul
cd D:\work\win_py_Greeting
rem start "" D:\work\win_py_Greeting\venv\Scripts\python.exe D:\work\win_py_Greeting\julius_server.py
timeout /t 1 > nul
start "" D:\work\win_py_Greeting\venv\Scripts\python.exe D:\work\win_py_Greeting\Greeting_w_v1.py
