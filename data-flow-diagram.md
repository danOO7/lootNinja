    The following sequence illustrates the complete user journey from profile input to product recommendations:
PHASE 1: USER INPUT
→   User opens Loot Ninja web application
→   User describes gift recipient in chat interface
→   Profile includes: age, interests, budget, occasion
PHASE 2: PROFILE PROCESSING
→   CopilotKit agent parses natural language input
→   Extract structured data: demographics, interests, constraints
→   Generate profile hash for cache lookup
→   Check Redis for cached recommendations
PHASE 3: CACHE DECISION
•       If Cache HIT: Return stored recommendations immediately (skip to Phase 6)
•       If Cache MISS: Proceed to Phase 4 for fresh search
PHASE 4: TREND DISCOVERY
→   Initiate parallel Tavily searches
→   TikTok Search: "trending products tiktok [profile]"
→   Reddit Search: "site:reddit.com gifts [profile]"
→   Receive structured results with URLs and snippets
→   Extract product names from content
PHASE 5: RANKING & STORAGE
→   Merge products from TikTok and Reddit
→   Calculate relevance scores:
• TikTok mentions: 2.0 points
• Reddit mentions: 1.5 points
• Recency bonus: +0.5 points
• Profile match: +1.0 points
→   Sort by total score (highest first)
→   Filter by budget constraints
→   Generate Amazon search URLs
→   Store results in Redis (24-hour TTL)
PHASE 6: PRESENTATION
→   Format top 8-10 products for display
→   Include: product name, trending reason, Amazon link
→   Display in CopilotKit chat interface
→   Offer refinement options to user