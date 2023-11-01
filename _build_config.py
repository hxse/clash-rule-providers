#!/usr/bin/env python3
# coding: utf-8
import yaml
from yaml import CSafeLoader as Loader, CSafeDumper as Dumper
from clash_api import reload_config, all_connections
from pathlib import Path
from shutil import copyfile


def create_proxy_providers(custom_data, black_list):
    obj = {}
    for i, v in custom_data.items():
        if i in black_list:
            obj[i] = {}
        else:
            obj[i] = v
    return obj


def replace_url(url, subconvert="http://127.0.0.1:25500/sub?target=clash&url="):
    return subconvert + url


def create_provider(name, obj, interval1=3600, interval2=300):
    return {
        "type": "http",
        "path": f"./profiles/proxies/{name}.yaml",
        "url": replace_url(obj["url"]),
        "filter": obj["filter"] if "filter" in obj else "",
        "interval": interval1,
        "health-check": {
            "enable": True,
            "url": "http://www.gstatic.com/generate_204",
            "interval": interval2,
        },
    }


def add_group_proxies(custom_data, enable_match=True):
    # enable_match开启匹配前缀功能
    # 匹配前缀,DOG-gatern项,匹配D-default,O-other,G-Game三个组,最好用大写,包含匹配(in)
    # 匹配子前缀,R-uk-region,匹配RG-uk-gatern_s,RG-uk-mojie_s,匹配的是[1:-1]中间的uk,相等匹配(==)
    res = []
    for group in custom_data["proxy-groups"]:
        res.append(group)
        group["proxies"] = ["DIRECT", "REJECT"]
        for i, v in custom_data["proxy-providers"].items():
            if not enable_match:
                group["proxies"].append(f"{i}_s")
                continue
            if group["name"].split("-")[0] in i.split("-")[0]:
                if len(group["name"].split("-")) <= 2:
                    group["proxies"].append(f"{i}_s")
                elif "-".join(group["name"].split("-")[1:-1]) == "-".join(
                    i.split("-")[1:-1]
                ):
                    group["proxies"].append(f"{i}_s")
    return res


def create_proxy_groups(name, interval=300):
    return [
        {
            "name": f"{name}_s",
            "type": "select",
            "interval": interval,
            "url": "http://www.gstatic.com/generate_204",
            "proxies": [f"{name}_a"],
            "use": [name],
        },
        {
            "name": f"{name}_a",
            "type": "url-test",
            "interval": interval,
            "url": "http://www.gstatic.com/generate_204",
            "use": [name],
        },
    ]


def run_build_config(path="config.custom.yaml", outPath="config.yaml"):
    with open(path, "r", encoding="utf8") as f:
        custom_data = yaml.load(f, Loader=Loader)
    new_obj = create_proxy_providers(custom_data, ["proxy-providers", "proxy-groups"])

    for i, v in custom_data["proxy-providers"].items():
        new_provider = create_provider(i, v)
        new_obj["proxy-providers"][i] = new_provider

    new_obj["proxy-groups"] = add_group_proxies(custom_data)

    for i, v in custom_data["proxy-providers"].items():
        new_group = create_proxy_groups(i)
        new_obj["proxy-groups"] = [*new_obj["proxy-groups"], *new_group]

    with open(outPath, "w", encoding="utf8") as f:
        yaml.dump(new_obj, f, allow_unicode=True, Dumper=Dumper)
    print("配置文件已生成", path)


def get_secret(path):
    with open(path, "r", encoding="utf8") as f:
        custom_data = yaml.load(f, Loader=Loader)
    secret = custom_data["secret"] if "secret" in custom_data else ""
    return secret


def run_api(path):
    secret = get_secret(path)
    reload_config(path, secret=secret)
    print("已重载配置", path)
    all_connections("delete", secret=secret)
    print("已清空连接")


def upload_gist(
    customPath, outPath, filterArr=[], gistPath="../clash-rule-providers-gist"
):
    Path(f"{gistPath}").mkdir(exist_ok=True)
    gistPath = f"{gistPath}/{outPath}"

    copyfile(outPath, gistPath)

    with open(gistPath, "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=Loader)
    for i in data["proxy-providers"]:
        k = data["proxy-providers"][i]
        for r in filterArr:
            k["url"] = k["url"].replace(r, "")
    with open(gistPath, "w", encoding="utf8") as f:
        yaml.dump(data, f, allow_unicode=True, Dumper=Dumper)


if __name__ == "__main__":
    customPath = "config.custom.yaml"
    outPath = "config.yaml"
    run_build_config(Path(customPath).resolve().as_posix())
    run_api(Path(outPath).resolve().as_posix())
    upload_gist(
        customPath,
        outPath,
        filterArr=["http://127.0.0.1:25500/sub?target=clash&url="],
        gistPath="../clash-rule-providers-gist",
    )
