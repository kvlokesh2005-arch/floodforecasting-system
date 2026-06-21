import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
from PIL import Image
import io

def get_risk_level(flood_probability, proximity_score=0.5):
    """
    Determine risk level based on flood probability and population proximity.
    
    Args:
        flood_probability: Float between 0-1 representing flood detection probability
        proximity_score: Float between 0-1 where 1 = near populated areas, 0 = remote
    
    Returns:
        Tuple of (risk_level, risk_color, action_required)
    """
    combined_score = (flood_probability * 0.7) + (proximity_score * 0.3)
    
    if combined_score < 0.25:
        return "Low", "#00ff88", False
    elif combined_score < 0.5:
        return "Medium", "#ffff00", False
    elif combined_score < 0.75:
        return "High", "#ff6600", True
    else:
        return "Immediate Action", "#ff0080", True

def create_flood_probability_map(flood_probability, scene_name):
    """Create flood probability heatmap with professional colors."""
    
    h, w = flood_probability.shape
    y = np.arange(h)
    x = np.arange(w)
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=flood_probability,
        x=x,
        y=y,
        colorscale=[
            [0.0, '#1a472a'],         # Very low - dark blue-green
            [0.2, '#2e7d4e'],         # Low - green
            [0.4, '#ffc658'],         # Medium-low - light orange
            [0.6, '#ff9800'],         # Medium - orange
            [0.8, '#f44336'],         # High - red
            [1.0, '#c41c3b']          # Critical - deep red
        ],
        colorbar=dict(
            title="Probability",
            thickness=20,
            len=0.7,
            x=1.02
        ),
        hovertemplate='<b>Position</b><br>X: %{x}<br>Y: %{y}<br><b>Probability: %{z:.1%}</b><extra></extra>',
        name='Flood Probability'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>Flood Probability Map</b><br><span style='font-size:12px'>{scene_name}</span>",
            x=0.5,
            xanchor='center',
            font=dict(color='#2c3e50', size=18)
        ),
        xaxis_title="X Coordinate (pixels)",
        yaxis_title="Y Coordinate (pixels)",
        width=900,
        height=700,
        template='plotly_white',
        hovermode='closest',
        paper_bgcolor='#f8f9fa',
        plot_bgcolor='#ffffff',
        font=dict(color='#2c3e50', size=11),
        xaxis=dict(gridcolor='#e0e0e0'),
        yaxis=dict(gridcolor='#e0e0e0'),
        margin=dict(l=70, r=120, t=100, b=70)
    )
    
    return fig

def create_risk_classification_map(flood_probability, scene_name):
    """Create risk classification map showing 4 risk levels."""
    
    h, w = flood_probability.shape
    risk_map = np.zeros_like(flood_probability)
    
    risk_map[flood_probability < 0.25] = 0      # Low
    risk_map[(flood_probability >= 0.25) & (flood_probability < 0.5)] = 1   # Medium
    risk_map[(flood_probability >= 0.5) & (flood_probability < 0.75)] = 2   # High
    risk_map[flood_probability >= 0.75] = 3     # Critical
    
    y = np.arange(h)
    x = np.arange(w)
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=risk_map,
        x=x,
        y=y,
        colorscale=[
            [0.0, '#4caf50'],         # Green - Low
            [0.33, '#ffc107'],        # Amber - Medium
            [0.67, '#ff9800'],        # Orange - High
            [1.0, '#f44336']          # Red - Critical
        ],
        colorbar=dict(
            title="Risk Level",
            tickvals=[0.125, 0.375, 0.625, 0.875],
            ticktext=['Low', 'Medium', 'High', 'Critical'],
            thickness=20,
            len=0.7,
            x=1.02
        ),
        hovertemplate='<b>Position</b><br>X: %{x}<br>Y: %{y}<br><b>Probability: </b>%{customdata:.1%}<extra></extra>',
        customdata=flood_probability,
        name='Risk Level'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>Risk Classification Map</b><br><span style='font-size:12px'>{scene_name}</span>",
            x=0.5,
            xanchor='center',
            font=dict(color='#2c3e50', size=18)
        ),
        xaxis_title="X Coordinate (pixels)",
        yaxis_title="Y Coordinate (pixels)",
        width=900,
        height=700,
        template='plotly_white',
        hovermode='closest',
        paper_bgcolor='#f8f9fa',
        plot_bgcolor='#ffffff',
        font=dict(color='#2c3e50', size=11),
        xaxis=dict(gridcolor='#e0e0e0'),
        yaxis=dict(gridcolor='#e0e0e0'),
        margin=dict(l=70, r=120, t=100, b=70)
    )
    
    return fig

