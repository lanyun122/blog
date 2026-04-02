---
date: 2026-03-25
categories:
  - 工具
tags:
  - 工具
  - AI
---
# Openclaw 安装、使用文档（Mac、Windows）

![封面](../assets/images/Openclaw图片01.png){ width="300" align=left style="border-radius: 8px; margin-right: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;" }

**本期要点：** 常用相关网站、安装步骤及相关代码（Windows、Mac系统）、常用命令。

<div style="margin-top: 25px; text-align: center;">
  <a href="https://www.youtube.com/watch?v=YbGr_9poheM&t=34s" target="_blank" class="md-button md-button--neutral" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 24px; font-size: 0.85rem; border-radius: 20px; text-decoration: none; font-weight: bold; border: 1px solid rgba(0,0,0,0.1); transition: all 0.3s ease;">
    <svg viewBox="0 0 576 512" style="height: 1.1em; fill: #FF0000; margin: 0; display: block;">
      <path d="M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.781 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z"/>
    </svg>
    立即观看完整视频
  </a>
</div>
<br clear="left">

<!-- more -->

## 一、常用网址

* Openclaw 官网：[https://openclaw.ai/](https://openclaw.ai/)
* Node.js 官网（中国区）：[https://nodejs.org/zh-cn](https://nodejs.org/zh-cn)
* Git 官网地址：[https://git-scm.com/](https://git-scm.com/)

---

## 二、准备工具
* 远程控制软件（Todesk）：[https://www.todesk.com](https://www.todesk.com/download.html)
* 代理软件（V2rayN）:[https://github.com/2dust/v2rayN](https://github.com/2dust/v2rayN)


---

## 三、Windows 版本安装方法

### 1. 安装 Node.js + npm
* 下载地址 Node.js 官网（中国区）[https://nodejs.org/zh-cn](https://nodejs.org/zh-cn)

* 检查node版本命令：
```powershell
node -v # 正确返回结果示例：v24.13.0
```

* 检查npm版本命令
```powershell
npm -v # 正确返回结果示例：11.6.2
```
### 2.安装Git
* 下载地址 Git官网[https://git-scm.com/](https://git-scm.com/)

* 检查git版本命令
```powershell
git --version # 正确返回示例：git version 2.53.0.windows.1
```

### 3.Windows脚本权限开启

- 脚本权限开启命令
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser # 正确返回示例：无
```

- 脚本权限检查命令
```powershell
Get-ExecutionPolicy -Scope CurrentUser # 正确返回示例：RemoteSigned
```

### 4.安装Openclaw命令

- 
```powershell
iwr -useb https://molt.bot/install.ps1 | iex
```

### 5.配置初始化

- 
```powershell
openclaw onboard
```

## 四、苹果Mac系统 安装方法

### 1.安装Apple命令开发工具命令

- 
```zsh
xcode-select --install
```

### 2.安装Homebrew

- 官方命令：
```zsh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- 备用命令（国内源）：
```zsh
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```

- 注意：安装成功 但还需要重启终端 或者运行以下命令，否则国内地址无法生效
```zsh
source /Users/zhyzh9008/.zprofile
```

- 检测Homebrew版本命令：
```zsh
brew --version
```

### 3.安装Git

- 安装命令：
```zsh
brew install git
```

- 版本检查命令：
```zsh
git --version # 正确返回示例：git version 2.39.5（Apple Git-154）
```

### 4.安装Node.js

- 安装命令：
```zsh
brew install node
```

- 版本检查命令：
```zsh
node -v # 正确返回结果示例：v24.14.0
```

- 
```zsh
npm -v # 正确返回结果示例：11.9.0
```

### 5.安装Openclaw

- 官方安装命令：
```zsh
curl -fsSL https://openclaw.ai/install.sh | bash
```

- 通用安装命令：
```zsh
npm install -g openclaw@latest
```

- 管理员身份安装命令：
```zsh
sudo npm install -g openclaw@latest
```

### 6.配置初始化

- 配置初始化命令：
```zsh
openclaw onboard
```

## 五、Ollama部署

* Ollama官网地址：[https://ollama.com/](https://ollama.com/)
* 步骤：下载安装ollama客户端 → 安装客户端 → 注册登录账号（QQ邮箱也可以） → 输入命令启动、部署云模型（每日有免费额度）
* ollama启动openclaw命令：
```
ollama launch openclaw --config
```

## 六、Channels连接

### 1.Telegram连接
- 前提：打开魔法
- Telegram中搜索BotFather，创建机器人，获取token
- 终端输入命令：openclaw config
- 配置channels，选择telegram
- 输入token
- 结束配置
- 在终端中输入：openclaw pairing approve telegram <配对码>
- 重启openclaw
- 完成

### 2.飞书配置（国内）
- 飞书控制台：[https://open.feishu.cn/](https://open.feishu.cn/?lang=zh-CN)
- 飞书插件安装说明网址：[OpenClaw飞书官方插件使用指南（公开版）](https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh)

- 飞书插件安装命令：

```powershell
npx -y @larksuite/openclaw-lark-tools install
```

- 扫码创建机器人
- 重启Openclaw，在飞书的机器人聊天中开启权限：/feishu auth ，根据提示操作

### 3.企业微信配置
- 企业微信插件安装说明网址：[官方文档](https://open.work.weixin.qq.com/help2/pc/21670?person_id=1&searchData=)
- 企业微信插件安装命令：快走快走快
```powershell
npx -y @wecom/wecom-openclaw-cli install
```没空
- 企业微信扫码创建机器人，如果提示有问题，就重新输入openclaw config配置机器人ID和Secret

- 配对代码命令：
```powershell
openclaw pairing approve wecom <配对码>
```

企业微信插件卸载命令：1定要看我是不是
```
openclaw plugins uninstall wecom-openclaw-plugin
```

### 3.1微信配置

* 微信插件安装命令
```powershell
npx -y @tencent-weixin/openclaw-weixin-cli@latest install
```

## 七、Skills（技能）安装

* 官方Skills（技能）网站：[https://clawhub.ai/](https://clawhub.ai/)
* Self-Improving + Proactive Agent（自我进化技能）：[点击跳转](https://clawhub.ai/ivangdavila/self-improving)
* Tavily AI Search（联网搜索技能）：[点击跳转](https://clawhub.ai/bert-builder/tavily)
* Multi Search Engine（多搜索引擎技能）：[点击跳转](https://clawhub.ai/gpyAngyoujun/multi-search-engine)
* 浏览器控制扩展程序，Windows、Mac通用：Chrome浏览器拓展商店搜索（OpenClaw Browser Relay for Windows）

## 八、多Agent创建

- 创建Agent命令
```powershell
openclaw agents add <agent名称>
```
- 然后让AI辅助，确定各Agent的角色定位、以及协作运行规则
- 再让Openclaw主模型，自行设置

- agent查询命令：
```
openclaw agents list
```

- 删除agent命令：
```
 openclaw agents delete <agent名称>
```
## 九、常用命令

启动命令：
```powershell
openclaw gateway
```

Ollama启动命令：
```powershell
ollama launch openclaw --config
```

配置命令：
```powershell
openclaw config
```

诊断命令：
```powershell
openclaw doctor --fix
```

Openclaw更新命令
```powershell
npm install -g openclaw@latest
```

版本检查命令：
```powershell
openclaw --version
```

ClawHub技能安装命令：
```powershell
npx clawhub@latest install <skill-name>
```

Openclaw卸载命令：
```
npm uninstall -g openclaw
```

将Git的SSH地址改为http地址命令：
```powershell
git config --global url."https://github.com/".insteadOf git@github.com:
```

查看npm源命令
```powershell
npm config get registry
```

切换npm源（mac）命令
```powershell
# 切换到淘宝镜像源（永久生效）
npm config set registry https://registry.npmmirror.com

# 恢复到 npm 官方源（如需）
npm config set registry https://registry.npmjs.org/
```

临时关闭证书验证（mac）命令
```powershell
# 临时关闭证书检查并安装 openclaw
sudo npm install -g openclaw@latest --registry=https://registry.npmmirror.com --unsafe-perm=true --allow-root --strict-ssl=false
```

## 十、Token转接平台

### （一）接入指南与定价说明

- 为了满足不同场景下的成本与稳定性需求，为大伙提供了“按量付费”与“月卡订阅”两种服务模式。

#### 1. API 按量付费服务
- 核心业务，支持 OpenAI 格式直接调用。我们提供两条不同技术路径的线路，丰俭由人，按需选择。
- 适用场景： 日常开发、高频调用、测试环境、个人工具集成。
- 定价策略：
  - 兑换比例： 1 RMB = 1 USD 额度
  - （相当于官方原价的 1.4 折，极具市场竞争力）
- 举个例子大伙就明白:
![封面](../assets/images/Claude-Opus-4.6官方Token价格.PNG)
- opus4.6 是5美金/百万token 输入,在咱们网站,你只需要使用5人民币使用同样的量

#### 1. 月卡订阅服务
- 适合不想折腾配置，直接在网页或客户端进行高频、大流量使用的个人开发者与创作者。
- 套餐价格表


| 套餐档位 | 价格 (RMB/月) | 每日刷新额度 | 适用人群 |
| :---: | :---: | :---: | :---: |
| 入门版 | **¥199** | **$15 / 天** | 个人开发者、日常编程辅助 |
| 轻量版 | **¥339** | **$30 / 天** | 个人开发者、日常编程辅助 |
| 标准版 | **¥499** | **$50 / 天** | 重度代码编写、长文档分析 |
| 高级版 | **¥1,118** | **$120 / 天** | 全职独立开发者、AI 极客 |
| 团队版 | **¥1,888** | **$200 / 天** | 极高频用户、小型工作室 |
| 商业版 | **¥4,688** | **$500 / 天** | 资深高频用户、中大型工作室 |
| 企业版 | **¥9,188** | **$1000 / 天** | 资深高频用户、中大型工作室 |


- 帮大伙提前算了,买499的套餐,每天都把50美金用完,相当于一个月能花1500美金,折合下来是0.33人民币/1美金

- 💡 选购建议： 标准版（$50/天）已能满足绝大多数高强度开发需求。如需更高并发或多人共享，可选购或灵活升级（多退少补）高阶套餐。

#### 3. 企业服务与合作
- 企业长期合作： 针对有稳定大额需求的企业客户，我们可以提供定制化 API 部署方案及备用线路保障。
- 合规支持： 支持企业对公转账及开具发票，解决报销与合规后顾之忧。

### （二）购买、使用相关文档

- 闲鱼交付文档：[点击跳转](https://my.feishu.cn/wiki/ZmM6wSSfAiRbWZkR2WGctTO6nXb)

- XueDingtoken｜小白AI无门槛宝典:[点击跳转](https://ocnoacy9az5w.feishu.cn/wiki/YL29wbEzpiAW6hk1DFEctDIenfd)

- Xuedingtoken API 服务接入指南与定价说:[点击跳转](https://ocnoacy9az5w.feishu.cn/wiki/SZDWwE99DiO5o2kRkUhc8ufvnFh?fromScene=spaceOverview)

- Claude Code 安装指南 · 小白操作指南（Windows）:[点击跳转](https://ocnoacy9az5w.feishu.cn/wiki/BJMHwKhRJigezhkJPZ7ccnBsn5c)

- Claude code 安装指南·小白操作指南（MacOS 版本）:[点击跳转](https://ocnoacy9az5w.feishu.cn/wiki/KVSywKq4fih0pikGdlxcVjb8nAe)

- Claude Code 配置指南：快速完成 claude code 配置避坑经验:[点击跳转](https://ocnoacy9az5w.feishu.cn/wiki/HqgGwWd7uictajkWszbcN1Hmnab)

- 如何在 openclaw(小龙虾) 配置 xuedingtoken API 指南:[点击跳转](https://ocnoacy9az5w.feishu.cn/wiki/Gr6kwcH7DirNyVkyoogcPcwqnqf)

- OpenClaw | ClaudeCode | OpenCode  安装教程:[点击跳转](https://ocnoacy9az5w.feishu.cn/wiki/JzMGwg1QSi1QzakHfCdcjTNxnJe)