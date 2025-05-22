import argparse
import logging
import os
import requests

from typing import Dict, Optional, Final, Any
from mcp.server import FastMCP
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService
from server.mcp_server_knowledgebase.src.mcp_server_knowledgebase.config import config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Global variables
knowledgebase_service: Optional[VikingKnowledgeBaseService] = None

# Create MCP server
mcp = FastMCP("Knowledgebase MCP Server", port=int(os.getenv("PORT", "8000")))


@mcp.tool()
def get_collection(
        collection_name: str,
        project: str,
) -> Dict:
    """
    Get information about a collection from your project.
    This tool allows you to get information about a collection from your project by collection_name.
    Args:
         project: the project of the knowledge base collection.
         collection_name: the name of the knowledge base collection to get info for.
    """

    try:
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")

        collection = knowledgebase_service.get_collection(collection_name, project)
        return collection

    except Exception as e:
        logger.error(f"Error in get_collection: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_doc(
        doc_id: str,
        project: str,
        collection_name: str,
) -> Dict:
    """
    Get information about a document from your collection.
    This tool allows you to get information about a document from your collection by doc_id and collection_name.

    Args:
         project: the project of the knowledge base collection.
         collection_name: the name of the knowledge base collection to get doc info for.
         doc_id: the id of the doc to get info.

    Returns:
        the status of the doc.
        process_status: the status of the doc.
        process_status = 0: the doc is not processed finished.
        process_status = 1: the doc is processed failed.
        process_status = 2: the doc is wait for processing in line.
        process_status = 3: the doc is wait for processing in line.
        process_status = 5: the doc is deleting.
        process_status = 6: the doc is processing.
    """

    try:
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")
        elif not doc_id:
            raise ValueError("Doc ID cannot be empty.")

        collection = knowledgebase_service.get_collection(collection_name, project)

        doc_info = collection.get_doc(project=project, doc_id=doc_id)
        return doc_info.get("status").get("process_status")
    except Exception as e:
        logger.error(f"Error in get_doc: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def list_collections(
        project: str,
) ->Dict:
    """
    List all collections of your from the Viking Knowledgebase service.
    This tool allows you to list all collections in the Viking Knowledgebase service.

    Args:
         project: the project user want to list collections for.
    """

    try:
        result = knowledgebase_service.list_collections(project=project)
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
        result = knowledgebase_service.search_knowledge(
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
        global knowledgebase_service

        knowledgebase_service = VikingKnowledgeBaseService(
            host=config.host,
            scheme="https",
            connection_timeout=30,
            socket_timeout=30,
        )
        knowledgebase_service.set_ak(config.ak)
        knowledgebase_service.set_sk(config.sk)

        logger.info(
            f"Initialized Viking Knowledge Base service for host: {config.host}, collection: {config.collection_name}"
        )

        # Run the MCP server
        logger.info(
            f"Starting Viking Knowledge Base MCP Server with {args.transport} transport"
        )

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Knowledgebase MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()