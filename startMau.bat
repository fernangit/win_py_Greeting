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
rem start "" microsoft-edge:http://localhost:5000
rem timeout /t 5 > nul
cd E:\work\win_py_Greeting
rem start "" E:\work\win_py_Greeting\venv\Scripts\python.exe E:\work\win_py_Greeting\julius_server.py
rem timeout /t 1 > nul
start "" E:\work\win_py_Greeting\venv\Scripts\python.exe E:\work\win_py_Greeting\Greeting_w_v1.py
rem timeout /t 10 > nul
rem E:\work\win_py_Greeting\activate.vbs msedge.exe
rem timeout /t 5 > nul
rem E:\work\win_py_Greeting\venv\Scripts\python.exe E:\work\win_py_Greeting\browserMaximize.py
