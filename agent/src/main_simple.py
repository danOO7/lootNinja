"""
Simple Agent Server - Runs the simple request agent.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

from simple_agent import agent, StateDeps, RequestState


def create_app():
    """Create and configure the FastAPI app."""
    return agent.to_ag_ui(deps=StateDeps(RequestState()))


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
