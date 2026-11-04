# AI 中医项目（ai_chinese_medical_project）

## 目录结构

```
ai_chinese_medical_project/
├── __000__demo/
│   └── __001__clawler_demo/
│       └── 爬虫基础.py        # 爬虫基础练习
├── .gitignore
└── README.md
```

## 环境配置

### 1. 安装 Conda

如果还没有安装，推荐安装 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)。安装完成后在终端验证：

```bash
conda --version
```

### 2. 创建并激活虚拟环境

```bash
# 创建环境（Python 3.12）
conda create -n env_chinese_medical python=3.12 -y

# 激活环境
conda activate env_chinese_medical

# 确认 Python 版本和路径
python --version
which python
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

> 项目暂时还没有 `requirements.txt`。新增依赖后，可以运行 `pip freeze > requirements.txt` 生成或更新。

### 4. 常用 Conda 命令

| 操作 | 命令 |
|---|---|
| 查看所有环境 | `conda env list` |
| 退出当前环境 | `conda deactivate` |
| 删除环境 | `conda remove -n env_chinese_medical --all` |
| 导出环境 | `conda env export > environment.yml` |
| 从文件恢复环境 | `conda env create -f environment.yml` |

## 编辑器配置（Cursor / VS Code）

### 1. 安装扩展

| 扩展 | 发布者 | 说明 |
|---|---|---|
| **Python** | ms-python | 必装，会自动带上 Python Debugger 和 Python Environments |
| **Pyrefly** | meta | 可选，提供代码补全、跳转定义、类型检查 |

### 2. 选择解释器

1. `Cmd + Shift + P` → 输入 `Python: Select Interpreter`
2. 选择 `env_chinese_medical`
3. 如果列表里没有，选 **Enter interpreter path...**，填入 `which python` 输出的路径（激活环境后执行），一般是：
   ```
   ~/miniconda3/envs/env_chinese_medical/bin/python
   ```

选好后，打开任意 `.py` 文件，右下角状态栏会显示 `3.12.x ('env_chinese_medical')`。

### 3. 常见问题

- **命令面板里找不到 `Python: Select Interpreter`**：没装 Python 扩展。装好后执行 `Developer: Reload Window`。
- **Pyrefly 的红色波浪线太多**：在设置中搜索 `pyrefly.typeCheckingMode`，调低检查级别。
