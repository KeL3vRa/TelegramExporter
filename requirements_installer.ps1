$pythonVersion = Invoke-Expression -Command "python -V" 2>&1
$python3Version = Invoke-Expression -Command "python3 -V" 2>&1


if([string]::IsNullOrEmpty($pythonVersion) -and [string]::IsNullOrEmpty($python3Version))
{
    Write-Output "No Python version found. Will be installed the version 3.9.0"
    #[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

    #Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.0/python-3.9.0.exe" -OutFile "c:/temp/python-3.9.0.exe"
    #c:/temp/python-3.9.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    
}
else 
{
    
    #check requirements.txt exist
    $scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
    $requirementFile = "$scriptPath\requirements.txt"
    $existFile = [System.IO.File]::Exists($requirementFile)
    if($existFile)
    {
        Write-Output "Install requirements..."
        #divide stdout and stderr
        $pip = &{pip3 install -r $requirementFile} 2>&1
        $pip | ?{ $_ -isnot [System.Management.Automation.ErrorRecord] }

        $pip.Exception.Message
    }
    else
    {
        Write-Output "Please, download requirements.txt"
    }
}
