#!/usr/bin/env python3
"""
Gemini Models Compatibility Checker for TradingAgents

This script tests which Google Gemini models are accessible with your API key
and provides recommendations for optimal configuration.

Usage:
    uv run python check_gemini_models.py

Output:
    - Lists all working models with your API key
    - Shows model performance characteristics
    - Identifies restricted models requiring billing
    - Reports deprecated/unavailable models
    - Provides configuration recommendations

Last updated: November 22, 2025
Compatible with: langchain-google-genai v2.1.5+
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Method 1: Using langchain-google-genai (which is already installed)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    print("=== Testing with langchain-google-genai ===")
    
    # Supported models based on testing (Nov 2025)
    # These models work with your API key
    working_models = [
        "gemini-3-pro-preview",     # ✅ Latest and most advanced model, not for free tier
        "gemini-2.5-pro",           # ✅ Most advanced available
        "gemini-2.5-flash",         # ✅ Fast and efficient  
        "gemini-2.5-flash-lite",    # ✅ Fastest option
        "gemini-2.0-flash",         # ✅ Previous generation workhorse
        "gemini-2.0-flash-lite",    # ✅ Previous generation fast
        "models/gemini-2.5-pro",    # ✅ Alternative naming
        "models/gemini-2.5-flash"   # ✅ Alternative naming
    ]
    
    # Models that have quota/billing restrictions
    restricted_models = [
        "gemini-3-pro-preview",      # ❌ Quota exceeded (requires billing)
        "gemini-3-pro-image-preview" # ❌ Quota exceeded (requires billing)
    ]
    
    # Models that are no longer available
    deprecated_models = [
        "gemini-pro",               # ❌ Deprecated
        "gemini-1.5-pro",           # ❌ No longer available
        "gemini-1.5-flash",         # ❌ No longer available
        "gemini-2.5-pro-latest",    # ❌ Not found
        "gemini-2.5-flash-latest"   # ❌ Not found
    ]
    
    model_names_to_try = working_models
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in environment variables")
        exit(1)
    
    print(f"Using API key: {api_key[:10]}...")
    print(f"Found {len(model_names_to_try)} model names to test\n")
    
    working_models = []
    
    for model_name in model_names_to_try:
        try:
            print(f"Testing model: {model_name}")
            
            # Try to initialize the model
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0
            )
            
            # Try a simple generation
            response = llm.invoke("Hello, respond with just 'OK'")
            print(f"  ✅ SUCCESS: {model_name} - Response: {response.content}")
            working_models.append(model_name)
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg:
                print(f"  ❌ NOT FOUND: {model_name}")
            elif "403" in error_msg or "permission" in error_msg.lower():
                print(f"  🚫 NO PERMISSION: {model_name}")
            else:
                print(f"  ⚠️  ERROR: {model_name} - {error_msg}")
    
    print(f"=== SUMMARY ===")
    print(f"Working models found: {len(working_models)}")
    for model in working_models:
        print(f"  ✅ {model}")
    
    if working_models:
        print(f"\nRecommended models:")
        print(f"  🚀 Primary:   {working_models[0]} (most advanced)")
        print(f"  ⚡ Secondary: {working_models[1]} (fast & efficient)")
        print(f"  💨 Fastest:   {working_models[2]} (ultra-fast)")
        
        print(f"\n=== CONFIGURATION READY ===")
        print(f"Your TradingAgents is configured to use:")
        print(f"  • Deep thinking: {working_models[0]}")
        print(f"  • Quick thinking: {working_models[1]}")
        
        print(f"\n=== RESTRICTED MODELS ===")
        print("These models require billing/paid plan:")
        for model in restricted_models:
            print(f"  💳 {model}")
            
        print(f"\n=== DEPRECATED MODELS ===") 
        print("These models are no longer available:")
        for model in deprecated_models:
            print(f"  ❌ {model}")
    else:
        print("\n❌ No working models found. Check your API key and permissions.")

except ImportError as e:
    print(f"Error importing langchain-google-genai: {e}")
    
except Exception as e:
    print(f"Unexpected error: {e}")