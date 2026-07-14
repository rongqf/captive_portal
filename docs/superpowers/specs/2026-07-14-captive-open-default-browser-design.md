# 认证成功后唤起默认浏览器 — 设计

**日期:** 2026-07-14  
**状态:** 已确认（方案 A）

## 目标

用户在强制门户点击登录并完成网关认证后，在成功页尝试唤起手机默认浏览器，打开规定落地页。

## 流程

1. 登录页跳转网关 `authaction`（现有逻辑不变）
2. 网关认证成功后 `redir` 到现有 `OPENNDS_OK_URL` → `/auth/opennds/ok`
3. `ok.html` 加载后：上报 `auth_ok` → 尝试唤起系统浏览器打开落地 URL → 保留手动链接兜底

## 落地 URL（测试阶段）

`http://115.190.191.173:8000/test`

后续可抽到配置；测试阶段可写在成功页或配置常量中。

## 改动范围

- 修改：`src/templates/ok.html`
- 可选：`src/configs/site_settings.py` 增加 `POST_AUTH_BROWSER_URL`
- 不改：`auth_opennds.py` 认证拼装

## 唤起策略

- Android：`intent://host/path#Intent;scheme=http|https;end`
- iOS：尝试 `x-safari-http(s)://...`
- 兜底：页面上「在浏览器中打开」普通 `<a href>`

## 约束

- 系统强制门户 WebView 可能拦截自动唤起，不保证 100% 成功
- WiFiDog `/portal/` 共用 `ok.html`，行为一致
