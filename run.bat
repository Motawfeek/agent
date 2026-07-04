@echo off
chcp 65001 >nul
echo.
echo  ====================================================
echo   Multi-Tool AI Agent  -  Powered by Groq ^& LangChain
echo  ====================================================
echo.

REM Check if .env has API key
findstr /C:"GROQ_API_KEY=" .env | findstr /V "GROQ_API_KEY=$" >nul 2>&1
if errorlevel 1 (
    echo  [!] لا يوجد Groq API key في ملف .env
    echo  [!] روح على https://console.groq.com واحصل على مفتاح مجاني
    echo  [!] ثم افتح ملف .env وضع المفتاح بعد GROQ_API_KEY=
    echo.
    pause
    exit /b 1
)

echo  [*] Starting Streamlit web app...
echo  [*] افتح المتصفح على http://localhost:8501
echo.
python -m streamlit run app.py --server.headless false
pause
