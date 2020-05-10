
echo %cd%

if exist "C:\ProgramData\Anaconda3\_conda.exe" (
    call echo "Anaconda Already Installed at C:\ProgramData\Anaconda3"
    call "C:\ProgramData\Anaconda3\Scripts\activate.bat"
    call conda env create -f environment.yml
    call conda activate crossoutML
    call python main.py

) else (
    call cd 
    if exist ".\Anaconda3-2020.02-Windows-x86_64.exe" (
        call start /wait "" Anaconda3-2020.02-Windows-x86_64.exe /InstallationType=AllUsers /AddToPath=1 /RegisterPython=1 /S /D=C:\ProgramData\Anaconda3
        call "C:\ProgramData\Anaconda3\Scripts\activate.bat"
        call conda env create -f environment.yml
        call conda activate crossoutML
        call python main.py
    ) else (
        call echo "Installing Anaconda at C:\ProgramData\Anaconda3"
        call curl https://repo.anaconda.com/archive/Anaconda3-2020.02-Windows-x86_64.exe -O
        call start /wait "" Anaconda3-2020.02-Windows-x86_64.exe /InstallationType=AllUsers /AddToPath=1 /RegisterPython=1 /S /D=C:\ProgramData\Anaconda3
        call "C:\ProgramData\Anaconda3\Scripts\activate.bat"
        call conda env create -f environment.yml
        call conda activate crossoutML
        call python main.py

    )


)