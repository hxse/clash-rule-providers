#!/usr/bin/env python3
# coding: utf-8
import yaml
from yaml import CSafeLoader as Loader, CSafeDumper as Dumper
from clash_api import reload_config, all_connections
from pathlib import Path


def create_proxy_providers(custom_data, black_list):
    obj = {}
    for i, v in custom_data.items():
        if i in black_list:
            obj[i] = {}
        else:
            obj[i] = v
    return obj


def create_provider(name, obj, interval1=3600, interval2=300):
    return {
        "type": "http",
        "path": f"./profiles/proxies/{name}.yaml",
        "url": obj["url"],
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
    # 匹配前缀,DOG-gatern项,匹配D-default,O-other,G-Game三个组,最好用大写
    res = []
    for group in custom_data["proxy-groups"]:
        res.append(group)
        group["proxies"] = ["DIRECT", "REJECT"]
        for i, v in custom_data["proxy-providers"].items():
            if not enable_match:
                group["proxies"].append(f"{i}_s")
                continue
            if group["name"].split("-")[0] in i.split("-")[0]:
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


def run_api(path):
    reload_config(path)
    print("已重载配置", path)
    all_connections("delete")
    print("已清空连接")


if __name__ == "__main__":
    customPath = "config.custom.yaml"
    outPath = "config.yaml"
    run_build_config(Path(customPath).resolve().as_posix())
    run_api(Path(outPath).resolve().as_posix())
