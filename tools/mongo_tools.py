from utils.mongo_utils import init_mongo
from langfuse import observe


@observe()
def get_team_boxscores(team_name: str) -> list[dict]:
    """
    Fetch all stored boxscores for a given team.
    """
    collection = init_mongo()
    return list(collection.find({"team_name": team_name}))

@observe()
def extract_players_from_games(mongo_docs: list[dict]) -> list[str]:
    """
    Extract unique player names from stored boxscore documents.
    """
    players = set()

    for game in mongo_docs:
        boxscore = game.get("boxscore", {})
        team_data = next(iter(boxscore.values()), {})

        for player in team_data.get("Players", []):
            name = player.get("Player")
            if name:
                players.add(name)

    return sorted(players)