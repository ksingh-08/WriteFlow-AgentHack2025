#!/usr/bin/env python3
"""WriteFlow Demo Script

This script demonstrates the key features of WriteFlow,
showing how it enhances human writing with AI assistance.
"""

import asyncio
from writeflow_mcp_config import WriteFlowMCPServer


async def demo_research_tool():
    """Demonstrate the research tool."""
    print("🔍 **Research Tool Demo**")
    print("=" * 50)
    
    server = WriteFlowMCPServer()
    
    # Research request
    research_params = {
        "topic": "AI in Healthcare",
        "context": "Research for a blog post about current AI applications in healthcare",
        "questions": [
            "What are the latest AI developments in healthcare?",
            "What are the main challenges and opportunities?",
            "How is AI improving patient outcomes?"
        ]
    }
    
    print(f"📝 Research Request:")
    print(f"   Topic: {research_params['topic']}")
    print(f"   Context: {research_params['context']}")
    print(f"   Questions: {len(research_params['questions'])} questions")
    
    # Execute research
    result = await server.handle_tool_call("research_tool", research_params)
    
    if result.get("success"):
        research_data = result["result"]
        print(f"\n✅ Research Completed!")
        print(f"   Findings: {len(research_data['findings'])} key insights")
        print(f"   Sources: {len(research_data['sources'])} references")
        print(f"   Suggestions: {len(research_data['suggestions'])} recommendations")
        
        print(f"\n📊 Sample Findings:")
        for i, finding in enumerate(research_data['findings'][:2], 1):
            print(f"   {i}. {finding}")
    else:
        print(f"❌ Research failed: {result.get('error')}")


async def demo_outline_tool():
    """Demonstrate the outline tool."""
    print("\n📋 **Outline Tool Demo**")
    print("=" * 50)
    
    server = WriteFlowMCPServer()
    
    # Outline request
    outline_params = {
        "topic": "AI in Healthcare",
        "content_type": "Blog Post",
        "key_points": [
            "Current AI applications in healthcare",
            "Benefits and improvements to patient care",
            "Challenges and ethical considerations",
            "Future outlook and predictions"
        ]
    }
    
    print(f"📝 Outline Request:")
    print(f"   Topic: {outline_params['topic']}")
    print(f"   Type: {outline_params['content_type']}")
    print(f"   Key Points: {len(outline_params['key_points'])} main areas")
    
    # Execute outline generation
    result = await server.handle_tool_call("outline_tool", outline_params)
    
    if result.get("success"):
        outline_data = result["result"]
        print(f"\n✅ Outline Generated!")
        print(f"   Structure: {len(outline_data['structure'])} main sections")
        print(f"   Writing Prompts: {len(outline_data['writing_prompts'])} suggestions")
        
        print(f"\n🏗️  Content Structure:")
        for section in outline_data['structure']:
            print(f"   📍 {section['section']}")
            print(f"      Subsections: {', '.join(section['subsections'])}")
            print(f"      Key Elements: {', '.join(section['key_elements'])}")
            print()
    else:
        print(f"❌ Outline generation failed: {result.get('error')}")


async def demo_writing_assistant():
    """Demonstrate the writing assistant tool."""
    print("\n✍️ **Writing Assistant Demo**")
    print("=" * 50)
    
    server = WriteFlowMCPServer()
    
    # Sample content for analysis
    sample_content = """
    Artificial Intelligence is transforming healthcare in remarkable ways. 
    From diagnostic imaging to drug discovery, AI systems are helping 
    medical professionals make better decisions and improve patient outcomes. 
    However, there are also challenges that need to be addressed.
    """
    
    # Writing assistance request
    writing_params = {
        "content": sample_content,
        "suggestion_type": "comprehensive",
        "context": "Blog post about AI in healthcare"
    }
    
    print(f"📝 Writing Assistance Request:")
    print(f"   Content Length: {len(sample_content)} characters")
    print(f"   Suggestion Type: {writing_params['suggestion_type']}")
    print(f"   Context: {writing_params['context']}")
    
    # Execute writing assistance
    result = await server.handle_tool_call("writing_assistant_tool", writing_params)
    
    if result.get("success"):
        writing_data = result["result"]
        print(f"\n✅ Writing Suggestions Generated!")
        print(f"   Suggestions: {len(writing_data['suggestions'])} improvements")
        
        print(f"\n💡 Writing Suggestions:")
        for suggestion in writing_data['suggestions']:
            print(f"   📌 {suggestion['type'].title()}: {suggestion['content']}")
            print(f"      Reasoning: {suggestion['reasoning']}")
            print(f"      Confidence: {suggestion['confidence']:.2f}")
            print()
    else:
        print(f"❌ Writing assistance failed: {result.get('error')}")


async def demo_bookmark_tool():
    """Demonstrate the bookmark tool."""
    print("\n📚 **Bookmark Tool Demo**")
    print("=" * 50)
    
    server = WriteFlowMCPServer()
    
    # Bookmark creation
    bookmark_params = {
        "title": "AI in Healthcare: Current State and Future Prospects",
        "url": "https://example.com/ai-healthcare-report",
        "notes": "Comprehensive report on AI applications in healthcare, including case studies and future predictions",
        "tags": ["AI", "Healthcare", "Technology", "Research"]
    }
    
    print(f"📝 Bookmark Creation:")
    print(f"   Title: {bookmark_params['title']}")
    print(f"   URL: {bookmark_params['url']}")
    print(f"   Tags: {', '.join(bookmark_params['tags'])}")
    
    # Execute bookmark creation
    result = await server.handle_tool_call("bookmark_tool", bookmark_params)
    
    if result.get("success"):
        bookmark_data = result["result"]
        print(f"\n✅ Bookmark Created!")
        print(f"   Title: {bookmark_data['title']}")
        print(f"   Status: {bookmark_data['status']}")
        print(f"   Created: {bookmark_data['created_at']}")
        print(f"   Tags: {', '.join(bookmark_data['tags'])}")
    else:
        print(f"❌ Bookmark creation failed: {result.get('error')}")


async def demo_thread_tool():
    """Demonstrate the thread tool."""
    print("\n🧵 **Thread Tool Demo**")
    print("=" * 50)
    
    server = WriteFlowMCPServer()
    
    # Thread creation
    thread_params = {
        "title": "Discussion: AI Ethics in Healthcare",
        "content": "Let's discuss the ethical considerations of using AI in healthcare. What are the main concerns and how can we address them?",
        "tags": ["AI Ethics", "Healthcare", "Discussion", "Ethics"]
    }
    
    print(f"📝 Thread Creation:")
    print(f"   Title: {thread_params['title']}")
    print(f"   Content: {thread_params['content'][:50]}...")
    print(f"   Tags: {', '.join(thread_params['tags'])}")
    
    # Execute thread creation
    result = await server.handle_tool_call("thread_tool", thread_params)
    
    if result.get("success"):
        thread_data = result["result"]
        print(f"\n✅ Thread Created!")
        print(f"   Title: {thread_data['title']}")
        print(f"   Status: {thread_data['status']}")
        print(f"   Created: {thread_data['created_at']}")
        print(f"   Responses: {len(thread_data['responses'])}")
    else:
        print(f"❌ Thread creation failed: {result.get('error')}")


async def main():
    """Run the WriteFlow demo."""
    print("✍️ **WriteFlow Demo - Human-Centered Writing Enhanced by AI**")
    print("=" * 70)
    print("This demo showcases how WriteFlow uses AI as an intelligent assistant")
    print("for research, organization, and drafting while preserving human creativity.")
    print()
    
    # Run all demos
    await demo_research_tool()
    await demo_outline_tool()
    await demo_writing_assistant()
    await demo_bookmark_tool()
    await demo_thread_tool()
    
    print("\n🎉 **Demo Complete!**")
    print("=" * 50)
    print("WriteFlow demonstrates the power of human-AI collaboration:")
    print("✅ AI assists with research and organization")
    print("✅ AI provides structure and suggestions")
    print("✅ Humans maintain creative control")
    print("✅ Collaborative workflow enhances productivity")
    print()
    print("🚀 Ready to try WriteFlow? Run: streamlit run writeflow_app.py")


if __name__ == "__main__":
    asyncio.run(main())
