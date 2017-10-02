@echo on
SETLOCAL
REM ONLY CHANGE EXPERIMENT DIRECTORY IN THE NEXT LINE ^
SET EXPERIMENT=OVCAR
REM *************** ASK ETHAN BEFORE CHANGING NEXT LINE *************** ^
call C:\\Users\Solaris\.virtualenvs\notebook\Scripts\activate && python C:\\Users\Solaris\Notebooks\solaris-tools-0.1.0\cli_solaris_batch_export.py "%EXPERIMENT%"
echo
echo Thank you, come again!
TIMEOUT /t 10
exit