chcp 65001
cd %~dp0
set /p c=请输入commit:
git add .
git commit -m "%c%"
git push https://hxse:%hxse_github_token%@github.com/hxse/clash-rule-providers.git


cd "..\clash-rule-providers-gist"
call "push gist.bat"
pause
