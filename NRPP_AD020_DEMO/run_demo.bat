@echo off

echo ======================================
echo NRPP - DEMONSTRACAO CAIXA
echo ======================================

python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado.
    pause
    exit
)

pip install -r requirements.txt

python orchestrator.py pdfs

echo.
echo Processamento concluido.
echo Veja os resultados na pasta output.

pause
