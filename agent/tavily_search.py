"""
Tavily search integration for GiftScout.
Handles real-time web searches for products and social trends.
"""

import os
import json
from typing import Optional, List, Dict, Any
from tavily import TavilyClient


class TavilySearchEngine:
    """Tavily search engine wrapper for GiftScout."""
    
    def __init__(self):
        """Initialize Tavily client with API key from environment."""
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))
        self.search_history = []
    
    def search_social_trends(self, persona: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search for trending gift ideas on social media platforms.
        
        Args:
            persona: Description of gift recipient (e.g., "20-year-old gaming enthusiast")
            max_results: Maximum number of results to return
        
        Returns:
            Dictionary containing trending topics and discussions
        """
        try:
            search_query = f"best gift ideas {persona} trending 2024 reddit tiktok youtube"
            response = self.client.search(
                query=search_query,
                max_results=max_results,
                include_answer=True
            )
            
            trends = self._parse_search_results(response)
            self.search_history.append({
                "type": "social_trends",
                "query": search_query,
                "results_count": len(trends)
            })
            
            return {
                "success": True,
                "trends": trends,
                "query": search_query
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_products(self, item_description: str, budget: float, 
                       max_results: int = 8) -> Dict[str, Any]:
        """
        Search for products matching description and budget.
        
        Args:
            item_description: Description of what to search for
            budget: Maximum price in USD
            max_results: Maximum number of results to return
        
        Returns:
            Dictionary containing product listings with prices and links
        """
        try:
            search_query = f"{item_description} buy online under ${budget}"
            response = self.client.search(
                query=search_query,
                max_results=max_results,
                include_answer=True
            )
            
            products = self._parse_product_results(response, budget)
            self.search_history.append({
                "type": "product_search",
                "query": search_query,
                "budget": budget,
                "results_count": len(products)
            })
            
            return {
                "success": True,
                "products": products,
                "query": search_query,
                "budget": budget
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_store_specific(self, product: str, store: str, 
                             max_results: int = 5) -> Dict[str, Any]:
        """
        Search for products on specific stores (Amazon, Etsy, etc.).
        
        Args:
            product: Product name to search for
            store: Store name (amazon, etsy, walmart, target, etc.)
            max_results: Maximum number of results
        
        Returns:
            Dictionary containing store-specific product listings
        """
        try:
            search_query = f"{product} site:{store}.com"
            response = self.client.search(
                query=search_query,
                max_results=max_results,
                include_answer=True
            )
            
            products = self._parse_search_results(response)
            
            return {
                "success": True,
                "store": store,
                "products": products,
                "query": search_query
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_personalized_gifts(self, interests: List[str], age_range: str, 
                                 budget: float, gender: Optional[str] = None) -> Dict[str, Any]:
        """
        Comprehensive search for personalized gift recommendations.
        
        Args:
            interests: List of interests (e.g., ["gaming", "reading", "photography"])
            age_range: Age range (e.g., "20-25" or "teen")
            budget: Maximum price in USD
            gender: Optional gender preference
        
        Returns:
            Dictionary with curated gift suggestions
        """
        try:
            interests_str = ", ".join(interests)
            persona_desc = f"{age_range} {gender if gender else 'person'} interested in {interests_str}"
            
            search_query = f"gift ideas for {persona_desc} budget ${budget}"
            response = self.client.search(
                query=search_query,
                max_results=10,
                include_answer=True
            )
            
            products = self._parse_product_results(response, budget)
            
            # Score products based on relevance to interests
            scored_products = self._score_by_relevance(products, interests)
            
            return {
                "success": True,
                "persona": persona_desc,
                "budget": budget,
                "products": scored_products[:5],
                "summary": response.get("answer", "")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_search_results(self, response: Dict) -> List[Dict[str, str]]:
        """Parse Tavily search response into standardized format."""
        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "source": item.get("source", ""),
                "snippet": item.get("content", "")[:300],
                "score": item.get("score", 0)
            })
        return results
    
    def _parse_product_results(self, response: Dict, budget: float) -> List[Dict[str, Any]]:
        """Parse search results looking for product information."""
        products = []
        for item in response.get("results", []):
            product = {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "source": item.get("source", ""),
                "snippet": item.get("content", "")[:300],
                "score": item.get("score", 0)
            }
            products.append(product)
        return products
    
    def _score_by_relevance(self, products: List[Dict], interests: List[str]) -> List[Dict]:
        """Score products based on relevance to user interests."""
        scored = []
        interests_lower = [i.lower() for i in interests]
        
        for product in products:
            title_lower = product["title"].lower()
            snippet_lower = product["snippet"].lower()
            
            relevance_score = product.get("score", 0)
            
            # Boost score if interests mentioned
            for interest in interests_lower:
                if interest in title_lower:
                    relevance_score += 2
                if interest in snippet_lower:
                    relevance_score += 1
            
            product["relevance_score"] = relevance_score
            scored.append(product)
        
        # Sort by relevance
        return sorted(scored, key=lambda x: x["relevance_score"], reverse=True)
    
    def get_search_summary(self) -> Dict[str, Any]:
        """Get summary of recent searches."""
        return {
            "total_searches": len(self.search_history),
            "recent": self.search_history[-5:] if self.search_history else []
        }


# Create singleton instance
search_engine = TavilySearchEngine()


def search_gifts(persona: str, budget: float, interests: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Convenience function to search for gifts using all available data.
    
    Args:
        persona: Description of gift recipient
        budget: Maximum budget
        interests: Optional list of interests
    
    Returns:
        Dictionary with comprehensive gift recommendations
    """
    if interests:
        age_range = persona.split()[0] if persona else "adult"
        return search_engine.search_personalized_gifts(
            interests=interests,
            age_range=age_range,
            budget=budget
        )
    else:
        return search_engine.search_products(f"gift for {persona}", budget)
