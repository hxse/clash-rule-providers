#!/usr/bin/env python3
# coding: utf-8
import yaml

with open("config.custom.yaml", "r", encoding="utf8") as f:
    custom_data = yaml.safe_load(f)

with open("config.template.yaml", "r", encoding="utf8") as f:
    template_data = yaml.safe_load(f)
    template_providers = template_data["proxy-providers"]
    custom_providers = custom_data["proxy-providers"]
    for template_name in template_providers:
        custom_item = custom_providers[template_name]
        template_item = template_providers[template_name]
        for custom_k, custom_v in custom_item.items():
            template_item[custom_k] = custom_v

    fields = [
        "mixed-port",
        "allow-lan",
        "mode",
        "log-level",
        "external-controller",
        "rules",
    ]
    assert "rules" in custom_data, "请定义rules字段"
    for i in fields:
        if i in template_data and i in custom_data:
            template_data[i] = custom_data[i]

with open("config.yaml", "w", encoding="utf8") as f:
    yaml.dump(template_data, f, allow_unicode=True)
