"""
API client for the Cartouche C# REST API.
Handles communication with the main C# backend.
"""

import aiohttp
import json
from typing import Dict, List, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.settings import SOCIAL_NETWORK_URL, API_KEY
from app.core.exceptions import APIError

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


class CartoucheAPIClient:
    """Client for interacting with the Cartouche C# REST API."""

    def __init__(self, base_url: str = SOCIAL_NETWORK_URL, token: str = API_KEY):
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API
            token: API token for authentication
        """
        self.base_url = base_url
        self.token = token
        self.session = None

    async def __aenter__(self):
        """Create session when entering context."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session when exiting context."""
        if self.session:
            await self.session.close()
            self.session = None

    def _get_auth_params(self) -> Dict[str, str]:
        """Get authentication parameters for requests."""
        return {"token": self.token}

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_posts(
        self, post_id: Optional[int] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Get posts from the API.

        Args:
            post_id: Optional post ID to get a specific post
            limit: Limit for number of posts when getting all posts (default: 25)

        Returns:
            List of post dictionaries
        """
        if post_id:
            # Get specific post
            endpoint = f"api/posts/{post_id}"
            url = f"{self.base_url.rstrip('/')}/{endpoint}"
        else:
            # Get all posts with caching and limit
            endpoint = "api/posts"
            url = f"{self.base_url.rstrip('/')}/{endpoint}?limit={limit}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.get(url, headers=headers) as response:
                response_text = await response.text()
                if response.status == 200:
                    try:
                        data = json.loads(response_text)
                        return data if isinstance(data, list) else [data]
                    except Exception as e:
                        logger.error(
                            f"[API][GET_POSTS] JSON decode error: {e}, Raw: {response_text}"
                        )
                        raise APIError(f"Failed to decode JSON: {response_text}")
                else:
                    logger.error(
                        f"[API][GET_POSTS] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to get posts: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in get_posts: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_comments(self, post_id: int) -> List[Dict[str, Any]]:
        """
        Get comments for a specific post.

        Args:
            post_id: ID of the post to get comments for

        Returns:
            List of comment dictionaries
        """
        endpoint = f"api/posts/{post_id}/comments/"
        url = f"{self.base_url.rstrip('/')}/{endpoint}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.get(url, headers=headers) as response:
                response_text = await response.text()
                if response.status == 200:
                    try:
                        data = json.loads(response_text)
                        return data if isinstance(data, list) else [data]
                    except Exception as e:
                        logger.error(
                            f"[API][GET_COMMENTS] JSON decode error: {e}, Raw: {response_text}"
                        )
                        raise APIError(f"Failed to decode JSON: {response_text}")
                else:
                    logger.error(
                        f"[API][GET_COMMENTS] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to get comments: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in get_comments: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    async def add_bot(self, bot_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new bot to the system.

        Args:
            bot_data: Bot data dictionary

        Returns:
            Response data
        """
        endpoint = "api/users/"
        url = f"{self.base_url.rstrip('/')}/{endpoint}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.post(
                url, json=bot_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status in (200, 201):
                    return await response.json()
                else:
                    logger.error(
                        f"[API][ADD_BOT] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to add bot: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in add_bot: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    async def add_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new profile to the system (Django API).

        Args:
            profile_data: Profile data dictionary

        Returns:
            Response data
        """
        endpoint = "api/profiles/"
        url = f"{self.base_url.rstrip('/')}/{endpoint}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.post(
                url, json=profile_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status in (200, 201):
                    return await response.json()
                else:
                    logger.error(
                        f"[API][ADD_PROFILE] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to add profile: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in add_profile: {str(e)}")
            raise APIError(f"API client error: {str(e)}")
        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    async def add_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new post to the system.

        Args:
            post_data: Post data dictionary

        Returns:
            Response data
        """
        endpoint = "api/posts/"
        url = f"{self.base_url.rstrip('/')}/{endpoint}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.post(
                url, json=post_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status in (200, 201):
                    try:
                        return await response.json()
                    except Exception as e:
                        logger.error(
                            f"[API][ADD_POST] JSON decode error: {e}, Raw: {response_text}"
                        )
                        raise APIError(f"Failed to decode JSON: {response_text}")
                else:
                    logger.error(
                        f"[API][ADD_POST] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to add post: {response_text}", response.status
                    )
        except Exception as e:
            logger.error(f"Error in add_post: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    async def like_post(self, post_id: int, user_id: int) -> Dict[str, Any]:
        """
        Like a post.

        Args:
            post_id: Post ID
            user_id: User ID

        Returns:
            Response status
        """
        endpoint = f"api/posts/{post_id}/like/"
        url = f"{self.base_url.rstrip('/')}/{endpoint}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.post(
                url, json={"user_id": user_id}, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status in (200, 201):
                    return await response.json()
                else:
                    logger.error(
                        f"[API][LIKE_POST] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to like post: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in like_post: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    async def add_comment(
        self, post_id: int, comment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a comment to a post.

        Args:
            post_id: Post ID
            comment_data: Comment data dictionary with keys: Name, FullName, Avatar, Text, OnDate

        Returns:
            Response data
        """
        endpoint = f"api/posts/{post_id}/comments/"
        url = f"{self.base_url.rstrip('/')}/{endpoint}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.post(
                url, json=comment_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status in (200, 201):
                    return await response.json()
                else:
                    logger.error(
                        f"[API][ADD_COMMENT] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to add comment: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in add_comment: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    async def follow_user(self, user_id: int, bot_id: int) -> Dict[str, Any]:
        """
        Subscribe (follow) a user as a bot.

        Args:
            user_id: ID of the user to follow
            bot_id: ID of the bot who follows

        Returns:
            Response data
        """
        # Build the endpoint and query
        endpoint = f"api/users/{user_id}/follow/"
        url = f"{self.base_url.rstrip('/')}/{endpoint}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.post(
                url, json={"follower_id": bot_id}, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status in (200, 201):
                    return await response.json()
                else:
                    logger.error(
                        f"[API][FOLLOW_USER] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to follow user: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in follow_user: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None


