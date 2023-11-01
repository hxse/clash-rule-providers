# clash-rule-providers
  * create config.custom.yaml overwrite fields
    * key-value field for example: "mixed-port","allow-lan", "mode", "log-level", "external-controller"
    * "proxy-providers", just only assign proxy name and proxy url
    * "rules", all items in the list are overwrite
# gist
  * create secret gist
  * git clone <your gist> in "../clash-rule-providers-gist"
  * create `push gist.bat` in "../clash-rule-providers-gist"
    ``` push gist.bat
    cd %~dp0
    @REM set /p c=请输入commit:
    set c= "update"
    git add .
    git commit -m "%c%"
    git push https://hxse:%hxse_github_token%@gist.github.com/hxse/<your gist url>
    ```
  * .\build_clash_demo.bat
  * .\push_clash_demo.bat