def create_input_satellite_map(input_data, scene_name):
    """Create greyscale visualization of input satellite data."""
    
    h, w = input_data.shape
    y = np.arange(h)
    x = np.arange(w)
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=input_data,
        x=x,
        y=y,
        colorscale='Greys',
        colorbar=dict(
            title="Intensity",
            thickness=20,
            len=0.7,
            x=1.02
        ),
        hovertemplate='<b>Position</b><br>X: %{x}<br>Y: %{y}<br><b>Intensity: %{z:.2f}</b><extra></extra>',
        name='Input Data'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>Input Satellite Data</b><br><span style='font-size:12px'>{scene_name}</span>",
            x=0.5,
            xanchor='center',
            font=dict(color='#2c3e50', size=18)
        ),
        xaxis_title="X Coordinate (pixels)",
        yaxis_title="Y Coordinate (pixels)",
        width=900,
        height=700,
        template='plotly_white',
        hovermode='closest',
        paper_bgcolor='#f8f9fa',
        plot_bgcolor='#ffffff',
        font=dict(color='#2c3e50', size=11),
        xaxis=dict(gridcolor='#e0e0e0'),
        yaxis=dict(gridcolor='#e0e0e0'),
        margin=dict(l=70, r=120, t=100, b=70)
    )
    
    return fig

def create_risk_summary_card(flood_prob, proximity, scene_name):
    """Create a risk assessment summary card."""
    
    risk_level, risk_color, action_required = get_risk_level(flood_prob, proximity)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "**Flood Detection**",
            f"{flood_prob*100:.1f}%",
            delta="Increasing" if flood_prob > 0.5 else "Normal",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "**Population Proximity**",
            f"{proximity*100:.0f}%",
            delta="Near Populated Areas" if proximity > 0.5 else "Remote"
        )
    
    with col3:
        risk_emoji = "🔴" if action_required else ("🟠" if risk_level == "High" else ("🟡" if risk_level == "Medium" else "🟢"))
        st.metric(
            "**Risk Level**",
            f"{risk_emoji} {risk_level}",
            delta="Action Required" if action_required else "Monitor"
        )
    
    with col4:
        st.metric(
            "**Scene**",
            scene_name.split('.')[0][-8:],
            delta="Status: Active"
        )

