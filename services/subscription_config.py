"""
Subscription Plans Configuration
"""

SUBSCRIPTION_PLANS = {
    "basic": {
        "name": "Basic Plan",
        "price": 49,
        "billing_cycle": "monthly",
        "description": "Essential legal practice management tools",
        "features": {
            # Core Features (Always Available)
            "document_management": True,
            "matter_management": True,
            "time_billing": True,
            "calendar_tasks": True,
            "client_portal": True,
            
            # AI Features (Not Available)
            "ai_insights": False,
            "case_comparison": False,
            "advanced_search": False,
            "business_intelligence": False,
            
            # Integrations
            "integrations": False,
            "mobile_app": False,
            "api_access": False,
        },
        "limits": {
            "max_matters": 50,
            "max_documents": 500,
            "max_users": 3,
            "storage_gb": 10,
            
            # AI Usage Limits (0 = Not Available)
            "ai_insights_per_month": 0,
            "case_comparisons_per_month": 0,
            "advanced_searches_per_month": 0,
        },
        "support": "Email support (48h response)"
    },
    
    "professional": {
        "name": "Professional Plan",
        "price": 149,
        "billing_cycle": "monthly",
        "description": "Advanced AI-powered legal analytics with usage limits",
        "features": {
            # Core Features (Always Available)
            "document_management": True,
            "matter_management": True,
            "time_billing": True,
            "calendar_tasks": True,
            "client_portal": True,
            
            # AI Features (Limited)
            "ai_insights": True,
            "case_comparison": True,
            "advanced_search": True,
            "business_intelligence": True,
            
            # Integrations
            "integrations": True,
            "mobile_app": True,
            "api_access": False,
        },
        "limits": {
            "max_matters": 200,
            "max_documents": 5000,
            "max_users": 10,
            "storage_gb": 100,
            
            # AI Usage Limits (Per Month)
            "ai_insights_per_month": 50,
            "case_comparisons_per_month": 25,
            "advanced_searches_per_month": 100,
        },
        "support": "Priority email + chat support (24h response)"
    },
    
    "enterprise": {
        "name": "Enterprise Plan",
        "price": 499,
        "billing_cycle": "monthly",
        "description": "Unlimited AI features and premium support",
        "features": {
            # Core Features (Always Available)
            "document_management": True,
            "matter_management": True,
            "time_billing": True,
            "calendar_tasks": True,
            "client_portal": True,
            
            # AI Features (Unlimited)
            "ai_insights": True,
            "case_comparison": True,
            "advanced_search": True,
            "business_intelligence": True,
            
            # Integrations
            "integrations": True,
            "mobile_app": True,
            "api_access": True,
            "white_label": True,
            "custom_integrations": True,
        },
        "limits": {
            "max_matters": -1,  # -1 = Unlimited
            "max_documents": -1,
            "max_users": -1,
            "storage_gb": -1,
            
            # AI Usage Limits (-1 = Unlimited)
            "ai_insights_per_month": -1,
            "case_comparisons_per_month": -1,
            "advanced_searches_per_month": -1,
        },
        "support": "24/7 phone + email + chat support + dedicated account manager"
    }
}

# Feature display names and icons
FEATURE_DISPLAY = {
    "document_management": {"name": "Document Management", "icon": "📁"},
    "matter_management": {"name": "Matter Management", "icon": "⚖️"},
    "time_billing": {"name": "Time & Billing", "icon": "💰"},
    "calendar_tasks": {"name": "Calendar & Tasks", "icon": "📅"},
    "client_portal": {"name": "Client Portal", "icon": "👥"},
    "ai_insights": {"name": "AI Insights", "icon": "🤖"},
    "case_comparison": {"name": "Case Comparison", "icon": "🔍"},
    "advanced_search": {"name": "Advanced Search", "icon": "🔎"},
    "business_intelligence": {"name": "Business Intelligence", "icon": "📊"},
    "integrations": {"name": "Integrations", "icon": "🔗"},
    "mobile_app": {"name": "Mobile App", "icon": "📱"},
    "api_access": {"name": "API Access", "icon": "🔌"},
}
