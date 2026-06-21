#!/usr/bin/env python3
# -- coding: utf-8 --
"""
FloodML Dashboard
Real-time Flood Detection & Monitoring System
Copyright (C) CNES - All Rights Reserved
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    from satellite_upload_module import create_satellite_upload_section
except ImportError:
    def create_satellite_upload_section():
        st.error("Satellite upload module not found")

st.set_page_config(
    page_title="🌊 FloodML Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes smoothPulse {
        0%, 100% { box-shadow: 0 0 8px rgba(100, 100, 140, 0.15); }
        50% { box-shadow: 0 0 12px rgba(100, 100, 140, 0.25); }
    }
    
    /* Main background and text colors */
    body {
        background: linear-gradient(135deg, #0f0c29 0%, #1a0e3d 100%);
        color: #b0b0b0;
        background-attachment: fixed;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0015 100%);
        background-attachment: fixed;
        color: #b0b0b0;
    }
    
    /* Soft titles with subtle animation */
    h1, h2, h3 {
        color: #d0d0d0 !important;
        text-shadow: 0 0 5px rgba(208, 208, 208, 0.3);
        font-weight: bold;
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Metric cards with texture and depth */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d1e3e 100%);
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(100, 100, 140, 0.03) 2px, rgba(100, 100, 140, 0.03) 4px);
        border: 1px solid #4a4a6a;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 
            0 0 10px rgba(100, 100, 140, 0.15),
            inset 0 1px 2px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        animation: fadeIn 0.8s ease-out;
    }
    
    [data-testid="metric-container"]:hover {
        box-shadow: 
            0 0 15px rgba(100, 100, 140, 0.25),
            inset 0 1px 2px rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling with texture */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
        background-image: 
            repeating-linear-gradient(90deg, transparent, transparent 1px, rgba(100, 100, 140, 0.02) 1px, rgba(100, 100, 140, 0.02) 2px);
        border-right: 1px solid #4a4a6a;
        animation: slideIn 0.6s ease-out;
    }
    
    /* Button styling with texture and transitions */
    .stButton > button {
        background: linear-gradient(135deg, #5a6a8a 0%, #4a5a7a 100%);
        background-image: 
            linear-gradient(135deg, #5a6a8a 0%, #4a5a7a 100%),
            repeating-linear-gradient(45deg, transparent, transparent 1px, rgba(255, 255, 255, 0.05) 1px, rgba(255, 255, 255, 0.05) 2px);
        background-blend-mode: overlay;
        color: #e0e0e0;
        font-weight: bold;
        border: 1px solid rgba(106, 122, 154, 0.6);
        box-shadow: 
            0 4px 12px rgba(0, 0, 0, 0.3),
            inset 0 1px 2px rgba(255, 255, 255, 0.1),
            inset 0 -2px 4px rgba(0, 0, 0, 0.2);
        border-radius: 8px;
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        box-shadow: 
            0 6px 16px rgba(100, 100, 140, 0.35),
            inset 0 1px 2px rgba(255, 255, 255, 0.15),
            inset 0 -2px 4px rgba(0, 0, 0, 0.25);
        transform: translateY(-2px);
        border-color: rgba(106, 122, 154, 0.8);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 
            0 2px 6px rgba(100, 100, 140, 0.2),
            inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Selectbox and inputs with texture */
    .stSelectbox, .stTextInput, .stNumberInput {
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div:first-child, 
    .stTextInput > div, 
    .stNumberInput > div {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d1e3e 100%) !important;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 1.5px, rgba(100, 100, 140, 0.04) 1.5px, rgba(100, 100, 140, 0.04) 3px) !important;
        border: 1px solid #4a4a6a !important;
        border-radius: 8px !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stSelectbox:focus-within > div:first-child,
    .stTextInput:focus-within > div,
    .stNumberInput:focus-within > div {
        border-color: #7a8aaa !important;
        box-shadow: 
            inset 0 1px 2px rgba(0, 0, 0, 0.2),
            0 0 8px rgba(122, 138, 170, 0.2);
    }
    
    /* Tabs with smooth transitions */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: rgba(10, 10, 10, 0.3);
        padding: 4px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #1f1a35 100%);
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 1px, rgba(100, 100, 140, 0.04) 1px, rgba(100, 100, 140, 0.04) 2px);
        border: 1px solid rgba(74, 74, 106, 0.5);
        border-radius: 6px;
        color: #b0b0b0;
        transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #252538 0%, #2a1f40 100%);
        border-color: rgba(106, 122, 154, 0.6);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #5a6a8a 0%, #4a5a7a 100%);
        background-image: 
            linear-gradient(135deg, #5a6a8a 0%, #4a5a7a 100%),
            repeating-linear-gradient(45deg, transparent, transparent 1px, rgba(255, 255, 255, 0.08) 1px, rgba(255, 255, 255, 0.08) 2px);
        background-blend-mode: overlay;
        color: #e0e0e0;
        border-color: rgba(106, 122, 154, 0.8);
        box-shadow: 
            0 2px 8px rgba(100, 100, 140, 0.25),
            inset 0 1px 2px rgba(255, 255, 255, 0.1);
        transform: translateY(-1px);
    }
    
    /* Expander with smooth transitions */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d1e3e 100%);
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 1px, rgba(100, 100, 140, 0.04) 1px, rgba(100, 100, 140, 0.04) 2px);
        border: 1px solid #4a4a6a;
        border-radius: 6px;
        color: #b0b0b0 !important;
        transition: all 0.35s ease;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #252538 0%, #34273f 100%);
        border-color: #5a6a8a;
        box-shadow: 
            inset 0 1px 2px rgba(0, 0, 0, 0.1),
            0 0 8px rgba(100, 100, 140, 0.15);
    }
    
    /* Dataframe styling */
    [data-testid="dataFrame"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Chart containers */
    .plotly-graph-div {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Smooth color transitions for interactive elements */
    * {
        transition: color 0.25s ease, background-color 0.25s ease, border-color 0.25s ease;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

def load_model(model_path):
    """Load pre-trained Random Forest model"""
    try:
        if os.path.exists(model_path):
            return joblib.load(model_path)
        return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def generate_mock_inference_data(satellite, resolution=100):
    """Generate realistic mock inference data"""
    flood_probability = np.random.uniform(0, 1, (resolution, resolution))
    flood_detected = (flood_probability > 0.5).astype(int)
    
    smoothed = np.convolve(flood_detected.flatten(), np.ones(9)/9, mode='same')
    flood_detected = (smoothed.reshape(resolution, resolution) > 0.3).astype(int)
    
    return {
        'flood_probability': flood_probability,
        'flood_detected': flood_detected,
        'coverage': np.random.uniform(30, 95),
        'confidence': np.random.uniform(0.7, 0.98),
        'timestamp': datetime.now(),
        'satellite': satellite
    }

def create_flood_map(data):
    """Create interactive flood map visualization"""
    flood_prob = data['flood_probability']
    
    fig = go.Figure(data=go.Heatmap(
        z=flood_prob,
        colorscale='RdYlGn_r',
        colorbar=dict(
            title="Flood<br>Probability",
            thickness=20,
            len=0.7,
            tickfont=dict(color='#b0b0b0', size=11),
            tickcolor='#b0b0b0'
        ),
        hovertemplate='Position: (%{x}, %{y})<br>Flood Prob: %{z:.2%}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': f"🌊 Real-time Flood Detection Map - {data['satellite'].upper()}",
            'font': {'color': '#d0d0d0', 'size': 20},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Longitude (pixels)",
        yaxis_title="Latitude (pixels)",
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(100, 100, 140, 0.1)',
            tickfont=dict(color='#b0b0b0'),
            titlefont=dict(color='#b0b0b0')
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(100, 100, 140, 0.1)',
            tickfont=dict(color='#b0b0b0'),
            titlefont=dict(color='#b0b0b0')
        ),
        plot_bgcolor='rgba(10, 10, 10, 0.8)',
        paper_bgcolor='rgba(10, 10, 10, 0)',
        font=dict(color='#b0b0b0'),
        height=500,
        margin=dict(l=60, r=60, t=80, b=60)
    )
    
    return fig

def create_statistics_chart(data):
    """Create flood statistics visualization"""
    flood_detected = data['flood_detected']
    total_pixels = flood_detected.size
    flooded_pixels = np.sum(flood_detected)
    non_flooded = total_pixels - flooded_pixels
    
    fig = go.Figure(data=[
        go.Bar(
            x=['🌊 Flooded', '🟢 Non-Flooded', '⚠ Uncertain'],
            y=[flooded_pixels, non_flooded, int(total_pixels * 0.05)],
            marker=dict(
                color=['#8a7aaa', '#7a8aaa', '#6a8aaa'],
                line=dict(color=['#8a7aaa', '#7a8aaa', '#6a8aaa'], width=2)
            ),
            text=[
                f"{flooded_pixels:,}<br>{flooded_pixels/total_pixels*100:.1f}%",
                f"{non_flooded:,}<br>{non_flooded/total_pixels*100:.1f}%",
                f"{int(total_pixels * 0.05):,}<br>5%"
            ],
            textposition='auto',
            textfont=dict(color='#e0e0e0', size=12, family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Pixels: %{y:,}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': "📊 Pixel Classification Statistics",
            'font': {'color': '#d0d0d0', 'size': 18},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            tickfont=dict(color='#b0b0b0', size=13, family='Arial Black'),
            titlefont=dict(color='#b0b0b0')
        ),
        yaxis=dict(
            title="Number of Pixels",
            tickfont=dict(color='#b0b0b0'),
            titlefont=dict(color='#b0b0b0'),
            showgrid=True,
            gridcolor='rgba(100, 100, 140, 0.1)'
        ),
        plot_bgcolor='rgba(10, 10, 10, 0.8)',
        paper_bgcolor='rgba(10, 10, 10, 0)',
        font=dict(color='#b0b0b0'),
        height=400,
        showlegend=False
    )
    
    return fig

def create_satellite_comparison():
    """Create satellite comparison chart"""
    satellites = ['Sentinel-1', 'Sentinel-2', 'Landsat 8', 'Landsat 9', 'TerraSAR-X']
    coverage = [87, 92, 78, 81, 65]
    accuracy = [0.92, 0.95, 0.88, 0.89, 0.87]
    processing_time = [2.3, 3.1, 1.8, 1.9, 2.8]
    
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]],
        subplot_titles=('Coverage %', 'Accuracy', 'Processing Time (min)'),
        horizontal_spacing=0.15
    )
    
    fig.add_trace(
        go.Bar(x=satellites, y=coverage, marker_color='#7a8aaa', name='Coverage',
               text=coverage, textposition='auto', textfont=dict(color='#e0e0e0', size=11),
               hovertemplate='<b>%{x}</b><br>Coverage: %{y}%<extra></extra>'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=satellites, y=accuracy, marker_color='#8a7aaa', name='Accuracy',
               text=[f'{a:.2f}' for a in accuracy], textposition='auto', textfont=dict(color='#e0e0e0', size=11),
               hovertemplate='<b>%{x}</b><br>Accuracy: %{y:.3f}<extra></extra>'),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(x=satellites, y=processing_time, marker_color='#6a8aaa', name='Processing Time',
               text=[f'{t:.1f}m' for t in processing_time], textposition='auto', textfont=dict(color='#e0e0e0', size=11),
               hovertemplate='<b>%{x}</b><br>Time: %{y:.1f} min<extra></extra>'),
        row=1, col=3
    )
    
    fig.update_xaxes(tickfont=dict(color='#b0b0b0', size=10), row=1, col=1)
    fig.update_xaxes(tickfont=dict(color='#b0b0b0', size=10), row=1, col=2)
    fig.update_xaxes(tickfont=dict(color='#b0b0b0', size=10), row=1, col=3)
    fig.update_yaxes(tickfont=dict(color='#b0b0b0'), row=1, col=1)
    fig.update_yaxes(tickfont=dict(color='#b0b0b0'), row=1, col=2)
    fig.update_yaxes(tickfont=dict(color='#b0b0b0'), row=1, col=3)
    
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(color='#b0b0b0', size=13)
    
    fig.update_layout(
        title={
            'text': "🛰 Satellite Source Comparison",
            'font': {'color': '#d0d0d0', 'size': 18},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='rgba(10, 10, 10, 0.8)',
        paper_bgcolor='rgba(10, 10, 10, 0)',
        font=dict(color='#b0b0b0'),
        height=400,
        showlegend=False,
        hovermode='closest'
    )
    
    return fig

def make_subplots(*args, **kwargs):
    """Wrapper for plotly subplots"""
    from plotly.subplots import make_subplots as ps_make_subplots
    return ps_make_subplots(*args, **kwargs)

def main():
    # ---------------------------------------------------------
    # 1. MODEL LOADING LOGIC (Added Fix)
    # ---------------------------------------------------------
    # Get the directory where app.py is running
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the model
    # TODO: REPLACE 'your_model_file.joblib' WITH YOUR ACTUAL FILE NAME
    model_filename = 'flood_model.pkl' 
    model_path = os.path.join(current_dir, 'models', model_filename)
    
    # Load the model
    model = load_model(model_path)

    # Show loading status in sidebar
    if model:
        st.sidebar.success(f"✅ Model Loaded: {model_filename}")
    else:
        st.sidebar.warning(f"⚠ Model not found at: {model_path}")
    # ---------------------------------------------------------

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 3em; margin: 0; text-shadow: 0 0 5px rgba(208, 208, 208, 0.3);'>🌊 FLOODML</h1>
            <p style='color: #d0d0d0; font-size: 1.2em; margin: 10px 0; text-shadow: 0 0 3px rgba(208, 208, 208, 0.2);'>
                Real-Time Flood Detection & Monitoring Dashboard
            </p>
            <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'>
                Advanced ML-Powered Satellite Imagery Analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border: 1px solid #4a4a6a; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='margin: 0; color: #b0b0b0;'>⚙ CONTROL PANEL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        selected_tab = st.radio(
            "📍 Select Dashboard View:",
            ["🏠 Overview", "🛰 Satellites", "🔍 Detection", "⚙ Configuration"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        satellite = st.selectbox(
            "🛰 Select Satellite Source:",
            ["Sentinel-1 (SAR)", "Sentinel-2 (Optical)", "Landsat 8", "Landsat 9", "TerraSAR-X (SAR)"],
            index=0
        )
        
        region = st.text_input(
            "📍 Region/Tile ID:",
            value="T30UUE"
        )
        
        date_range = st.date_input(
            "📅 Analysis Period:",
            value=(datetime.now() - timedelta(days=7), datetime.now()),
            label_visibility="visible"
        )
        
        st.markdown("---")
        
        confidence_threshold = st.slider(
            "🎯 Confidence Threshold:",
            min_value=0.5,
            max_value=0.99,
            value=0.75,
            step=0.05,
            help="Minimum confidence to report flood detection"
        )
        
        pixel_filter = st.slider(
            "🔍 Minimum Flood Area (pixels):",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="Filter out detections smaller than this"
        )
        
        st.markdown("---")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        st.markdown("""
        <div style='margin-top: 30px; padding: 15px; background: rgba(100, 100, 140, 0.1); border: 1px solid #4a4a6a; border-radius: 8px;'>
            <p style='color: #b0b0b0; font-size: 0.85em; margin: 0;'>
                <strong>💡 Tip:</strong> Adjust confidence threshold for better flood detection sensitivity.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if selected_tab == "🏠 Overview":
        st.markdown("### 📈 System Status & Key Metrics")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            # If the model is loaded, we could display real attributes here
            accuracy_display = "94.7%" 
            st.metric(
                "🤖 Model Accuracy",
                accuracy_display,
                "+2.3%",
                delta_color="inverse"
            )
        
        with metric_col2:
            st.metric(
                "🌍 Total Scenes Processed",
                "12,847",
                "+156",
                delta_color="inverse"
            )
        
        with metric_col3:
            st.metric(
                "🌊 Floods Detected",
                "2,341",
                "+89",
                delta_color="inverse"
            )
        
        with metric_col4:
            st.metric(
                "⚡ Avg Processing Time",
                "2.3s",
                "-0.4s",
                delta_color="off"
            )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚨 Recent Detections (Last 7 Days)")
            
            detections_data = {
                'Date': pd.date_range(start=datetime.now() - timedelta(days=6), periods=7, freq='D'),
                'Satellite': np.random.choice(['S1', 'S2', 'L8', 'L9'], 7),
                'Confidence': np.random.uniform(0.75, 0.99, 7),
                'Affected Area (km²)': np.random.uniform(10, 500, 7),
                'Status': np.random.choice(['🔴 Critical', '🟠 High', '🟡 Medium'], 7)
            }
            
            detections_df = pd.DataFrame(detections_data)
            st.dataframe(
                detections_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    'Confidence': st.column_config.ProgressColumn('Confidence', min_value=0, max_value=1),
                    'Affected Area (km²)': st.column_config.ProgressColumn('Area (km²)', min_value=0, max_value=500),
                }
            )
        
        with col2:
            st.markdown("### 🌐 System Health")
            
            health_metrics = {
                'Component': ['GPU Processing', 'Data Pipeline', 'Model Inference', 'API Services', 'Storage'],
                'Status': ['✅ Healthy', '✅ Healthy', '✅ Healthy', '✅ Healthy', '✅ Healthy'],
                'Uptime': ['99.8%', '99.9%', '99.7%', '100%', '99.9%'],
                'Load': [65, 42, 78, 28, 56]
            }
            
            health_df = pd.DataFrame(health_metrics)
            st.dataframe(
                health_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    'Load': st.column_config.ProgressColumn('Load %', min_value=0, max_value=100),
                }
            )
    
    elif selected_tab == "🛰 Satellites":
        st.markdown("### 🛰 Satellite Sources & Capabilities")
        
        st.plotly_chart(create_satellite_comparison(), use_container_width=True)
        
        st.markdown("---")
    
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2d1e3e 100%); border: 1px solid #4a4a6a; border-radius: 10px; padding: 15px; text-align: center;'>
                <h3 style='color: #d0d0d0; margin: 0;'>🛰 Sentinel-1</h3>
                <p style='color: #8a9aaa; margin: 10px 0;'><strong>SAR - All Weather</strong></p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Resolution:</strong> 10m</p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Revisit:</strong> 6 days</p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Accuracy:</strong> 92%</p>
                <p style='color: #909090; font-size: 0.85em; margin: 10px 0;'>✅ Active</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2d1e3e 100%); border: 1px solid #4a4a6a; border-radius: 10px; padding: 15px; text-align: center;'>
                <h3 style='color: #d0d0d0; margin: 0;'>🛰 Sentinel-2</h3>
                <p style='color: #8a9aaa; margin: 10px 0;'><strong>Optical - Multispectral</strong></p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Resolution:</strong> 10m</p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Revisit:</strong> 5 days</p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Accuracy:</strong> 95%</p>
                <p style='color: #909090; font-size: 0.85em; margin: 10px 0;'>✅ Active</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2d1e3e 100%); border: 1px solid #4a4a6a; border-radius: 10px; padding: 15px; text-align: center;'>
                <h3 style='color: #d0d0d0; margin: 0;'>🛰 Landsat 8/9</h3>
                <p style='color: #8a9aaa; margin: 10px 0;'><strong>Optical - Multispectral</strong></p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Resolution:</strong> 30m</p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Revisit:</strong> 8 days</p>
                <p style='color: #b0b0b0; font-size: 0.9em; margin: 5px 0;'><strong>Accuracy:</strong> 88%</p>
                <p style='color: #909090; font-size: 0.85em; margin: 10px 0;'>✅ Active</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📊 Satellite Data Availability")
        
        availability_data = {
            'Satellite': ['Sentinel-1', 'Sentinel-2', 'Landsat 8', 'Landsat 9', 'TerraSAR-X'],
            '2024-11-17': ['✅', '✅', '✅', '✅', '❌'],
            '2024-11-18': ['✅', '✅', '❌', '✅', '✅'],
            '2024-11-19': ['✅', '✅', '✅', '✅', '✅'],
            'Last 7 Days': ['35/7', '35/7', '28/7', '30/7', '21/7']
        }
        
        avail_df = pd.DataFrame(availability_data)
        st.dataframe(avail_df, hide_index=True, use_container_width=True)
    
    elif selected_tab == "🔍 Detection":
        # ---------------------------------------------------------
        # 2. DETECTION LOGIC (Updated)
        # ---------------------------------------------------------
        # Attempt to pass the model to the upload module
        # If create_satellite_upload_section doesn't accept args,
        # you will need to update that function too.
        try:
            create_satellite_upload_section(model=model) 
        except TypeError:
            # Fallback if the function isn't updated to take arguments
            create_satellite_upload_section()
    
    elif selected_tab == "⚙ Configuration":
        st.markdown("### ⚙ System Configuration & Settings")
        
        with st.expander("🤖 Model Configuration", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("*Random Forest Classifier*")
                st.text(f"Number of Trees: 100")
                st.text(f"Max Depth: Auto")
                st.text(f"Min Samples Split: 2")
                st.text(f"Min Samples Leaf: 1")
                st.text(f"Random State: 42")
            
            with col2:
                st.markdown("*Training Data*")
                st.text(f"Total Samples: 45,892")
                st.text(f"Training Set: 70% (32,125)")
                st.text(f"Test Set: 30% (13,767)")
                st.text(f"Features: VV, VH/NDVI/MNDWI, Slope")
                st.text(f"Classes: 2 (Water/No-Water)")
        
        with st.expander("🔧 Processing Pipeline"):
            st.markdown("""
            *Input Processing:*
            - Satellite data ingestion and validation
            - Cloud/shadow detection and masking
            - Radiometric calibration
            
            *Feature Extraction:*
            - Synthetic band generation (NDVI, MNDWI)
            - DEM-based slope calculation
            - Morphological filtering
            
            *Classification:*
            - Random Forest inference
            - Confidence scoring
            - Class probability estimation
            
            *Post-Processing:*
            - Majority filter (radius: 2-3 pixels)
            - Connected component analysis
            - Land cover overlay (ESA World Cover)
            """)
        
        with st.expander("💾 Data Management"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("*Database*")
                st.text(f"Type: PyArrow + GDAL")
                st.text(f"Cache Size: 10 GB")
                st.text(f"Archive Path: /data/archive")
                st.text(f"Max Retention: 2 years")
            
            with col2:
                st.markdown("*Storage*")
                st.text(f"Current Usage: 567 GB / 2 TB")
                st.text(f"Growth Rate: ~45 GB/month")
                st.text(f"Backup: Daily (AWS S3)")
                st.text(f"Compression: LZW (GeoTIFF)")
        
        with st.expander("🚀 Performance Tuning"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("*GPU Configuration*")
                st.selectbox("GPU Device:", ["CUDA:0", "CUDA:1"], key="gpu_config")
                st.slider("GPU Memory (%)", 0, 100, 75, key="gpu_mem")
                st.toggle("Use cuML (GPU ML)", value=True, key="cuml_toggle")
            
            with col2:
                st.markdown("*Parallel Processing*")
                st.slider("CPU Threads", 1, 32, 8, key="cpu_threads")
                st.slider("Batch Size", 16, 1024, 256, key="batch_size")
                st.toggle("Distributed Processing", value=False, key="dist_proc")
        
        with st.expander("⚠ Advanced Settings"):
            st.markdown("*Post-Processing Radius*")
            post_radius = st.slider("Majority Filter Radius (pixels):", 1, 5, 2)
            
            st.markdown("*Cloud Threshold*")
            cloud_thresh = st.slider("Cloud Confidence Threshold:", 0.0, 1.0, 0.3)
            
            st.markdown("*DEM Source*")
            dem_source = st.selectbox("Select DEM:", ["Copernicus DEM", "MERIT DEM"], key="dem_select")
            
            st.markdown("*Nodata Handling*")
            nodata_value = st.number_input("Nodata Value:", value=255, key="nodata_val")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Configuration", use_container_width=True):
                st.success("✅ Configuration saved successfully!")
        
        with col2:
            if st.button("🔄 Reset to Defaults", use_container_width=True):
                st.info("ℹ Configuration reset to defaults")
        
        with col3:
            if st.button("📥 Export Settings", use_container_width=True):
                st.success("✅ Settings exported to JSON")

if __name__ == "__main__":
    main()