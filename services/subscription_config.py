"""
Subscription Plans Configuration
"""

SUBSCRIPTION_PLANS = {
    'basic': {
        'name': 'Basic',
        'price': 0,
        'features': {
            'document_management': True,
            'matter_management': True,
            'time_billing': True,
            'calendar': True,
            'case_comparison': False,  # Not available
            'ai_insights': False,
            'advanced_search': False,
            'business_intelligence': False,
        },
        'limits': {
            'max_users': 1,
            'max_documents': 100,
            'max_matters': 10,
            'case_comparison_per_month': 0,  # Not available
            'ai_insights_per_month': 0,
            'advanced_search_per_month': 0,
        }
    },
    'professional': {
        'name': 'Professional',
        'price': 99,
        'features': {
            'document_management': True,
            'matter_management': True,
            'time_billing': True,
            'calendar': True,
            'case_comparison': True,
            'ai_insights': True,
            'advanced_search': True,
            'business_intelligence': True,
        },
        'limits': {
            'max_users': 10,
            'max_documents': 1000,
            'max_matters': 100,
            'case_comparison_per_month': 50,
            'ai_insights_per_month': 100,
            'advanced_search_per_month': 200,
        }
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': 299,
        'features': {
            'document_management': True,
            'matter_management': True,
            'time_billing': True,
            'calendar': True,
            'case_comparison': True,
            'ai_insights': True,
            'advanced_search': True,
            'business_intelligence': True,
            'integrations': True,
            'api_access': True,
            'custom_workflows': True,
        },
        'limits': {
            'max_users': -1,  # Unlimited
            'max_documents': -1,  # Unlimited
            'max_matters': -1,  # Unlimited
            'case_comparison_per_month': -1,  # Unlimited
            'ai_insights_per_month': -1,  # Unlimited
            'advanced_search_per_month': -1,  # Unlimited
        }
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
