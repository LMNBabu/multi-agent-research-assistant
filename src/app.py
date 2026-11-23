import streamlit as st
from agents.research_crew import create_research_crew

# Page Configuration
st.set_page_config(page_title="AI Research Assistant", page_icon="🔍", layout="wide")

# Custom CSS for better readability
st.markdown("""
    <style>
    .stAlert { padding: 1rem; }
    .report-section { margin-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🔍 Multi-Agent AI Research Assistant")
    st.markdown("Powered by CrewAI, Gemini, and Tavily Search.")
    
    # Input Section
    with st.form("research_form"):
        topic = st.text_input("Enter your research topic:", placeholder="e.g., The impact of solid-state batteries on EV range")
        submitted = st.form_submit_button("Generate Research Report", type="primary", use_container_width=True)

    if submitted and topic:
        with st.spinner("🧠 Research Manager is planning the workflow..."):
            try:
                # Initialize and run the crew
                crew = create_research_crew(topic)
                
                # We use a placeholder to update status as agents work
                status_placeholder = st.empty()
                status_placeholder.info("🔍 Agents are researching and analyzing... (Check terminal for detailed logs)")
                
                result = crew.kickoff(inputs={"topic": topic})
                
                status_placeholder.empty()
                
                # Extract the Pydantic model
                report = result.pydantic
                
                if not report:
                    st.error("The agents failed to generate a structured report. Please try again.")
                    return

                # --- RENDER REPORT ---
                st.markdown("---")
                st.header(report.title)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("📖 Introduction")
                    st.write(report.introduction)
                    
                    st.subheader("🔑 Key Findings")
                    for finding in report.key_findings:
                        st.markdown(f"- {finding}")
                        
                    st.subheader("📊 Analysis")
                    st.write(report.analysis)
                    
                    st.subheader("⚠️ Limitations")
                    st.write(report.limitations)
                    
                    st.subheader("🎯 Conclusion")
                    st.write(report.conclusion)

                with col2:
                    st.subheader("🔗 References")
                    if report.references:
                        for ref in report.references:
                            st.markdown(f"**[{ref.title}]({ref.url})**")
                    else:
                        st.info("No specific references were captured.")

            except Exception as e:
                st.error(f"An error occurred during research: {str(e)}")
                st.info("Please check your API keys in the .env file and ensure you have internet access.")

if __name__ == "__main__":
    main()