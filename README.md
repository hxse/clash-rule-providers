# clash-rule-providers
  * create config.custom.yaml overwrite fields
    * key-value field for example: "mixed-port","allow-lan", "mode", "log-level", "external-controller"
    * "proxy-providers", just only assign proxy name and proxy url
    * "rules", all items in the list are overwrite
# gist
  * 在github上创建一个secret gist
  * git clone 项目, 然后把clone下来的所有文件都复制到gist文件夹下面(包括.git文件夹)
  * 运行push_clash_demo的时候, 会自动push repo和gist
  * 最后复制gist raw订阅链接的时候, 注意把raw后面的用来指定版本的随机字符去掉, 否则指定版本的话就没法更新了
