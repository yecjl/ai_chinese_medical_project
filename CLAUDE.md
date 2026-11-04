# 项目约定

## 依赖管理
- 所有第三方依赖统一写入项目根目录的 `requirements.txt`（整个项目共用一份）。
- 代码中每引入一个新的第三方库，都要同步加入 `requirements.txt`，并加一行注释说明用途。
- 版本写法：`包名>=当前版本`。
- 安装：`pip install -r requirements.txt`

## Git
- 本项目直接在 `main` 分支上提交，不需要新建功能分支。
- 提交信息格式：`type(scope): 中文描述`，正文用 `- ` 列出改动点。
