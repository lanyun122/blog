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

## 五、Channels连接

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

- 企业微信插件安装命令：
```powershell
npx -y @wecom/wecom-openclaw-cli install
```
- 企业微信扫码创建机器人，如果提示有问题，就重新输入openclaw config配置机器人ID和Secret

- 配对代码命令：
```powershell
openclaw pairing approve wecom <配对码>
```
### 3.1微信配置

* 微信插件安装命令
```powershell
npx -y @tencent-weixin/openclaw-weixin-cli@latest install
```

## 六、Skills（技能）安装

* 官方Skills（技能）网站：[https://clawhub.ai/](https://clawhub.ai/)
* Self-Improving + Proactive Agent（自我进化技能）：[点击跳转](https://clawhub.ai/ivangdavila/self-improving)
* Tavily AI Search（联网搜索技能）：[点击跳转](https://clawhub.ai/bert-builder/tavily)
* Multi Search Engine（多搜索引擎技能）：[点击跳转](https://clawhub.ai/gpyAngyoujun/multi-search-engine)
* 浏览器控制扩展程序，Windows、Mac通用：Chrome浏览器拓展商店搜索（OpenClaw Browser Relay for Windows）

## 七、多Agent创建

- 创建Agent命令
```powershell
openclaw agents add <agent名称>
```
- 然后让AI辅助，确定各Agent的角色定位、以及协作运行规则
- 再让Openclaw主模型，自行设置

## 常用命令

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
npm uninstall openclaw
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

#### 待测试命令

配置多模型 命令
```powershell
# 配置多模型 
openclaw config set models.default "openai/gpt-4" 
openclaw config set models.fallback "anthropic/claude-3-haiku"
```

命令
```powershell

```
命令
```powershell

```

命令
```powershell

```

命令
```powershell

```

命令
```powershell

```