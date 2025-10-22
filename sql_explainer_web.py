import streamlit as st
from groq import Groq
import os

# Page configuration
st.set_page_config(
    page_title="SQL Query Explainer",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("🔍 AI-Powered SQL Query Explainer")
st.markdown("Paste any SQL query and get instant AI analysis with explanations, performance insights, and optimization tips.")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "Groq API Key:", 
        type="password",
        help="Get your free API key from console.groq.com"
    )
    st.markdown("---")
    st.markdown("### About")
    st.info("Built by Nagabhushan Reddy Kadiri\n\nPart of AI PM Portfolio")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Your SQL Query")
    
    # SQL input area
    sql_query = st.text_area(
        "Paste your SQL query here:",
        height=300,
        placeholder="""SELECT u.name, COUNT(o.id) as orders
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING COUNT(o.id) > 5"""
    )
    
    # Analyze button
    analyze_button = st.button("🚀 Analyze Query", type="primary", use_container_width=True)

with col2:
    st.subheader("🤖 AI Analysis")
    
    # Analysis results area
    if analyze_button:
        if not sql_query.strip():
            st.error("⚠️ Please enter a SQL query to analyze!")
        elif not api_key:
            st.error("⚠️ Please enter your Groq API key in the sidebar!")
        else:
            # Show loading spinner
            with st.spinner("🔄 Analyzing your query..."):
                try:
                    # Initialize Groq client
                    client = Groq(api_key=api_key)
                    
                    # Create prompt
                    prompt = f"""You are a SQL expert. Analyze this query:

{sql_query}

Provide:
1. **Plain English Explanation**
2. **Key Operations**
3. **Performance Analysis**
4. **Optimization Suggestions**

Be clear and actionable."""

                    # Call Groq API
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    # Display result
                    result = response.choices[0].message.content
                    st.success("✅ Analysis Complete!")
                    st.markdown(result)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.info("👈 Enter your SQL query and click 'Analyze Query' to get started!")

# Footer with examples
st.markdown("---")
with st.expander("📚 See Example Queries"):
    st.markdown("### Simple Query")
    st.code("""SELECT name, email 
FROM customers 
WHERE status = 'active'""", language="sql")
    
    st.markdown("### Complex Query")
    st.code("""SELECT 
    c.customer_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.created_at >= '2024-01-01'
GROUP BY c.id, c.customer_name
HAVING COUNT(o.order_id) > 5
ORDER BY total_spent DESC
LIMIT 10""", language="sql")

st.markdown("---")
st.markdown("**💡 Pro Tip:** For best results, paste complete SQL queries including SELECT, FROM, WHERE, etc.")
