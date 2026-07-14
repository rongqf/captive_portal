import os

PORT = 8000

DB_URI_OTC = 'postgresql+psycopg2://captive_portal:captive_portal@101.201.74.166:5432/captive_portal'

OPENNDS_OK_URL = os.environ.get(
    'OPENNDS_OK_URL',
    'http://115.190.191.173:8000/auth/opennds/ok',
)
# 认证成功后尝试用默认浏览器打开的落地页；测试/生产通过环境变量配置，勿写死测试 IP
POST_AUTH_BROWSER_URL = os.environ.get('POST_AUTH_BROWSER_URL', '')
