#!/usr/bin/env python3
"""递归查找所有叶子节点文档"""

import json

# 已知的文档结构（根据之前的查询结果）
docs_tree = {
    "ChainTrace 架构设计文档 v1.0": {
        "node_token": "SB4mwgqHoiDqm7k0tQlcQo2Bnzb",
        "has_child": True,
        "children": [
            {"title": "引入可信数据空间的方案分析", "has_child": False, "obj_token": "U8LWdyGOyoVAHQxJ4S0cjAm2nBd"},
            {"title": "可信数据空间（阶段二：隐私计算）架构 v1.0 副本", "has_child": False, "obj_token": "VajtdXdPdoXtgCx1U8BcvVSqn2f"},
            {"title": "ChainTrace 总架构设计文档 v1.0", "has_child": False, "obj_token": "XaeEdt5SHoXVR2x6eAcccfFqnQf"},
            {"title": "ChainTrace 链上溯源平台 - 用户端（C 端）架构设计文档 v1.0", "has_child": False, "obj_token": "QzOgdWxF0oA8ENxJfpac8ihpnDO"},
            {"title": "ChainTrace 链上溯源平台 - 商家端（B 端）架构设计文档 v1.0", "has_child": False, "obj_token": "A3CTdg3Rooy4onxof0Jc8zTinUh"},
            {"title": "ChainTrace 链上溯源平台 - 管理端（A 端）架构设计文档 v1.0", "has_child": False, "obj_token": "Nu5WdYWTSoi1Z5xLC29cZPwWnJh"},
            {"title": "ChainTrace 功能模块图", "has_child": False, "obj_token": "RTNhdbnULojcIlx1XqmcYiWOnJg"},
            {"title": "ChainTrace 用户端（C 端）功能手册（网页端）", "has_child": False, "obj_token": "Bj8jdfsoWovEjexBC2ZcqU7Bnce"},
            {"title": "ChainTrace 商家端（B 端）功能手册（网页端）", "has_child": False, "obj_token": "AGw1dtdEZo7LXpx9VYfc5ljwn8g"},
            {"title": "ChainTrace 管理端（A 端）功能手册（网页端）", "has_child": False, "obj_token": "A2iidew9goyAUBxv24VchfOvnhb"},
        ]
    },
    "ChainTrace 权益设计文档 v1.0": {
        "node_token": "MS00wMvxaiQE8AkAWqZcKlRwn2e",
        "has_child": True,
        "children": []  # 需要查询
    },
    "ChainTrace 开发设计文档 v1.0": {
        "node_token": "FMuiwMarNioMPCkvNtCcsirin2g",
        "has_child": True,
        "children": []  # 需要查询
    },
    "ChainTrace 开发协作文档 v1.0": {
        "node_token": "DYBUw3gDFihoPlkgbjucek0rnRh",
        "has_child": True,
        "children": []  # 需要查询
    },
    "ChainTrace 算法开发文档 v1.0": {
        "node_token": "HiIiwEmfUiFM4SkZOfpcdHxNnND",
        "has_child": True,
        "children": []  # 需要查询
    },
    "ChainTrace 艺术设计文档 v1.0": {
        "node_token": "TqKvwAbYTiyIt3kcIs5c7ysXnFe",
        "has_child": True,
        "children": []  # 需要查询
    },
}

# 叶子节点（has_child=False 的顶层文档）
leaf_nodes_top = [
    {"title": "ChainTrace 项目介绍", "obj_token": "BdaCd4uzEowcyXxAzjucUpvKn1e", "has_child": False},
    {"title": "ChainTrace 企业级架构文档索引", "obj_token": "GQeAdiOudoIJNPxDNnKcQ3aLnN5", "has_child": False},
    {"title": "ChainTrace-Bug 管理", "obj_token": "AiKyd58g5oOCVHxyVbLci9MNnig", "has_child": False},
    {"title": "ChainTrace-上线文档 v1.0", "obj_token": "TIoDdHtJIoC0dhxXLzzcQUT7n0d", "has_child": False},
    {"title": "ChainTrace 写给项目新成员的项目介绍文档", "obj_token": "Fp5ad7BQQoic4uxleEAcZvu5nXd", "has_child": False},
    {"title": "README", "obj_token": "PjlmdHNK7oxQEzxdTi0crVv1nlh", "has_child": False},
]

print("=== 顶层叶子节点 ===")
for doc in leaf_nodes_top:
    print(f"  - {doc['title']} ({doc['obj_token']})")

print("\n=== 架构设计文档的子节点（叶子） ===")
for child in docs_tree["ChainTrace 架构设计文档 v1.0"]["children"]:
    print(f"  - {child['title']} ({child['obj_token']})")

print("\n=== 需要查询子文档的节点 ===")
for title, info in docs_tree.items():
    if info["has_child"] and not info["children"]:
        print(f"  - {title} (node_token: {info['node_token']})")
