#!/usr/bin/env python3
"""检查所有叶子节点文档的内容长度"""

# 所有叶子节点文档列表
leaf_docs = [
    # 顶层叶子节点 (6 个)
    {"title": "ChainTrace 项目介绍", "obj_token": "BdaCd4uzEowcyXxAzjucUpvKn1e", "checked": True, "length": 4058},
    {"title": "ChainTrace 企业级架构文档索引", "obj_token": "GQeAdiOudoIJNPxDNnKcQ3aLnN5", "checked": True, "length": 3871},
    {"title": "ChainTrace-Bug 管理", "obj_token": "AiKyd58g5oOCVHxyVbLci9MNnig", "checked": True, "length": 4500},
    {"title": "ChainTrace-上线文档 v1.0", "obj_token": "TIoDdHtJIoC0dhxXLzzcQUT7n0d", "checked": True, "length": 5500},
    {"title": "ChainTrace 写给项目新成员的项目介绍文档", "obj_token": "Fp5ad7BQQoic4uxleEAcZvu5nXd", "checked": True, "length": 6000},
    {"title": "README", "obj_token": "PjlmdHNK7oxQEzxdTi0crVv1nlh", "checked": True, "length": 7856},
    
    # 架构设计文档的子节点 (10 个)
    {"title": "引入可信数据空间的方案分析", "obj_token": "U8LWdyGOyoVAHQxJ4S0cjAm2nBd", "checked": True, "length": 2109},
    {"title": "可信数据空间（阶段二：隐私计算）架构 v1.0 副本", "obj_token": "VajtdXdPdoXtgCx1U8BcvVSqn2f", "checked": True, "length": 3742},
    {"title": "ChainTrace 总架构设计文档 v1.0", "obj_token": "XaeEdt5SHoXVR2x6eAcccfFqnQf", "checked": True, "length": 18229},
    {"title": "ChainTrace 链上溯源平台 - 用户端（C 端）架构设计文档 v1.0", "obj_token": "QzOgdWxF0oA8ENxJfpac8ihpnDO", "checked": True, "length": 20363},
    {"title": "ChainTrace 链上溯源平台 - 商家端（B 端）架构设计文档 v1.0", "obj_token": "A3CTdg3Rooy4onxof0Jc8zTinUh", "checked": True, "length": 39624},
    {"title": "ChainTrace 链上溯源平台 - 管理端（A 端）架构设计文档 v1.0", "obj_token": "Nu5WdYWTSoi1Z5xLC29cZPwWnJh", "checked": False, "length": 0},
    {"title": "ChainTrace 功能模块图", "obj_token": "RTNhdbnULojcIlx1XqmcYiWOnJg", "checked": False, "length": 0},
    {"title": "ChainTrace 用户端（C 端）功能手册（网页端）", "obj_token": "Bj8jdfsoWovEjexBC2ZcqU7Bnce", "checked": False, "length": 0},
    {"title": "ChainTrace 商家端（B 端）功能手册（网页端）", "obj_token": "AGw1dtdEZo7LXpx9VYfc5ljwn8g", "checked": False, "length": 0},
    {"title": "ChainTrace 管理端（A 端）功能手册（网页端）", "obj_token": "A2iidew9goyAUBxv24VchfOvnhb", "checked": False, "length": 0},
    
    # 权益设计文档的子节点 (2 个)
    {"title": "ChainTrace 用户端（C 端）会员权益设计文档 v1.0", "obj_token": "Nh8LdT17To8b92x23QMcvhsInih", "checked": False, "length": 0},
    {"title": "ChainTrace 商家端（B 端）权益设计文档 v1.0", "obj_token": "IxJWdG90ho3R0VxEOJIcU820nmg", "checked": False, "length": 0},
    
    # 开发设计文档的子节点 (15 个)
    {"title": "ChainTrace 接口需求表", "obj_token": "Tnt1dHnsMob2JqxWlUPcrqfLn2b", "checked": False, "length": 0},
    {"title": "ChainTrace 技术选型", "obj_token": "MuwDdOi2xokuwHx0h8FcOqP1nbb", "checked": False, "length": 0},
    {"title": "ChainTrace 后端架构设计", "obj_token": "NBs1dG4laol1ywxbyqFcSKqxnMx", "checked": False, "length": 0},
    {"title": "ChainTrace 前端架构设计", "obj_token": "ERljdDYHDoWi2ixhiUCcZ32Zn0f", "checked": False, "length": 0},
    {"title": "ChainTrace 数据库结构设计", "obj_token": "OPxnd0i14oId8SxAWlAcfgv1nOf", "checked": False, "length": 0},
    {"title": "ChainTrace 部署方案设计", "obj_token": "ROHddOTWsoBnt2x4SR7c5EZenKe", "checked": False, "length": 0},
    {"title": "ChainTrace 子模块接口文档", "obj_token": "TYDTdNIRfo1Mtxx2GYrck8iznhc", "checked": False, "length": 0},
    {"title": "ChainTrace 用户端（C 端）注册登录流程设计", "obj_token": "TKaCdNUEho2jmdxv81McNNFjnJc", "checked": False, "length": 0},
    {"title": "ChainTrace 商家端（B 端）注册登录流程设计", "obj_token": "Vm4ndFU2boRRkBxTCC9cpG4Nnqg", "checked": False, "length": 0},
    {"title": "ChainTrace 管理端（A 端）注册登录流程设计", "obj_token": "LVCydcPIPoebCxxEcKHcpn0pnBd", "checked": False, "length": 0},
    {"title": "ChainTrace 支付模块设计", "obj_token": "IQSVdFib2odrC7xhrBBcRYEEnrh", "checked": False, "length": 0},
    {"title": "ChainTrace 交易链路可视化设计", "obj_token": "Wts4dxPpcoXQFMx0EjKcs4gsnqf", "checked": False, "length": 0},
    {"title": "ChainTrace 欺诈分析可视化设计", "obj_token": "Tl4VdJ8mfoRidJxQGvVc3M16nvb", "checked": False, "length": 0},
    {"title": "链上追踪溯源模块设计", "obj_token": "Q27SdNjJLohtmyx0QFfcX7PDnLd", "checked": False, "length": 0},
    {"title": "智能分析报告模块设计", "obj_token": "Nt6qdI4n1oQS2axcnJ0cN4msnHh", "checked": False, "length": 0},
    {"title": "ChainTrace 风控模块设计", "obj_token": "UjqpdXMpqoJsIWxQFk6cIYfQnQf", "checked": False, "length": 0},
    {"title": "ChainTrace 用户端（C 端）创作发布流程设计", "obj_token": "P35wd8Mr2oImwyxNNGCcsjZ6nYe", "checked": False, "length": 0},
    
    # 开发协作文档的子节点 (5 个)
    {"title": "ChainTrace 前端开发协作指南", "obj_token": "VCcMdPS4mou4WUxyCrqc62rPnXb", "checked": False, "length": 0},
    {"title": "ChainTrace 后端开发协作指南", "obj_token": "EpqndkKwLo0drnxZPhQcEi2bnSf", "checked": False, "length": 0},
    {"title": "ChainTrace 前后端联调", "obj_token": "G0M8dNbUkomOipxwXa5c5FznnJd", "checked": False, "length": 0},
    {"title": "ChainTrace-Git 版本管理规范", "obj_token": "EaUjdJHJtoJ1fRxWG3ocEHV5nKh", "checked": False, "length": 0},
    {"title": "ChainTrace 开发协作指南 v1.0", "obj_token": "X1hgd9k5GoWKzqxrvTOcfTuOn4e", "checked": False, "length": 0},
    
    # 算法开发文档的子节点 (4 个)
    {"title": "ChainTrace 总算法设计文档 v1.0", "obj_token": "E3kmdfzxQoiVx5xaAylcEtIYnXD", "checked": False, "length": 0},
    {"title": "混币穿透算法", "obj_token": "NCgPdetigobu2fxbyP5cZabhnXf", "checked": False, "length": 0},
    {"title": "隐私币标记算法", "obj_token": "HHKIdtSGlombl9xXzCBchVfsn6g", "checked": False, "length": 0},
    {"title": "风险指数算法", "obj_token": "JzmBdKzb7oOTTlxq90ic6QRHnFe", "checked": False, "length": 0},
    
    # 艺术设计文档的子节点 (2 个)
    {"title": "ChainTrace-UI/UX设计", "obj_token": "XoeId7v2OoaZUAxMsPicLvDMn4e", "checked": False, "length": 0},
    {"title": "ChainTrace-logo/品牌设计", "obj_token": "VFfldf1YQo4nSuxKlKWcHkkQnth", "checked": False, "length": 0},
]

# 统计
checked = sum(1 for d in leaf_docs if d["checked"])
unchecked = sum(1 for d in leaf_docs if not d["checked"])
blank = sum(1 for d in leaf_docs if d["length"] == 0)

print(f"总计：{len(leaf_docs)} 个叶子节点文档")
print(f"已检查：{checked} 个")
print(f"未检查：{unchecked} 个")
print(f"空白文档 (length=0): {blank} 个")

print("\n=== 空白文档列表 ===")
for doc in leaf_docs:
    if doc["length"] == 0:
        print(f"  - {doc['title']} ({doc['obj_token']})")
