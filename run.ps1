$pythonVersion = Invoke-Expression -Command "python -V" 2>&1
$python3Version = Invoke-Expression -Command "python3 -V" 2>&1
$numberVersion = $pythonVersion.Split(" ")


if(![string]::IsNullOrEmpty($pythonVersion))
{
    if($numberVersion[1] -like "3*")
    {
        python telegramexporter.py
        Read-Host -Prompt "Press enter to continue..."
    }
    else
    {
        Write-Output "Too low Python version found. Please, install a Python version >= 3.6"
        Read-Host -Prompt "Press enter to continue..."
    }
}
elseif(![string]::IsNullOrEmpty($python3Version))
{
    
    python3 telegramexporter.py
    Read-Host -Prompt "Press enter to continue..."
}
else
{
    Write-Output "No Python versions found. Please, install a Python version >= 3.6"
    Read-Host -Prompt "Press enter to continue..."
}