import os
import json
import logging

logger = logging.getLogger(__name__)


class KnowledgebaseConfig:
    """Configuration for Knowledgebase MCP Server."""
    region: str
    access_key_id: str
    access_key_secret: str
    account_id: str

    def __init__(self, region, access_key_id, access_key_secret, account_id):
        self.region = region
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.account_id = account_id


def load_config(config_path: str = None) -> KnowledgebaseConfig:
    """Load configuration from config file or environment variables."""

    # 优先从config文件中加载配置
    if config_path:
        try:
            with open(config_path) as f:
                config_data = json.load(f)
                env_vars = config_data.get('env', {})
                return KnowledgebaseConfig(
                    region=env_vars.get("VOLCENGINE_REGION", os.getenv("VOLCENGINE_REGION", "cn-beijing")),
                    access_key_id=env_vars.get("VOLCENGINE_ACCESS_KEY", os.environ["VOLCENGINE_ACCESS_KEY"]),
                    access_key_secret=env_vars.get("VOLCENGINE_SECRET_KEY", os.environ["VOLCENGINE_SECRET_KEY"]),
                    account_id=env_vars.get("ACCOUNT_ID", os.getenv("ACCOUNT_ID", ""))
                )
        except Exception as e:
            logger.error(f"Failed to load config from {config_path}: {e}")

    # 从环境变量中加载配置
    required_vars = ["VOLCENGINE_ACCESS_KEY", "VOLCENGINE_SECRET_KEY", "VOLCENGINE_REGION"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return KnowledgebaseConfig(
        region=os.environ.get("VOLCENGINE_REGION", "cn-beijing"),
        access_key_id=os.environ.get("VOLCENGINE_ACCESS_KEY"),
        access_key_secret=os.environ.get("VOLCENGINE_SECRET_KEY"),
        account_id=os.environ.get("ACCOUNT_ID", "")
    )