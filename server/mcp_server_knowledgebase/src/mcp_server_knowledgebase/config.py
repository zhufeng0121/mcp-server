import os
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeBaseConfig:
    """Configuration for Viking Knowledge Base MCP Server."""

    host: str
    ak: str
    sk: str
    collection_name: Optional[str] = None
    project: Optional[str] = None


def load_config() -> KnowledgeBaseConfig:
    """Load configuration from environment variables."""
    required_vars = [
        "VOLCENGINE_ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY",
    ]

    # Check if all required environment variables are set
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Load configuration from environment variables
    return KnowledgeBaseConfig(
        ak=os.environ["VOLCENGINE_ACCESS_KEY"],
        sk=os.environ["VOLCENGINE_SECRET_KEY"],
        host=os.getenv("VIKING_KB_HOST", "api-knowledgebase.mlp.cn-beijing.volces.com"),
        collection_name=os.getenv("VIKING_KB_COLLECTION_NAME", None),
        project=os.getenv("VIKING_KB_PROJECT", None),
    )


config = load_config()
