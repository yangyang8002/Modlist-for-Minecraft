- en [English](README.md)
- zh_CN [简体中文](README.zh_CN.md)

# Minecraft 模组清单扫描器

一款 Python 工具，用于扫描 Minecraft 模组目录并生成包含模组 ID、名称和版本的整洁 JSON 列表。

[![Python 版本](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![开源协议: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 功能特点

- 🧩 支持所有主流模组加载器：Forge、NeoForge、Fabric 和 Quilt
- 🔍 递归扫描目录中的模组文件
- 🧹 通过移除特殊字符来清理模组名称和版本号
- 💾 输出包含 modid、名称和版本的整洁 JSON
- 🛡️ 处理特殊字符和非标准 JAR 文件
- 📋 提供已处理和已跳过文件的详细报告

## 安装说明

1. 克隆代码库：
```bash
git clone https://github.com/yangyang8002/Modlist-for-Minecraft.git
cd Modlist-for-Minecraft
```

2. 确保已安装 Python 3.6 或更高版本。

## 使用方法

### 基本使用
运行脚本并按照提示操作：
```bash
python mod_scanner.py
```

### 命令行选项
指定目录路径运行：
```bash
python mod_scanner.py --directory "path/to/your/mods"
```

静默模式（仅显示错误和最终结果）：
```bash
python mod_scanner.py --quiet
```

指定输出文件：
```bash
python mod_scanner.py --output custom_mods.json
```

### 输出示例
脚本将生成包含以下结构的 `mods.json` 文件：
```json
[
  {
    "modid": "jei",
    "name": "Just Enough Items",
    "version": "11.2.0.256"
  },
  {
    "modid": "lazydfu",
    "name": "LazyDFU",
    "version": "0.1.3"
  }
]
```

## 支持的文件类型
扫描器将处理以下扩展名的文件：
- `.jar`（标准模组文件）
- `.zip`（某些模组使用 zip 格式）
- `.disabled`（已禁用的模组）

## 工作原理
扫描器会：
1. 递归搜索指定目录
2. 将每个模组文件作为 ZIP 存档打开
3. 按以下顺序查找模组元数据文件：
   - `fabric.mod.json`（Fabric/Quilt 模组）
   - `mods.toml`（Forge/NeoForge 模组）
   - `mcmod.info`（旧版 Forge 模组）
4. 如果未找到元数据，则从文件名提取信息
5. 通过移除特殊字符（如 `#mandatory` 和 `\`）来清理数据
6. 将结果输出到 JSON 文件

## 故障排除

### 已知问题
1. 请批量将“#mandatory”一词和反斜杠“\”替换为空（即删除它们）。

### 常见问题
1. **权限错误**：如果扫描受保护目录，请以管理员/root 身份运行脚本
2. **损坏的模组文件**：尝试重新下载导致错误的任何模组
3. **特殊字符**：脚本可处理大多数特殊字符，但极度畸形的文件名可能会导致问题

### 问题报告
如果遇到任何问题，请：
1. 使用 `--debug` 标志运行脚本
2. 记下导致问题的模组文件
3. [提交问题](https://github.com/yangyang8002/Modlist-for-Minecraft/issues)并提供这些信息

## 贡献指南
欢迎贡献代码！请遵循以下步骤：
1. Fork 本代码库
2. 为您的功能创建新分支
3. 提交更改
4. 提交拉取请求

## 开源协议
本项目采用 MIT 开源协议 - 详见 [LICENSE](LICENSE) 文件。

---

**注意**：此工具与 Minecraft、Mojang 或 Microsoft 无关联。Minecraft 是 Mojang Studios 的商标。
