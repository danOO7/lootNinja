"""
Redis utility functions for GiftScout.
Handles caching and session management for gift search workflows.
"""

import json
import os
from datetime import datetime, timedelta
import redis

# Initialize Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


def cache_search_results(session_id: str, results: dict, ttl: int = 3600) -> bool:
    """
    Cache gift search results in Redis.
    
    Args:
        session_id: Unique session identifier
        results: Dictionary containing search results
        ttl: Time to live in seconds (default: 1 hour)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cache_key = f"giftscount:results:{session_id}"
        redis_client.setex(
            cache_key,
            ttl,
            json.dumps(results)
        )
        return True
    except Exception as e:
        print(f"Cache error: {e}")
        return False


def get_cached_results(session_id: str) -> dict:
    """
    Retrieve cached search results from Redis.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        dict: Cached results or empty dict if not found
    """
    try:
        cache_key = f"giftscount:results:{session_id}"
        cached = redis_client.get(cache_key)
        return json.loads(cached) if cached else {}
    except Exception as e:
        print(f"Cache retrieval error: {e}")
        return {}


def save_user_preference(user_id: str, preferences: dict) -> bool:
    """
    Save user preferences for future gift searches.
    
    Args:
        user_id: Unique user identifier
        preferences: Dictionary with preference data
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        pref_key = f"giftscount:preferences:{user_id}"
        redis_client.set(pref_key, json.dumps(preferences))
        redis_client.expire(pref_key, 86400 * 30)  # 30 days
        return True
    except Exception as e:
        print(f"Preference save error: {e}")
        return False


def get_user_preference(user_id: str) -> dict:
    """
    Retrieve user preferences from Redis.
    
    Args:
        user_id: Unique user identifier
    
    Returns:
        dict: User preferences or empty dict if not found
    """
    try:
        pref_key = f"giftscount:preferences:{user_id}"
        prefs = redis_client.get(pref_key)
        return json.loads(prefs) if prefs else {}
    except Exception as e:
        print(f"Preference retrieval error: {e}")
        return {}


def track_search_history(user_id: str, search_data: dict) -> bool:
    """
    Track user search history in Redis.
    
    Args:
        user_id: Unique user identifier
        search_data: Dictionary with search details
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        history_key = f"giftscount:history:{user_id}"
        search_entry = {
            "timestamp": datetime.now().isoformat(),
            **search_data
        }
        redis_client.lpush(history_key, json.dumps(search_entry))
        redis_client.ltrim(history_key, 0, 99)  # Keep last 100 searches
        redis_client.expire(history_key, 86400 * 90)  # 90 days
        return True
    except Exception as e:
        print(f"History tracking error: {e}")
        return False


def get_search_history(user_id: str, limit: int = 10) -> list:
    """
    Retrieve user search history from Redis.
    
    Args:
        user_id: Unique user identifier
        limit: Number of recent searches to retrieve
    
    Returns:
        list: List of search history entries
    """
    try:
        history_key = f"giftscount:history:{user_id}"
        raw_history = redis_client.lrange(history_key, 0, limit - 1)
        return [json.loads(entry) for entry in raw_history]
    except Exception as e:
        print(f"History retrieval error: {e}")
        return []


def increment_search_counter(counter_name: str) -> int:
    """
    Increment a search counter for analytics.
    
    Args:
        counter_name: Name of the counter
    
    Returns:
        int: Updated counter value
    """
    try:
        counter_key = f"giftscount:counter:{counter_name}"
        return redis_client.incr(counter_key)
    except Exception as e:
        print(f"Counter error: {e}")
        return 0


def get_trending_searches() -> dict:
    """
    Get analytics on trending searches.
    
    Returns:
        dict: Dictionary with trending search statistics
    """
    try:
        pattern = "giftscount:counter:*"
        keys = redis_client.keys(pattern)
        trending = {}
        
        for key in keys:
            counter_name = key.replace("giftscount:counter:", "")
            count = redis_client.get(key)
            trending[counter_name] = int(count) if count else 0
        
        # Sort by count descending
        return dict(sorted(trending.items(), key=lambda x: x[1], reverse=True))
    except Exception as e:
        print(f"Trending searches error: {e}")
        return {}


def clear_session_data(session_id: str) -> bool:
    """
    Clear all data for a specific session.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        pattern = f"giftscount:*:{session_id}"
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        print(f"Session clear error: {e}")
        return False
