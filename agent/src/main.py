import uvicorn

from agent import agent, StateDeps, GiftScoutState


def create_app():
    """Create and configure the FastAPI app."""
    return agent.to_ag_ui(deps=StateDeps(GiftScoutState()))


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )