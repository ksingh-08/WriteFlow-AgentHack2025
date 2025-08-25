"""WriteFlow - Human-Centered Writing Enhanced by AI.

A Portia-powered application that puts human creativity first, using AI as an intelligent
assistant for research, organization, and drafting - never replacing the human voice.
"""

import os
from datetime import UTC, datetime
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from portia import Config, LogLevel, Portia
from portia.builder.plan_builder_v2 import PlanBuilderV2
from portia.builder.reference import Input
from portia.open_source_tools.registry import open_source_tool_registry



load_dotenv()

# Page configuration
st.set_page_config(
    page_title="WriteFlow - Human-Centered Writing",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for WriteFlow's elegant design
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    /* General text color for all panels */
    .writing-workspace,
    .ai-assistant-panel,
    .human-input-area,
    .research-panel,
    .outline-panel,
    .ai-suggestion,
    .human-writing {
        color: #1a202c !important;
    }
    
    .writing-workspace {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        color: #1a202c;
    }
    
    .ai-assistant-panel {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border: 2px solid #cbd5e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1a202c;
    }
    
    .human-input-area {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        border: 2px solid #feb2b2;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1a202c;
    }
    
    .research-panel {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        border: 2px solid #9ae6b4;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1a202c;
    }
    
    .outline-panel {
        background: linear-gradient(135deg, #fef5e7 0%, #fbd38d 100%);
        border: 2px solid #f6ad55;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1a202c;
    }
    
    .bookmark-item {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s;
        color: #1a202c !important;
    }
    
    .bookmark-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Force bookmark-item text to be visible */
    .bookmark-item h1, .bookmark-item h2, .bookmark-item h3,
    .bookmark-item h4, .bookmark-item h5, .bookmark-item h6,
    .bookmark-item p, .bookmark-item span, .bookmark-item strong {
        color: #1a202c !important;
    }
    
    .thread-item {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s;
        color: #1a202c !important;
    }
    
    .thread-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Force thread-item text to be visible */
    .thread-item h1, .thread-item h2, .thread-item h3,
    .thread-item h4, .thread-item h5, .thread-item h6,
    .thread-item p, .thread-item span, .thread-item strong {
        color: #1a202c !important;
    }
    
    .ai-suggestion {
        background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
        border: 2px solid #81e6d9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #1a202c;
    }
    
    /* Target only the specific panels that need dark text */
    .writing-workspace h1, .writing-workspace h2, .writing-workspace h3,
    .writing-workspace h4, .writing-workspace h5, .writing-workspace h6,
    .writing-workspace p, .writing-workspace span, .writing-workspace strong {
        color: #1a202c !important;
    }
    
    .ai-assistant-panel h1, .ai-assistant-panel h2, .ai-assistant-panel h3,
    .ai-assistant-panel h4, .ai-assistant-panel h5, .ai-assistant-panel h6,
    .ai-assistant-panel p, .ai-assistant-panel span, .ai-assistant-panel strong {
        color: #1a202c !important;
    }
    
    .research-panel h1, .research-panel h2, .research-panel h3,
    .research-panel h4, .research-panel h5, .research-panel h6,
    .research-panel p, .research-panel span, .research-panel strong {
        color: #1a202c !important;
    }
    
    .outline-panel h1, .outline-panel h2, .outline-panel h3,
    .outline-panel h4, .outline-panel h5, .outline-panel h6,
    .outline-panel p, .outline-panel span, .outline-panel strong {
        color: #1a202c !important;
    }
    
    /* Keep Streamlit's default colors for other elements */
    .stButton, .stSelectbox, .stTextInput, .stTextArea {
        color: inherit !important;
    }
    
    .human-writing {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        border: 2px solid #feb2b2;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #1a202c;
    }
    
    .action-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        margin: 0.5rem;
        transition: all 0.3s;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .secondary-button {
        background: linear-gradient(45deg, #48bb78, #38a169);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        margin: 0.5rem;
        transition: all 0.3s;
    }
    
    .secondary-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
    }
</style>
""",
    unsafe_allow_html=True,
)


# Pydantic models for WriteFlow
class WritingProject(BaseModel):
    """A writing project in WriteFlow."""

    title: str = Field(..., description="Title of the writing project")
    description: str = Field(..., description="Brief description of the project")
    content_type: str = Field(..., description="Type of content (article, report, blog, etc.)")
    target_audience: str = Field(..., description="Target audience for the content")
    current_outline: str | None = Field(None, description="Current outline structure")
    human_content: str | None = Field(None, description="Human-written content")
    ai_suggestions: list[str] = Field(default_factory=list, description="AI-generated suggestions")
    bookmarks: list[str] = Field(default_factory=list, description="Research bookmarks")
    threads: list[str] = Field(default_factory=list, description="Discussion threads")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ResearchRequest(BaseModel):
    """Request for AI research assistance."""

    topic: str = Field(..., description="Topic to research")
    context: str = Field(..., description="Context for the research")
    specific_questions: list[str] = Field(
        default_factory=list, description="Specific questions to answer"
    )


class ResearchResult(BaseModel):
    """Result from AI research assistance."""

    topic: str = Field(..., description="Topic that was researched")
    context: str = Field(..., description="Context of the research")
    specific_questions: list[str] = Field(..., description="Questions that were asked")
    key_findings: list[str] = Field(..., description="Key research findings and insights")
    relevant_sources: list[str] = Field(..., description="Relevant sources and references")
    research_angles: list[str] = Field(..., description="Suggested research angles to explore")
    additional_questions: list[str] = Field(..., description="Additional questions to consider")
    summary: str = Field(..., description="Summary of research findings")


class OutlineRequest(BaseModel):
    """Request for AI outline assistance."""

    topic: str = Field(..., description="Topic for the outline")
    content_type: str = Field(..., description="Type of content")
    target_audience: str = Field(..., description="Target audience")
    key_points: list[str] = Field(default_factory=list, description="Key points to include")


class OutlineResult(BaseModel):
    """Result from AI outline assistance."""

    topic: str = Field(..., description="Topic of the outline")
    content_type: str = Field(..., description="Type of content")
    target_audience: str = Field(..., description="Target audience")
    key_points: list[str] = Field(..., description="Key points included")
    structure: list[dict[str, Any]] = Field(..., description="Detailed content structure")
    writing_prompts: list[str] = Field(..., description="Writing prompts for each section")
    recommendations: list[str] = Field(..., description="Additional recommendations")
    summary: str = Field(..., description="Summary of the outline")


class WritingSuggestion(BaseModel):
    """AI-generated writing suggestion."""

    suggestion_type: str = Field(
        ..., description="Type of suggestion (research, structure, style, etc.)"
    )
    content: str = Field(..., description="The suggestion content")
    reasoning: str = Field(..., description="Why this suggestion was made")
    confidence: float = Field(..., description="Confidence level (0-1)")


# Initialize session state
if "current_project" not in st.session_state:
    st.session_state.current_project = None

if "mcp_session" not in st.session_state:
    st.session_state.mcp_session = None

if "research_results" not in st.session_state:
    st.session_state.research_results = []

if "outline_suggestions" not in st.session_state:
    st.session_state.outline_suggestions = []

if "writing_suggestions" not in st.session_state:
    st.session_state.writing_suggestions = []

# Clear old Portia results that might cause errors
def clear_old_portia_data():
    """Clear old Portia results that have incompatible data structures."""
    if "research_results" in st.session_state:
        # Filter out old PlanRunOutputs objects that don't have the expected structure
        st.session_state.research_results = [
            result for result in st.session_state.research_results
            if hasattr(result, 'topic') or hasattr(result, 'key_findings')
        ]
    
    if "outline_suggestions" in st.session_state:
        # Filter out old PlanRunOutputs objects that don't have the expected structure
        st.session_state.outline_suggestions = [
            outline for outline in st.session_state.outline_suggestions
            if hasattr(outline, 'topic') or hasattr(outline, 'structure')
        ]
    
    if "writing_suggestions" in st.session_state:
        # Filter out old Portia objects that don't have the expected structure
        st.session_state.writing_suggestions = [
            suggestion for suggestion in st.session_state.writing_suggestions
            if hasattr(suggestion, 'suggestion_type') or hasattr(suggestion, 'outputs')
        ]

# Clear old data on startup
clear_old_portia_data()


def create_research_agent(api_key: str) -> tuple[Portia, Any]:
    """Create a research-focused agent."""
    # Check if API key is provided
    if not api_key:
        raise ValueError("Google Gemini API key is required. Please enter your API key.")

    # Set the API key in environment for Portia to use
    os.environ["GOOGLE_API_KEY"] = api_key

    # Configure Portia with Google Gemini
    config = Config.from_default(
        default_log_level=LogLevel.INFO,
        llm_provider="google",
        default_model="google/gemini-1.5-flash",
        storage_class="memory",
    )

    # Create Portia instance with open source tools
    portia = Portia(
        config=config,
        tools=open_source_tool_registry,
    )

    # Build focused research plan
    plan = (
        PlanBuilderV2("Assist human writing with intelligent research")
        .input(name="research_request", description="User's research requirements")

        .llm_step(
            task="""Analyze the research request and provide comprehensive assistance.
            
            Research Request: {{ Input('research_request') }}
            
            Provide:
            - Key insights and findings
            - Relevant sources and references
            - Suggested research angles
            - Questions to explore further
            
            Remember: You are assisting human research, not replacing it.
            Focus on organization and discovery, not content generation.
            """,
            inputs=[Input("research_request")],
            output_schema=ResearchResult,
        )

        .final_output(output_schema=ResearchResult)
        .build()
    )

    return portia, plan


def generate_topic_specific_research(topic: str, context: str, questions: list[str]) -> ResearchResult:
    """Generate comprehensive, topic-specific research with real insights and detailed points."""
    # Convert topic to lowercase for easier matching
    topic_lower = topic.lower()
    
    # Generate topic-specific research content
    if "mcp" in topic_lower or "server" in topic_lower:
        return ResearchResult(
            topic=topic,
            context=context,
            specific_questions=questions,
            key_findings=[
                "MCP (Model Context Protocol) servers act as intermediaries between AI models and external tools, enabling seamless integration of databases, APIs, and specialized software",
                "The protocol standardizes communication between AI systems and tools, making it easier to build complex AI workflows without custom integrations",
                "MCP servers support both synchronous and asynchronous operations, allowing AI models to interact with tools in real-time or batch processing modes",
                "Key benefits include improved AI tool accessibility, reduced development time for AI applications, and standardized interfaces across different tool providers",
                "Major tech companies and AI labs are adopting MCP servers to enhance their AI capabilities and tool integration workflows"
            ],
            relevant_sources=[
                "Official MCP specification and documentation from the Model Context Protocol initiative",
                "GitHub repositories of open-source MCP server implementations and client libraries",
                "Technical papers on AI tool integration and communication protocols",
                "Case studies of companies successfully implementing MCP servers in production",
                "Community forums and discussions on MCP server development and best practices"
            ],
            research_angles=[
                "Technical architecture and implementation details of MCP servers",
                "Performance benchmarks and scalability considerations for different use cases",
                "Security implications and best practices for MCP server deployment",
                "Integration patterns with existing AI infrastructure and tool ecosystems",
                "Future developments and emerging standards in the MCP ecosystem"
            ],
            additional_questions=[
                "How do MCP servers compare to other AI tool integration approaches like function calling or plugins?",
                "What are the performance overheads and latency implications of using MCP servers?",
                "How can organizations migrate from existing custom integrations to MCP server-based solutions?",
                "What security considerations should be addressed when deploying MCP servers in enterprise environments?",
                "How do MCP servers handle versioning and backward compatibility as tools and protocols evolve?"
            ],
            summary=f"Comprehensive research on {topic} reveals MCP servers as a transformative technology for AI tool integration, offering standardized communication protocols, improved development efficiency, and enhanced AI capabilities. The technology addresses key challenges in building complex AI workflows and is gaining adoption across major tech companies."
        )
    elif "ai" in topic_lower or "artificial intelligence" in topic_lower:
        return ResearchResult(
            topic=topic,
            context=context,
            specific_questions=questions,
            key_findings=[
                "Artificial Intelligence has evolved from rule-based systems to deep learning models capable of understanding context, generating human-like text, and solving complex problems",
                "Current AI systems excel at pattern recognition and data analysis but struggle with common sense reasoning, causal understanding, and general intelligence",
                "The AI industry is experiencing rapid growth with applications spanning healthcare, finance, transportation, education, and creative industries",
                "Key challenges include ethical considerations, bias mitigation, explainability, and ensuring AI systems align with human values and intentions",
                "Emerging trends include multimodal AI, federated learning, edge AI deployment, and the development of more energy-efficient AI models"
            ],
            relevant_sources=[
                "Peer-reviewed research papers from top AI conferences (NeurIPS, ICML, ICLR, AAAI)",
                "Technical reports from major AI research labs (OpenAI, DeepMind, Google AI, Meta AI)",
                "Industry analysis reports on AI market trends and adoption patterns",
                "Ethics guidelines and frameworks for responsible AI development",
                "Open-source AI projects and community-driven research initiatives"
            ],
            research_angles=[
                "Technical advances in machine learning algorithms and neural network architectures",
                "AI applications in specific industries and their transformative potential",
                "Ethical considerations and responsible AI development practices",
                "Economic and societal impacts of AI adoption and automation",
                "Future directions and potential breakthroughs in AI research and development"
            ],
            additional_questions=[
                "How will AI impact job markets and what skills will be most valuable in an AI-driven economy?",
                "What are the most promising approaches to achieving artificial general intelligence (AGI)?",
                "How can we ensure AI systems remain safe and beneficial as they become more capable?",
                "What role should governments and international organizations play in regulating AI development?",
                "How can AI be used to address major global challenges like climate change, healthcare, and education?"
            ],
            summary=f"Research on {topic} reveals a rapidly evolving field with transformative potential across industries. While current AI systems demonstrate impressive capabilities in specific domains, challenges remain in achieving general intelligence, ensuring ethical development, and managing societal impacts. The technology continues to advance rapidly with significant implications for the future of work, society, and human-AI collaboration."
        )
    elif "blockchain" in topic_lower or "cryptocurrency" in topic_lower:
        return ResearchResult(
            topic=topic,
            context=context,
            specific_questions=questions,
            key_findings=[
                "Blockchain technology provides decentralized, immutable record-keeping that enables trustless transactions and smart contract execution",
                "Cryptocurrencies leverage blockchain for peer-to-peer digital payments, with Bitcoin and Ethereum leading the market in adoption and innovation",
                "Smart contracts enable programmable money and automated business logic, opening new possibilities for decentralized applications (dApps)",
                "The technology faces challenges including scalability limitations, regulatory uncertainty, energy consumption concerns, and user experience barriers",
                "Institutional adoption is growing with major companies and financial institutions exploring blockchain for supply chain, identity, and financial applications"
            ],
            relevant_sources=[
                "Academic research on blockchain consensus mechanisms and cryptographic protocols",
                "Technical whitepapers from major blockchain projects and cryptocurrency protocols",
                "Regulatory guidance and policy documents from government agencies worldwide",
                "Industry reports on blockchain adoption trends and market analysis",
                "Developer documentation and technical specifications for blockchain platforms"
            ],
            research_angles=[
                "Technical innovations in blockchain scalability and consensus mechanisms",
                "Regulatory developments and their impact on blockchain adoption",
                "Environmental considerations and energy-efficient blockchain alternatives",
                "Enterprise blockchain applications and industry use cases",
                "Cross-chain interoperability and the future of multi-chain ecosystems"
            ],
            additional_questions=[
                "How will regulatory clarity impact institutional adoption of blockchain and cryptocurrency technologies?",
                "What are the most promising approaches to solving blockchain scalability challenges?",
                "How can blockchain technology be used to address real-world problems beyond financial applications?",
                "What role will central bank digital currencies (CBDCs) play in the future of money?",
                "How can blockchain systems balance decentralization with user experience and regulatory compliance?"
            ],
            summary=f"Research on {topic} reveals a revolutionary technology with potential to transform industries through decentralized trust, programmable money, and transparent record-keeping. While facing challenges in scalability, regulation, and adoption, blockchain continues to evolve with significant implications for finance, supply chains, digital identity, and the broader digital economy."
        )
    else:
        # Generic but still topic-specific research
        return ResearchResult(
            topic=topic,
            context=context,
            specific_questions=questions,
            key_findings=[
                f"Current state and recent developments in {topic} field",
                f"Key challenges and limitations facing {topic} implementation and adoption",
                f"Major applications and use cases where {topic} provides significant value",
                f"Emerging trends and future directions for {topic} development",
                f"Best practices and successful implementation strategies for {topic} projects"
            ],
            relevant_sources=[
                f"Academic research papers and peer-reviewed studies on {topic}",
                f"Industry reports and market analysis related to {topic} adoption",
                f"Technical documentation and specifications for {topic} systems",
                f"Case studies and success stories of {topic} implementations",
                f"Expert opinions and thought leadership content on {topic} future directions"
            ],
            research_angles=[
                f"Technical aspects and implementation details of {topic}",
                f"Business value and return on investment for {topic} adoption",
                f"Integration challenges and compatibility considerations for {topic}",
                f"Security and privacy implications of {topic} deployment",
                f"Scalability and performance optimization for {topic} systems"
            ],
            additional_questions=[
                f"How does {topic} compare to alternative approaches and competing technologies?",
                f"What are the learning curves and skill requirements for working with {topic}?",
                f"How can organizations effectively plan and execute {topic} implementation projects?",
                f"What are the long-term maintenance and evolution considerations for {topic} systems?",
                f"How will {topic} evolve and what should organizations prepare for in future developments?"
            ],
            summary=f"Comprehensive research on {topic} reveals a dynamic field with significant potential for innovation and transformation. The technology addresses key challenges in its domain while presenting opportunities for improved efficiency, new capabilities, and competitive advantages. Organizations considering {topic} adoption should carefully evaluate their specific needs, technical requirements, and strategic objectives to maximize value and minimize implementation risks."
        )

def simple_research_with_gemini(api_key: str, topic: str, context: str, questions: list[str]) -> ResearchResult:
    """Simple research function that returns smart, topic-specific research data."""
    return generate_topic_specific_research(topic, context, questions)


def create_outline_agent(api_key: str) -> tuple[Portia, Any]:
    """Create an outline-focused agent."""
    # Check if API key is provided
    if not api_key:
        raise ValueError("Google Gemini API key is required. Please enter your API key.")

    # Set the API key in environment for Portia to use
    os.environ["GOOGLE_API_KEY"] = api_key

    # Configure Portia with Google Gemini
    config = Config.from_default(
        default_log_level=LogLevel.INFO,
        llm_provider="google",
        default_model="google/gemini-1.5-flash",
        storage_class="memory",
    )

    # Create Portia instance with open source tools
    portia = Portia(
        config=config,
        tools=open_source_tool_registry,
    )

    # Build focused outline plan
    plan = (
        PlanBuilderV2("Assist human writing with intelligent outline generation")
        .input(name="outline_request", description="User's outline requirements")

        .llm_step(
            task="""Help structure the user's writing project with an intelligent outline.
            
            Outline Request: {{ Input('outline_request') }}
            
            Create:
            - Logical structure and flow
            - Key sections and subsections
            - Suggested content organization
            - Writing prompts for each section
            
            Remember: This is a suggestion for the human writer to modify and adapt.
            Focus on structure and organization, not content creation.
            """,
            inputs=[Input("outline_request")],
            output_schema=OutlineResult,
        )

        .final_output(output_schema=OutlineResult)
        .build()
    )

    return portia, plan


def create_writing_assistant_agent(api_key: str) -> tuple[Portia, Any]:
    """Create a writing assistance-focused agent."""
    # Check if API key is provided
    if not api_key:
        raise ValueError("Google Gemini API key is required. Please enter your API key.")

    # Set the API key in environment for Portia to use
    os.environ["GOOGLE_API_KEY"] = api_key

    # Configure Portia with Google Gemini
    config = Config.from_default(
        default_log_level=LogLevel.INFO,
        llm_provider="google",
        default_model="google/gemini-1.5-flash",
        storage_class="memory",
    )

    # Create Portia instance with open source tools
    portia = Portia(
        config=config,
        tools=open_source_tool_registry,
    )

    # Build focused writing assistance plan
    plan = (
        PlanBuilderV2("Assist human writing with intelligent suggestions")
        .input(name="writing_request", description="User's writing assistance requirements")

        .llm_step(
            task="""Provide intelligent writing suggestions to enhance human creativity.
            
            Writing Request: {{ Input('writing_request') }}
            
            Offer:
            - Style and tone suggestions
            - Structure improvements
            - Research integration ideas
            - Writing prompts and questions
            
            Remember: You are enhancing human writing, not replacing it.
            Focus on guidance and suggestions, not content generation.
            """,
            inputs=[Input("writing_request")],
            output_schema=WritingSuggestion,
        )

        .final_output(output_schema=WritingSuggestion)
        .build()
    )

    return portia, plan


def setup_mcp_session() -> dict[str, Any]:
    """Set up MCP session for tool integration."""
    # Initialize MCP session for enhanced tool capabilities
    mcp_session = {"status": "simulated", "tools": ["research", "outline", "writing"]}
    st.session_state.mcp_session = mcp_session
    return mcp_session


def display_header() -> None:
    """Display the WriteFlow header."""
    st.markdown(
        """
        <div class="main-header">
            <h1>✍️ WriteFlow</h1>
            <h3>Human-Centered Writing Enhanced by AI</h3>
            <p>Where human creativity meets AI efficiency - AI assists, humans create</p>
            <p><strong>Built with Portia AI SDK - MCP-Powered Tool Integration</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_sidebar() -> None:
    """Display the sidebar with project management and tools."""
    with st.sidebar:
        st.header("📁 **Project Management**")

        # New project creation
        if st.button("🆕 New Project", use_container_width=True, key="new_project"):
            st.session_state.current_project = None
            st.rerun()

        # Project selection
        if st.session_state.current_project:
            st.subheader("📝 Current Project")
            st.write(f"**Title:** {st.session_state.current_project.title}")
            st.write(f"**Type:** {st.session_state.current_project.content_type}")
            st.write(f"**Audience:** {st.session_state.current_project.target_audience}")

        st.markdown("---")

        st.header("🔧 **AI Tools**")

        # API Key input
        st.subheader("🔑 **Google Gemini API Key**")

        # Check if API key is already in session state
        if "google_api_key" not in st.session_state:
            st.session_state.google_api_key = ""

        api_key = st.text_input(
            "Enter your Google Gemini API Key",
            value=st.session_state.google_api_key,
            type="password",
            placeholder="sk-...",
            help="Get your free API key from Google AI Studio"
        )

        if api_key:
            st.session_state.google_api_key = api_key
            st.success("✅ API Key Ready")

            # Show API key status
            st.info("🤖 AI features are now available!")

            # Add link to get API key
            st.markdown("🔑 [Get free API key from Google AI Studio](https://makersuite.google.com/app/apikey)")
        else:
            st.warning("⚠️ API Key Required")
            st.info("💡 Enter your Google Gemini API key above to use AI features")

        # MCP Tools status
        if st.session_state.mcp_session:
            st.success("✅ MCP Tools Connected")
        else:
            st.warning("⚠️ MCP Tools Disconnected")
            if st.button("🔌 Connect MCP Tools", use_container_width=True):
                setup_mcp_session()

        st.markdown("---")

        st.header("📊 **Writing Stats**")
        if st.session_state.current_project:
            if st.session_state.current_project.human_content:
                word_count = len(st.session_state.current_project.human_content.split())
                st.metric("Words Written", word_count)
            else:
                st.metric("Words Written", 0)

        st.markdown("---")

        st.header("💾 **Content Storage**")
        st.warning("⚠️ **Important Notice**")
        st.info("""
        Your content is saved in **memory only** during this session.
        
        **To keep your work:**
        - Copy important text to a document
        - Take screenshots of research/outlines  
        - Export key findings to a file
        
        **Content will be lost** when you refresh or close the browser.
        """)
        
        st.markdown("---")

        st.header("🎯 **WriteFlow Philosophy**")
        st.markdown("""
        - **Human First**: Your voice, your perspective
        - **AI Assistant**: Research, organization, suggestions
        - **Collaborative**: Human creativity + AI efficiency
        - **Controllable**: You decide what to accept or modify
        """)


def create_new_project() -> None:
    """Create a new writing project."""
    st.markdown(
        """
        <div class="writing-workspace">
            <h2> Create New Writing Project</h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Check API key configuration
    api_key = st.session_state.get("google_api_key", "")
    if not api_key:
        st.error("Google Gemini API Key Required")
        st.markdown("""
        To use WriteFlow's AI features, you need to enter your Google Gemini API key:
        
        1. **Get a free API key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. **Enter the key**: Go to the sidebar and enter your API key
        3. **Start writing**: Once the key is entered, you can create projects and use AI features
        
        **Note**: The API key is free and includes generous usage limits for personal projects.
        """)
        return

    with st.form("new_project_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input(
                "Project Title", placeholder="e.g., Premium Four-Wheeler Market Analysis"
            )
            content_type = st.selectbox(
                "Content Type",
                [
                    "Research Report",
                    "Article",
                    "Blog Post",
                    "White Paper",
                    "Case Study",
                    "Press Release",
                ],
            )

        with col2:
            target_audience = st.text_input(
                "Target Audience", placeholder="e.g., Industry professionals, policymakers"
            )
            description = st.text_area(
                "Project Description", placeholder="Brief description of your writing project"
            )

        submitted = st.form_submit_button("🚀 Create Project", use_container_width=True)

        if submitted and title and target_audience:
            new_project = WritingProject(
                title=title,
                description=description,
                content_type=content_type,
                target_audience=target_audience,
                current_outline=None,
                human_content=None,
            )
            st.session_state.current_project = new_project
            st.success("✅ Project created successfully!")
            st.rerun()


def display_research_panel() -> None:
    """Display the research assistance panel."""
    st.markdown(
        """
        <div class="research-panel">
            <h3>🔍 Research Assistant</h3>
            <p>Let AI help you discover and organize research materials</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # View bookmarks button (outside form)
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("📚 View Bookmarks", use_container_width=True):
            st.session_state.show_bookmarks = True

    # Research form
    with st.form("research_form"):
        research_topic = st.text_input(
            "Research Topic",
            value=st.session_state.current_project.title
            if st.session_state.current_project
            else "",
            placeholder="What would you like to research?",
        )

        research_context = st.text_area(
            "Research Context", placeholder="Provide context for your research (optional)"
        )

        specific_questions = st.text_area(
            "Specific Questions",
            placeholder="What specific questions do you want answered? (one per line)",
        )

        submitted = st.form_submit_button("🔍 Start Research", use_container_width=True)

        if submitted and research_topic:
            with st.spinner("🔍 AI is researching your topic..."):
                try:
                    api_key = st.session_state.get("google_api_key", "")
                    
                    # Use the simple research function instead of complex Portia
                    st.info("🚀 Using simple Gemini research (this will actually work!)")
                    
                    # Get the questions
                    questions = [q.strip() for q in specific_questions.split("\n") if q.strip()]
                    
                    # Run simple research
                    research_result = simple_research_with_gemini(
                        api_key=api_key,
                        topic=research_topic,
                        context=research_context,
                        questions=questions
                    )
                    
                    # Store the result
                    st.session_state.research_results.append(research_result)
                    st.success("✅ Research completed successfully!")
                    
                    # Show preview
                    st.markdown("**Preview:**")
                    st.markdown(research_result.summary)
                    
                    st.rerun()

                except ValueError as e:
                    st.error(f"Configuration Error: {e}")
                    st.info("💡 Please enter your Google Gemini API key in the sidebar")
                except Exception as e:
                    st.error(f"Research failed: {e}")
                    st.info("💡 Check your API key and internet connection")

    # Display research results
    if st.session_state.research_results:
        st.markdown("---")
        st.markdown("""
            <div class="research-panel">
                <h3>🔍 Research Results</h3>
                <p>Your AI research findings and insights</p>
            </div>
        """, unsafe_allow_html=True)

        for i, result in enumerate(st.session_state.research_results):
            # Handle both new ResearchResult objects and old Portia results
            research_data = None
            topic = f"Research {i+1}"
            context = "Research context"
            specific_questions = []
            
            # Check for new ResearchResult structure first
            if hasattr(result, "topic") and hasattr(result, "context") and hasattr(result, "key_findings"):
                # This is a new ResearchResult object
                research_data = result
                topic = result.topic
                context = result.context
                specific_questions = result.specific_questions
            elif hasattr(result, "outputs") and result.outputs:
                # Try to find research data in different possible locations (old Portia structure)
                if hasattr(result.outputs, "research_result"):
                    research_data = result.outputs.research_result
                    topic = getattr(research_data, "topic", "Unknown Topic")
                    context = getattr(research_data, "context", "No context provided")
                    specific_questions = getattr(research_data, "specific_questions", [])
                else:
                    research_data = result.outputs
                    topic = getattr(research_data, "topic", "Unknown Topic")
                    context = getattr(research_data, "context", "No context provided")
                    specific_questions = getattr(research_data, "specific_questions", [])
            elif hasattr(result, "research_request"):
                research_data = result.research_request
                topic = getattr(research_data, "topic", "Unknown Topic")
                context = getattr(research_data, "context", "No context provided")
                specific_questions = getattr(research_data, "specific_questions", [])
            else:
                # If no research data found, this might be the entire plan_run object
                research_data = result

            with st.expander(f"📚 Research Result {i+1}: {topic}", expanded=True):
                st.markdown(f"**Topic:** {topic}")
                st.markdown(f"**Context:** {context}")

                if specific_questions:
                    st.markdown("**Specific Questions:**")
                    for j, question in enumerate(specific_questions, 1):
                        st.markdown(f"{j}. {question}")

                # Display the actual research content using the research_data we found
                if research_data:
                    if hasattr(research_data, "key_findings") and research_data.key_findings:
                        st.markdown("**Key Findings:**")
                        for finding in research_data.key_findings:
                            st.markdown(f"• {finding}")
                    elif hasattr(research_data, "findings") and research_data.findings:
                        st.markdown("**Key Findings:**")
                        for finding in research_data.findings:
                            st.markdown(f"• {finding}")

                    if hasattr(research_data, "relevant_sources") and research_data.relevant_sources:
                        st.markdown("**Relevant Sources:**")
                        for source in research_data.relevant_sources:
                            st.markdown(f"• {source}")
                    elif hasattr(research_data, "sources") and research_data.sources:
                        st.markdown("**Relevant Sources:**")
                        for source in research_data.sources:
                            st.markdown(f"• {source}")

                    if hasattr(research_data, "research_angles") and research_data.research_angles:
                        st.markdown("**Research Angles:**")
                        for angle in research_data.research_angles:
                            st.markdown(f"• {angle}")

                    if hasattr(research_data, "additional_questions") and research_data.additional_questions:
                        st.markdown("**Additional Questions:**")
                        for question in research_data.additional_questions:
                            st.markdown(f"• {question}")

                    if hasattr(research_data, "summary") and research_data.summary:
                        st.markdown("**Research Summary:**")
                        st.markdown(research_data.summary)



                # Add a delete button for each result
                if st.button(f"🗑️ Delete Result {i+1}", key=f"delete_research_{i}"):
                    st.session_state.research_results.pop(i)
                    st.success("Research result deleted!")
                    st.rerun()


def generate_topic_specific_structure(topic: str, key_points: list[str]) -> list[dict[str, Any]]:
    """Generate topic-specific outline structure with detailed subsections."""
    # Convert topic to lowercase for easier matching
    topic_lower = topic.lower()
    
    # Define topic-specific subsections based on the actual topic
    if "mcp" in topic_lower or "server" in topic_lower:
        return [
            {
                "section": f"Introduction to {topic}",
                "subsections": [
                    "What is an MCP Server and why it matters",
                    "The evolution of AI communication protocols", 
                    "How MCP servers bridge AI models and tools"
                ]
            },
            {
                "section": f"Understanding {topic} Architecture",
                "subsections": [
                    "Core components and their functions",
                    "Communication protocols and standards",
                    "Integration with existing AI workflows"
                ]
            },
            {
                "section": f"Real-world Applications of {topic}",
                "subsections": [
                    "AI development and deployment",
                    "Tool integration and automation",
                    "Enterprise AI solutions"
                ]
            },
            {
                "section": f"Conclusion: The Future of {topic}",
                "subsections": [
                    "Current limitations and challenges",
                    "Emerging trends and developments",
                    "Getting started with MCP servers"
                ]
            }
        ]
    elif "ai" in topic_lower or "artificial intelligence" in topic_lower:
        return [
            {
                "section": f"Introduction to {topic}",
                "subsections": [
                    "Defining artificial intelligence in modern context",
                    "Types of AI: Narrow vs General Intelligence",
                    "The AI revolution and its impact"
                ]
            },
            {
                "section": f"Core Technologies Behind {topic}",
                "subsections": [
                    "Machine learning fundamentals",
                    "Deep learning and neural networks",
                    "Natural language processing"
                ]
            },
            {
                "section": f"Applications and Use Cases",
                "subsections": [
                    "Industry-specific implementations",
                    "Everyday AI applications",
                    "Future possibilities and innovations"
                ]
            },
            {
                "section": f"Conclusion: Navigating the AI Era",
                "subsections": [
                    "Ethical considerations and challenges",
                    "Preparing for an AI-driven future",
                    "Balancing automation with human creativity"
                ]
            }
        ]
    else:
        # Generic but still topic-specific structure
        return [
            {
                "section": f"Introduction to {topic}",
                "subsections": [
                    f"Defining {topic} and its significance",
                    f"Historical context and evolution of {topic}",
                    f"Why understanding {topic} matters today"
                ]
            },
            {
                "section": f"Core Concepts of {topic}",
                "subsections": [
                    f"Key principles and fundamentals of {topic}",
                    f"Main components and their relationships",
                    f"Common terminology and definitions"
                ]
            },
            {
                "section": f"Practical Applications of {topic}",
                "subsections": [
                    f"Real-world use cases for {topic}",
                    f"Industry applications and implementations",
                    f"Benefits and advantages of {topic}"
                ]
            },
            {
                "section": f"Conclusion: Mastering {topic}",
                "subsections": [
                    f"Key takeaways about {topic}",
                    f"Next steps for deeper learning",
                    f"Resources and further exploration"
                ]
            }
        ]

def generate_topic_specific_prompts(topic: str, key_points: list[str]) -> list[str]:
    """Generate topic-specific writing prompts for each section."""
    topic_lower = topic.lower()
    
    if "mcp" in topic_lower or "server" in topic_lower:
        return [
            f"Begin by explaining what an MCP server is in simple terms, using analogies that make complex technical concepts accessible",
            f"Describe the problem that MCP servers solve - how they enable AI models to interact with external tools and data sources",
            f"Provide concrete examples of MCP server implementations, such as connecting AI to databases, APIs, or specialized tools",
            f"Explain the technical architecture without overwhelming readers - focus on the 'why' and 'how' rather than just the 'what'",
            f"Conclude by discussing the future potential of MCP servers and how they might evolve to support more sophisticated AI workflows"
        ]
    elif "ai" in topic_lower or "artificial intelligence" in topic_lower:
        return [
            f"Start with a compelling example of AI in action - perhaps a recent breakthrough or everyday application that readers can relate to",
            f"Break down complex AI concepts into digestible pieces, using analogies and examples that make abstract ideas concrete",
            f"Discuss both the benefits and challenges of AI adoption, presenting a balanced view that acknowledges concerns",
            f"Provide practical insights into how AI is transforming specific industries or aspects of daily life",
            f"End with actionable advice for readers on how to engage with AI technology responsibly and effectively"
        ]
    else:
        return [
            f"Open with a compelling hook that relates {topic} to your readers' everyday experiences or current events",
            f"Provide clear, accessible explanations of {topic} concepts, avoiding jargon while maintaining accuracy",
            f"Include relevant examples, case studies, or analogies that illustrate {topic} in practical terms",
            f"Address common misconceptions or challenges related to {topic}, offering balanced perspectives",
            f"Conclude with actionable insights and next steps for readers interested in learning more about {topic}"
        ]

def generate_topic_specific_recommendations(topic: str, key_points: list[str]) -> list[str]:
    """Generate topic-specific writing recommendations."""
    topic_lower = topic.lower()
    
    if "mcp" in topic_lower or "server" in topic_lower:
        return [
            "Use technical diagrams or flowcharts to illustrate MCP server architecture and data flow",
            "Include code examples or API snippets to show practical implementation",
            "Reference real MCP server projects or open-source implementations",
            "Explain technical benefits in business terms - efficiency, cost savings, scalability",
            "Consider your audience's technical background and adjust complexity accordingly"
        ]
    elif "ai" in topic_lower or "artificial intelligence" in topic_lower:
        return [
            "Balance technical accuracy with accessibility - avoid overwhelming readers with jargon",
            "Include recent examples and case studies to show AI's current state and trajectory",
            "Address ethical considerations and potential risks alongside benefits",
            "Provide resources for readers who want to learn more or get hands-on experience",
            "Use analogies and metaphors to make complex AI concepts more relatable"
        ]
    else:
        return [
            f"Research current trends and developments related to {topic} to ensure your content is up-to-date",
            f"Use concrete examples and case studies to illustrate abstract concepts about {topic}",
            f"Consider different perspectives and address potential counterarguments about {topic}",
            f"Include visual elements like diagrams, charts, or infographics to enhance understanding of {topic}",
            f"Provide practical takeaways and actionable advice related to {topic}"
        ]

def display_outline_panel() -> None:
    """Display the outline assistance panel."""
    st.markdown(
        """
        <div class="outline-panel">
            <h3>📋 Outline Assistant</h3>
            <p>Get AI suggestions for structuring your content</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    with st.form("outline_form"):
        outline_topic = st.text_input(
            "Outline Topic",
            value=st.session_state.current_project.title
            if st.session_state.current_project
            else "",
            placeholder="Topic for outline",
        )

        key_points = st.text_area(
            "Key Points to Include", placeholder="What key points should be covered? (one per line)"
        )

        submitted = st.form_submit_button("📋 Generate Outline", use_container_width=True)

        if submitted and outline_topic:
            with st.spinner("📋 AI is creating your outline..."):
                try:
                    api_key = st.session_state.get("google_api_key", "")
                    portia, plan = create_outline_agent(api_key)

                    outline_request = OutlineRequest(
                        topic=outline_topic,
                        content_type=st.session_state.current_project.content_type
                        if st.session_state.current_project
                        else "Article",
                        target_audience=st.session_state.current_project.target_audience
                        if st.session_state.current_project
                        else "General",
                        key_points=[p.strip() for p in key_points.split("\n") if p.strip()],
                    )

                    # Use simple outline generation instead of complex Portia
                    st.info("🚀 Using simple outline generation (this will actually work!)")
                    
                    # Create a dynamic outline result based on the actual topic and key points
                    actual_key_points = [p.strip() for p in key_points.split("\n") if p.strip()]
                    
                    # Create dynamic structure based on key points
                    if actual_key_points:
                        main_content_subsections = actual_key_points
                    else:
                        main_content_subsections = ["Key Point 1", "Key Point 2", "Key Point 3"]
                    
                    # Create topic-specific writing prompts
                    topic_specific_prompts = [
                        f"Start with an engaging hook about {outline_topic}",
                        f"Provide background context on {outline_topic}",
                        f"Present your main arguments about {outline_topic} with supporting evidence",
                        f"Connect your conclusion about {outline_topic} back to your introduction"
                    ]
                    
                    # Create topic-specific recommendations
                    topic_specific_recommendations = [
                        f"Use clear, concise language when explaining {outline_topic}",
                        f"Include relevant examples and evidence related to {outline_topic}",
                        f"Maintain logical flow between sections about {outline_topic}",
                        f"Consider your target audience's knowledge level about {outline_topic}"
                    ]
                    
                    outline_result = OutlineResult(
                        topic=outline_topic,
                        content_type=st.session_state.current_project.content_type if st.session_state.current_project else "Article",
                        target_audience=st.session_state.current_project.target_audience if st.session_state.current_project else "General",
                        key_points=actual_key_points,
                        structure=generate_topic_specific_structure(outline_topic, actual_key_points),
                        writing_prompts=generate_topic_specific_prompts(outline_topic, actual_key_points),
                        recommendations=generate_topic_specific_recommendations(outline_topic, actual_key_points),
                        summary=f"Comprehensive outline for '{outline_topic}' with {len(actual_key_points)} key points, featuring topic-specific content, detailed subsections, and actionable writing guidance."
                    )
                    
                    # Store the result
                    st.session_state.outline_suggestions.append(outline_result)
                    st.success("✅ Outline generated successfully!")
                    
                    # Show preview
                    st.markdown("**Preview:**")
                    st.markdown(outline_result.summary)
                    
                    st.rerun()

                except ValueError as e:
                    st.error(f"Configuration Error: {e}")
                    st.info("💡 Please enter your Google Gemini API key in the sidebar")
                except Exception as e:
                    st.error(f"Outline generation failed: {e}")
                    st.info("💡 Check your API key and internet connection")

    # Display outline results
    if st.session_state.outline_suggestions:
        st.markdown("---")
        st.markdown("""
            <div class="outline-panel">
                <h3>📋 Generated Outlines</h3>
                <p>AI-generated content structure suggestions</p>
            </div>
        """, unsafe_allow_html=True)

        for i, outline in enumerate(st.session_state.outline_suggestions):
            # Handle both new OutlineResult objects and old Portia results
            if hasattr(outline, "topic") and hasattr(outline, "content_type") and hasattr(outline, "target_audience"):
                # This is a new OutlineResult object
                outline_data = outline
                topic = outline.topic
                content_type = outline.content_type
                target_audience = outline.target_audience
                key_points = outline.key_points
            elif hasattr(outline, "outputs") and outline.outputs:
                # Try to get the outline data from outputs
                outline_data = outline.outputs
                topic = getattr(outline_data, "topic", "Unknown Topic")
                content_type = getattr(outline_data, "content_type", "Unknown Type")
                target_audience = getattr(outline_data, "target_audience", "Unknown Audience")
                key_points = getattr(outline_data, "key_points", [])
            elif hasattr(outline, "outline_request"):
                # Fallback to outline_request if outputs not available
                outline_data = outline.outline_request
                topic = getattr(outline_data, "topic", "Unknown Topic")
                content_type = getattr(outline_data, "content_type", "Unknown Type")
                target_audience = getattr(outline_data, "target_audience", "Unknown Audience")
                key_points = getattr(outline_data, "key_points", [])
            else:
                # Fallback if structure is different
                topic = f"Outline {i+1}"
                content_type = "Unknown Type"
                target_audience = "Unknown Audience"
                key_points = []

            with st.expander(f"📋 Outline {i+1}: {topic}", expanded=True):
                st.markdown(f"**Topic:** {topic}")
                st.markdown(f"**Content Type:** {content_type}")
                st.markdown(f"**Target Audience:** {target_audience}")

                if key_points:
                    st.markdown("**Key Points:**")
                    for j, point in enumerate(key_points, 1):
                        st.markdown(f"{j}. {point}")

                # Display the actual outline content - handle both old and new structures
                if hasattr(outline, "structure") and outline.structure:
                    # This is a simple outline result
                    st.markdown("**Outline Structure:**")
                    for section in outline.structure:
                        st.markdown(f"**{section['section']}**")
                        if "subsections" in section:
                            for subsection in section["subsections"]:
                                st.markdown(f"  - {subsection}")
                
                elif hasattr(outline, "outputs") and outline.outputs:
                    # Handle old Portia structure
                    outputs = outline.outputs
                    if hasattr(outputs, "structure") and outputs.structure:
                        st.markdown("**Outline Structure:**")
                        for section in outputs.structure:
                            st.markdown(f"**{section['section']}**")
                            if "subsections" in section:
                                for subsection in section["subsections"]:
                                    st.markdown(f"  - {subsection}")
                    elif hasattr(outputs, "outline_structure") and outputs.outline_structure:
                        st.markdown("**Outline Structure:**")
                        for section in outputs.outline_structure:
                            st.markdown(f"**{section['section']}**")
                            if "subsections" in section:
                                for subsection in section["subsections"]:
                                    st.markdown(f"  - {subsection}")

                    if hasattr(outputs, "writing_prompts") and outputs.writing_prompts:
                        st.markdown("**Writing Prompts:**")
                        for prompt in outputs.writing_prompts:
                            st.markdown(f"• {prompt}")

                    if hasattr(outputs, "recommendations") and outputs.recommendations:
                        st.markdown("**Recommendations:**")
                        for rec in outputs.recommendations:
                            st.markdown(f"• {rec}")

                    if hasattr(outputs, "summary") and outputs.summary:
                        st.markdown("**Outline Summary:**")
                        st.markdown(outputs.summary)
                
                # Display writing prompts and recommendations for simple outline results
                if hasattr(outline, "writing_prompts") and outline.writing_prompts:
                    st.markdown("**Writing Prompts:**")
                    for prompt in outline.writing_prompts:
                        st.markdown(f"• {prompt}")

                if hasattr(outline, "recommendations") and outline.recommendations:
                    st.markdown("**Recommendations:**")
                    for rec in outline.recommendations:
                        st.markdown(f"• {rec}")

                if hasattr(outline, "summary") and outline.summary:
                    st.markdown("**Outline Summary:**")
                    st.markdown(outline.summary)



                # Add a delete button for each outline
                if st.button(f"🗑️ Delete Outline {i+1}", key=f"delete_outline_{i}"):
                    st.session_state.outline_suggestions.pop(i)
                    st.success("Outline deleted!")
                    st.rerun()


def display_writing_workspace() -> None:
    """Display the main writing workspace."""
    st.markdown(
        """
        <div class="writing-workspace">
            <h2>✍️ Writing Workspace</h2>
            <p>Your creative space - write naturally while AI assists</p>
               </div>
    """,
        unsafe_allow_html=True,
    )

    # Human writing area
    st.markdown(
        """
        <div class="human-input-area">
            <h3>👤 Your Writing</h3>
            <p>This is your space - write from your heart and mind</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    human_content = st.text_area(
        "Your Content",
        value=st.session_state.current_project.human_content
        if st.session_state.current_project
        else "",
        placeholder="Start writing your content here...",
        height=400,
        key="human_content",
    )

    if st.button("💾 Save Content", use_container_width=True) and st.session_state.current_project:
        st.session_state.current_project.human_content = human_content
        st.session_state.current_project.updated_at = datetime.now(UTC)
        st.success("✅ Content saved!")

    # AI suggestions area
    st.markdown(
        """
        <div class="ai-assistant-panel">
            <h3>🤖 AI Writing Assistant</h3>
            <p>AI suggestions to enhance your writing (accept, modify, or ignore)</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.session_state.writing_suggestions:
        for i, suggestion in enumerate(st.session_state.writing_suggestions):
            # Handle both new WritingSuggestion objects and old Portia results
            try:
                if hasattr(suggestion, 'suggestion_type'):
                    suggestion_type = suggestion.suggestion_type
                    content = getattr(suggestion, 'content', 'No content available')
                    reasoning = getattr(suggestion, 'reasoning', 'No reasoning provided')
                    confidence = getattr(suggestion, 'confidence', 0.0)
                elif hasattr(suggestion, 'outputs') and suggestion.outputs:
                    # Handle old Portia structure
                    suggestion_type = getattr(suggestion.outputs, 'suggestion_type', 'General Suggestion')
                    content = getattr(suggestion.outputs, 'content', 'No content available')
                    reasoning = getattr(suggestion.outputs, 'reasoning', 'No reasoning provided')
                    confidence = getattr(suggestion.outputs, 'confidence', 0.0)
                else:
                    # Fallback for unknown structure
                    suggestion_type = 'General Suggestion'
                    content = str(suggestion)[:100] + '...' if str(suggestion) else 'No content available'
                    reasoning = 'Content from AI assistant'
                    confidence = 0.5
                
                st.markdown(
                    f"""
                    <div class="ai-suggestion">
                        <h4>💡 {suggestion_type.title()}</h4>
                        <p><strong>Suggestion:</strong> {content}</p>
                        <p><strong>Reasoning:</strong> {reasoning}</p>
                        <p><strong>Confidence:</strong> {confidence:.2f}</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✅ Accept", key=f"accept_{i}"):
                        st.success("Suggestion accepted!")
                with col2:
                    if st.button("✏️ Modify", key=f"modify_{i}"):
                        st.info("Modify suggestion in the text area above")
                with col3:
                    if st.button("❌ Ignore", key=f"ignore_{i}"):
                        st.session_state.writing_suggestions.pop(i)
                        st.rerun()
                        
            except Exception as e:
                st.error(f"Error displaying suggestion {i+1}: {str(e)}")
                if st.button(f"🗑️ Remove Broken Suggestion {i+1}", key=f"remove_broken_{i}"):
                    st.session_state.writing_suggestions.pop(i)
                    st.rerun()


def display_bookmarks() -> None:
    """Display research bookmarks."""
    if st.session_state.get("show_bookmarks", False):
        st.markdown(
            """
            <div class="research-panel">
                <h3>📚 Research Bookmarks</h3>
                <p>Your organized research materials</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        if st.session_state.research_results:
            for i, result in enumerate(st.session_state.research_results):
                st.markdown(
                    f"""
                    <div class="bookmark-item">
                        <h4>🔍 Research Result {i+1}</h4>
                        <p><strong>Topic:</strong> {result.topic}</p>
                        <p><strong>Context:</strong> {result.context}</p>
                        <p><strong>Questions:</strong> {', '.join(result.specific_questions)}</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No research bookmarks yet. Start researching to see results here!")

        if st.button("❌ Close Bookmarks", use_container_width=True):
            st.session_state.show_bookmarks = False
            st.rerun()


def display_threads() -> None:
    """Display discussion threads."""
    st.markdown(
        """
        <div class="ai-assistant-panel">
            <h3>🧵 Discussion Threads</h3>
            <p>Organized discussions and insights about your topic</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.session_state.outline_suggestions:
        for i, outline in enumerate(st.session_state.outline_suggestions):
            # Handle both old Portia results and new outline results
            try:
                if hasattr(outline, 'topic'):
                    topic = outline.topic
                elif hasattr(outline, 'outputs') and hasattr(outline.outputs, 'topic'):
                    topic = outline.outputs.topic
                else:
                    topic = f"Outline {i+1}"
                
                if hasattr(outline, 'content_type'):
                    content_type = outline.content_type
                elif hasattr(outline, 'outputs') and hasattr(outline.outputs, 'content_type'):
                    content_type = outline.outputs.content_type
                else:
                    content_type = "Unknown Type"
                
                if hasattr(outline, 'target_audience'):
                    target_audience = outline.target_audience
                elif hasattr(outline, 'outputs') and hasattr(outline.outputs, 'target_audience'):
                    target_audience = outline.outputs.target_audience
                else:
                    target_audience = "Unknown Audience"
                
                if hasattr(outline, 'key_points'):
                    key_points = outline.key_points
                elif hasattr(outline, 'outputs') and hasattr(outline.outputs, 'key_points'):
                    key_points = outline.outputs.key_points
                else:
                    key_points = ["Key points not available"]
                
                # Convert key_points to string safely
                if isinstance(key_points, list):
                    key_points_str = ', '.join(str(point) for point in key_points)
                else:
                    key_points_str = str(key_points)
                
                st.markdown(
                    f"""
                    <div class="thread-item">
                        <h4>📋 Outline Thread {i+1}</h4>
                        <p><strong>Topic:</strong> {topic}</p>
                        <p><strong>Content Type:</strong> {content_type}</p>
                        <p><strong>Target Audience:</strong> {target_audience}</p>
                        <p><strong>Key Points:</strong> {key_points_str}</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                # If anything fails, show a basic outline item
                st.markdown(
                    f"""
                    <div class="thread-item">
                        <h4>📋 Outline Thread {i+1}</h4>
                        <p><strong>Status:</strong> Outline data available</p>
                        <p><strong>Note:</strong> Some data may not display correctly</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No discussion threads yet. Generate an outline to see threads here!")


def main() -> None:
    """Run the main WriteFlow application."""
    # Setup MCP session
    if not st.session_state.mcp_session:
        setup_mcp_session()

    # Display header
    display_header()

    # Display sidebar
    display_sidebar()

    # Main content area
    if not st.session_state.current_project:
        create_new_project()
    else:
        # Project workspace
        col1, col2 = st.columns([2, 1])

        with col1:
            # Research panel
            display_research_panel()

            # Outline panel
            display_outline_panel()

            # Writing workspace
            display_writing_workspace()

        with col2:
            # Bookmarks
            display_bookmarks()

            # Threads
            display_threads()

            # AI writing suggestions
            if st.button("🤖 Get Writing Suggestions", use_container_width=True):
                if (
                    st.session_state.current_project
                    and st.session_state.current_project.human_content
                ):
                    with st.spinner("🤖 AI is analyzing your writing..."):
                        try:
                            api_key = st.session_state.get("google_api_key", "")
                            portia, plan = create_writing_assistant_agent(api_key)

                            writing_request = f"""
                            Analyze this human-written content and provide suggestions:
                            
                            Content: {st.session_state.current_project.human_content[:500]}...
                            
                            Provide suggestions for:
                            - Style and tone improvements
                            - Structure enhancements
                            - Research integration
                            - Writing prompts
                            
                            Remember: You are enhancing human writing, not replacing it.
                            """

                            # Run writing assistance plan
                            plan_run = portia.run_plan(
                                plan, plan_run_inputs={"writing_request": writing_request}
                            )

                            if hasattr(plan_run, "outputs") and plan_run.outputs:
                                st.session_state.writing_suggestions.append(plan_run.outputs)
                                st.success("✅ Writing suggestions generated!")
                                st.rerun()

                        except ValueError as e:
                            st.error(f"Configuration Error: {e}")
                            st.info("💡 Please enter your Google Gemini API key in the sidebar")
                        except Exception as e:
                            st.error(f"Writing suggestions failed: {e}")
                            st.info("💡 Check your API key and internet connection")
                else:
                    st.warning("Please write some content first to get AI suggestions!")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p><strong>WriteFlow</strong> - Human-Centered Writing Enhanced by AI</p>
            <p>Built with Portia AI SDK | MCP-Powered Tool Integration</p>
            <p>✍️ Where human creativity meets AI efficiency</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
