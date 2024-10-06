set /a R=%RANDOM%*3/32768
if %R%==0 (
    cd E:\work\webGL_Greeting\WebGL
    start "" E:\work\webGL_Greeting\WebGL\unisrv.exe
) else if %R%==1 (
    cd E:\work\webGL_Greeting\WebGL
    start "" E:\work\webGL_Greeting\WebGL\unisrv.exe
) else (
    cd E:\work\webGL_Greeting\WebGL
    start "" E:\work\webGL_Greeting\WebGL\unisrv.exe
)
timeout /t 5 > nul
start "" E:\work\win_py_Greeting\venv\Scripts\python.exe E:\work\webGL_Greeting\WebGL\startServer.py
timeout /t 5 > nul
start "" microsoft-edge:http://localhost:5000
timeout /t 5 > nul
cd E:\work\win_py_Greeting
rem start "" E:\work\win_py_Greeting\venv\Scripts\python.exe E:\work\win_py_Greeting\julius_server.py
rem timeout /t 1 > nul
start "" E:\work\win_py_Greeting\venv\Scripts\python.exe E:\work\win_py_Greeting\Greeting_w_v1.py
timeout /t 10 > nul
E:\work\win_py_Greeting\activate.vbs msedge.exe
timeout /t 5 > nul
E:\work\win_py_Greeting\venv\Scripts\python.exe E:\work\win_py_Greeting\browserMaximize.py
