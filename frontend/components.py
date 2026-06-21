import streamlit as st
import plotly.graph_objects as go

def load_css(file_name: str):
    """Loads external CSS into the Streamlit app to inject custom styling."""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file '{file_name}' not found.")

def status_card(risk_score: int):
    """Renders the main patient status card based on the Overall Risk Score."""
    # Determine color and text based on risk thresholds
    if risk_score < 30:
        status_class = "safe"
        status_text = "🟢 SAFE"
    elif risk_score < 60:
        status_class = "monitor"
        status_text = "🟡 MONITOR"
    elif risk_score < 80:
        status_class = "warning"
        status_text = "🟠 WARNING"
    else:
        status_class = "emergency"
        status_text = "🔴 EMERGENCY"

    html = f"""
    <div class="status-card {status_class}">
        <h2>Patient Status: {status_text}</h2>
        <p style="font-size: 1.4rem; margin: 0; font-weight: 600;">Overall Risk Score: {risk_score}/100</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def emergency_alert(alert_text: str):
    """Renders a highly visible flashing alert panel."""
    html = f"""
    <div class="alert-panel">
        ⚠ {alert_text}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_gauge(title: str, value: int, color: str = None):
    """Renders a clean, professional Plotly gauge chart."""
    
    # Auto-assign color based on severity if not explicitly provided
    if color is None:
        if value < 30:
            color = "#28a745" # Green
        elif value < 60:
            color = "#ffc107" # Yellow
        elif value < 80:
            color = "#fd7e14" # Orange
        else:
            color = "#dc3545" # Red

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20, 'color': '#2c3e50', 'family': 'Inter'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e9ecef",
            'steps': [
                {'range': [0, 30], 'color': "rgba(40, 167, 69, 0.15)"},
                {'range': [30, 60], 'color': "rgba(255, 193, 7, 0.15)"},
                {'range': [60, 80], 'color': "rgba(253, 126, 20, 0.15)"},
                {'range': [80, 100], 'color': "rgba(220, 53, 69, 0.15)"}],
            'threshold': {
                'line': {'color': "#2c3e50", 'width': 4},
                'thickness': 0.75,
                'value': value}
        }
    ))
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        height=250,
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#212529", 'family': "Inter"}
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def module_panel(title: str, data: dict):
    """Render a clean module panel using native Streamlit components."""

    with st.container(border=True):

        st.subheader(title)

        for key, val in data.items():

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**{key}**")

            with col2:
                if str(val) == "Detected":
                    st.error(val)

                elif str(val) == "Irregular":
                    st.warning(val)

                elif (
                    isinstance(val, str)
                    and "%" in val
                    and val.replace("%", "").isdigit()
                    and int(val.replace("%", "")) >= 80
                ):
                    st.error(val)

                else:
                    st.success(val)

        st.markdown("")

def timeline_event(time: str, text: str):
    """Renders a single event in the vertical timeline."""
    html = f"""
    <div class="timeline-event">
        <div class="timeline-time">{time}</div>
        <div class="timeline-text">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
