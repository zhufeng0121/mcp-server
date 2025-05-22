import argparse
import logging
import os
from time import struct_time

from typing import Dict, Optional, Final, Any
from mcp.server import FastMCP
from volcengine.example.viking_knowledgebase.example import viking_knowledgebase_service
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 这个port的环境变量确认一下
mcp = FastMCP("Knowledgebase MCP Server", port = int(os.getenv("MCP_KNOWLEDGE_SERVER_PORT", 8080)))

@mcp.tool()
def list_collections(
        project: str,
) ->Dict:
    """
    List all collections of your from the Viking Knowledgebase service.
    This tool allows you to list all collections in the Viking Knowledgebase service.

    Args:
         project: the project of the knowledge base collection.
    """

    try:
        result = viking_knowledgebase_service.list_collections(project=project)
        return result.get("collection_list")
    except Exception as e:
        logger.error(f"Error in list_collections: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def search_knowledge(
        query: str,
        collection_name: str,
        project: str,
        limit: int = 3,
) -> Dict:
    """Search knowledge from the Viking Knowledgebase service.
    This tool allows you to search knowledge in provided collection based on the given query.

    Args:
        query: the search query string.
        limit: the maximum number of results to return (default: 3).
        collection_name: the name of the knowledge base collection to search for.
        project: the project of the knowledge base collection.
    """

    logger.info(f"Received search_knowledge request with query: {query}, limit: {limit}")

    try:
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")
        result = viking_knowledgebase_service.search_knowledge(
            collection_name=collection_name,
            query=query,
            limit=limit,
            dense_weight=0.5,
            project=project,
        )
        return result.get("result_list")
    except Exception as e:
        logger.error(f"Error in search_knowledge: {str(e)}")
        return {"error": str(e)}


def main():
    """Main entry point for the Knowledgebase MCP server."""
    parser = argparse.ArgumentParser(description='Run the Viking Knowledgebase MCP Server')
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()

    logger.info(f"Starting Knowledgebase MCP Server with {args.transport} transport")

    try:

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Knowledgebase MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()