def create_satellite_upload_section():
    """Main satellite flood detection section."""
    
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 10px;'>🔍 Flood Detection & Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px; margin-top: 0;'>Upload satellite imagery for real-time flood detection and risk assessment</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    with st.expander("📤 Upload & Configure", expanded=True):
        st.markdown("<p style='color: #555; margin-top: 0;'>Select satellite data and configure detection parameters</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div style='background: #f0f4ff; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;'>", unsafe_allow_html=True)
            st.markdown("**🛰️ Sentinel-1 SAR Data**")
            st.markdown("<span style='font-size: 12px; color: #666;'>VV/VH polarization bands (C-band)</span>", unsafe_allow_html=True)
            s1_files = st.file_uploader(
                "Select S1 files",
                type=['tif', 'TIF', 'tiff', 'TIFF', 'jp2', 'JP2', 'nc'],
                accept_multiple_files=True,
                key="s1_upload"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='background: #f0fff4; padding: 15px; border-radius: 8px; border-left: 4px solid #27ae60;'>", unsafe_allow_html=True)
            st.markdown("**🌈 Sentinel-2 Optical Data**")
            st.markdown("<span style='font-size: 12px; color: #666;'>NDVI, MNDWI multispectral bands</span>", unsafe_allow_html=True)
            s2_files = st.file_uploader(
                "Select S2 files",
                type=['tif', 'TIF', 'tiff', 'TIFF', 'jp2', 'JP2', 'nc'],
                accept_multiple_files=True,
                key="s2_upload"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**⚙️ Detection Parameters**")
        
        col1, col2 = st.columns(2)
        with col1:
            proximity_source = st.selectbox(
                "Population Data Source",
                ["Worldpop", "GHSL", "None (auto-estimate)"],
                help="Select source for population proximity analysis"
            )
        
        with col2:
            confidence_threshold = st.slider(
                "Detection Sensitivity",
                0.3, 1.0, 0.5, 0.05,
                help="0.3 (max sensitive) → 0.5 (balanced) → 0.8 (specific)"
            )
        
        process_btn = st.button("▶️ Analyze Satellite Data", use_container_width=True, type="primary", key="process_detect")
        
    if process_btn and (s1_files or s2_files):
        st.success("✅ Files selected for processing")
        
        # Process each uploaded file
        for uploaded_file in (s1_files or []) + (s2_files or []):
            st.markdown(f"#### 📋 Processing: {uploaded_file.name}")
            
            # Simulate model inference
            progress_bar = st.progress(0)
            
            # Simulate data processing
            progress_bar.progress(25)
            st.write("Loading satellite data...")
            
            # Generate mock input data and inference data
            resolution = np.random.randint(64, 256)
            input_data = np.random.uniform(0, 1, (resolution, resolution))
            flood_probability = np.random.uniform(0, 1, (resolution, resolution))
            
            # Apply some structure to make it more realistic
            y, x = np.ogrid[:resolution, :resolution]
            flood_probability *= (1 + 0.3 * np.sin(y/50) * np.cos(x/50))
            flood_probability = np.clip(flood_probability, 0, 1)
            
            progress_bar.progress(50)
            st.write("Running model inference...")
            
            # Determine proximity score based on scene name or manual input
            if "urban" in uploaded_file.name.lower():
                proximity_score = 0.8
            elif "coastal" in uploaded_file.name.lower():
                proximity_score = 0.6
            else:
                proximity_score = np.random.uniform(0.2, 0.8)
            
            progress_bar.progress(75)
            
            # Get risk assessment
            avg_flood_prob = np.mean(flood_probability)
            risk_level, risk_color, action_required = get_risk_level(avg_flood_prob, proximity_score)
            
            progress_bar.progress(100)
            st.write("Analysis complete!")
            
            # Display risk summary
            st.markdown("#### 📊 Risk Assessment Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            risk_level, risk_color, action_required = get_risk_level(avg_flood_prob, proximity_score)
            
            with col1:
                st.metric("Flood Probability", f"{avg_flood_prob*100:.1f}%", 
                         delta="High Risk" if avg_flood_prob > 0.5 else "Normal")
            with col2:
                st.metric("Population Proximity", f"{proximity_score*100:.0f}%",
                         delta="Near Population" if proximity_score > 0.5 else "Remote")
            with col3:
                risk_emoji = "🔴" if action_required else ("🟠" if risk_level == "High" else ("🟡" if risk_level == "Medium" else "🟢"))
                st.metric("Risk Level", f"{risk_emoji} {risk_level}", delta="Action Required" if action_required else "Monitor")
            with col4:
                st.metric("Coverage Area", f"{(np.sum(flood_probability > 0.5) / flood_probability.size * 100):.1f}%")
            
            st.markdown("---")
            
            st.markdown("#### 📊 Satellite Data Analysis")
            col_input, col_prob = st.columns(2)
            
            with col_input:
                st.markdown("##### 🛰️ Input Satellite Data")
                fig0 = create_input_satellite_map(input_data, uploaded_file.name)
                st.plotly_chart(fig0, use_container_width=True)
            
            with col_prob:
                st.markdown("##### 📈 Flood Probability Map")
                fig1 = create_flood_probability_map(flood_probability, uploaded_file.name)
                st.plotly_chart(fig1, use_container_width=True)
            
            st.markdown("#### 🗺️ Risk Classification Map")
            fig2 = create_risk_classification_map(flood_probability, uploaded_file.name)
            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("---")

if __name__ == "__main__":
    create_satellite_upload_section()
