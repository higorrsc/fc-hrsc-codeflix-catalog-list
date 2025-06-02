from uuid import UUID

from src._shared.infra.client import CodeflixClient
from src._shared.models.video import VideoResponse


class HttpCodeflixClient(CodeflixClient):
    """
    A class that implements the CodeflixClient interface using HTTP requests.
    """

    def get_video(self, video_id: UUID) -> VideoResponse:
        """
        Retrieves a video by id.

        Args:
            video_id (UUID): The ID of the video to be retrieved.

        Returns:
            VideoResponse: The video response object containing the video details.
        """

        return VideoResponse(
            **{
                "id": video_id,
                "title": "The Godfather",
                "launch_year": 1972,
                "rating": "AGE_18",
                "is_active": True,
                "categories": [
                    {
                        "id": "142f2b4b-1b7b-4f3b-8eab-3f2f2b4b1b7b",
                        "name": "Action",
                        "description": "Action movies",
                    }
                ],
                "cast_members": [
                    {
                        "id": "242f2b4b-1b7b-4f3b-8eab-3f2f2b4b1b7b",
                        "name": "Marlon Brando",
                        "type": "ACTOR",
                    },
                    {
                        "id": "342f2b4b-1b7b-4f3b-8eab-3f2f2b4b1b7b",
                        "name": "Al Pacino",
                        "type": "DIRECTOR",
                    },
                ],
                "genres": [
                    {
                        "id": "442f2b4b-1b7b-4f3b-8eab-3f2f2b4b1b7b",
                        "name": "Drama",
                    }
                ],
                "banner": {
                    "name": "The Godfather",
                    "raw_location": "https://banner.com/the-godfather",
                },
            }
        )
