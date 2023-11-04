Set Processes = GetObject("winmgmts:").InstancesOf("Win32_Process")
Dim ARGS
set ARGS=WScript.Arguments

For Each Process In Processes
    If StrComp(Process.Name, ARGS.Item(0), vbTextCompare) = 0 Then

        ' Activate the window using its process ID...
        With CreateObject("WScript.Shell")
            .AppActivate Process.ProcessId
            .SendKeys "%{F11}"
        End With

        ' We found our process. No more iteration required...
        Exit For

    End If
Next