# 认证成功唤起默认浏览器 — Implementation Plan

> **For agentic workers:** Implement task-by-task. Steps use checkbox syntax.

**Goal:** 认证成功页尝试唤起默认浏览器打开 `/test` 落地页，并提供手动链接兜底。

**Architecture:** 认证链路不变；仅在 `ok.html` 增加唤起逻辑与配置项。

**Tech Stack:** Jinja2 模板 + 少量前端 JS；可选 `site_settings` 常量。

---

### Task 1: 配置落地 URL

- [ ] 在 `src/configs/site_settings.py` 增加 `POST_AUTH_BROWSER_URL = 'http://115.190.191.173:8000/test'`
- [ ] 在 `auth_opennds.py` 与 `auth_wifidogx.py` 的 ok/portal 响应 context 传入该 URL

### Task 2: 修改 ok.html

- [ ] 增加「在浏览器中打开」链接指向落地 URL
- [ ] DOMContentLoaded 中：reportAction 后按 UA 尝试 intent / x-safari 唤起
- [ ] 自动唤起失败时依赖手动链接

### Task 3: 验证

- [ ] 本地打开 ok 页确认链接与脚本无语法错误
- [ ] 真机：登录 → 成功页 → 观察是否打开默认浏览器到 `/test`
