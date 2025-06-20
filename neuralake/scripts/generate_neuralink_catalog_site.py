#!/usr/bin/env python3
"""
Generate Neuralink-specific Static Catalog Site

This script creates a realistic demonstration of the Neuralake data catalog
with tables that reflect actual Neuralink neural data platform needs.

Based on the architecture described in docs/explanation/neuralake.md:
- High-throughput neural signal ingestion
- Real-time processing for closed-loop control
- Research data analysis workflows
- Clinical trial data management
"""

import sys
from pathlib import Path
import polars as pl
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from catalog_core import default_catalog, register_static_table, table
from ssg import CatalogSiteGenerator

def create_neuralink_tables():
    """Create realistic Neuralink neural data tables."""
    
    # Neural Signal Tables
    @table(
        name="neural_signals",
        description="High-frequency neural signals from N1 chip electrodes",
        tags=["neural-signals", "real-time", "n1-chip", "high-frequency"],
        owner="Neural Engineering Team",
        schema={
            "timestamp_ns": "Int64",
            "chip_id": "Utf8", 
            "electrode_id": "Int32",
            "voltage_uv": "Float32",
            "spike_detected": "Boolean",
            "sample_rate_hz": "Int32",
            "session_id": "Utf8"
        }
    )
    def neural_signals():
        """
        Raw neural signals captured from Neuralink N1 chip electrodes.
        
        This table contains high-frequency (30kHz) neural signal data from 
        individual electrodes on the N1 chip. Each record represents a single
        sample point with microsecond timestamp precision.
        
        Used for:
        - Real-time spike detection
        - Closed-loop motor control
        - Neural decoder training
        - Signal quality monitoring
        """
        return pl.LazyFrame({
            "timestamp_ns": [1234567890123456789],
            "chip_id": ["N1_001"], 
            "electrode_id": [42],
            "voltage_uv": [125.5],
            "spike_detected": [True],
            "sample_rate_hz": [30000],
            "session_id": ["session_20250619_001"]
        })
    
    @table(
        name="spike_events",
        description="Processed spike events extracted from neural signals",
        tags=["spikes", "processed", "motor-control", "real-time"],
        owner="Signal Processing Team",
        schema={
            "timestamp_ns": "Int64",
            "chip_id": "Utf8",
            "electrode_id": "Int32", 
            "spike_amplitude": "Float32",
            "waveform_features": "List(Float32)",
            "classification": "Utf8",
            "confidence": "Float32"
        }
    )
    def spike_events():
        """
        Classified neural spike events for motor intent decoding.
        
        Processed spike data with extracted features and classifications
        used for real-time motor intent prediction and closed-loop control.
        
        Features extracted using Neuralink's custom spike detection algorithms
        optimized for sub-millisecond latency requirements.
        """
        return pl.LazyFrame({
            "timestamp_ns": [1234567890123456789],
            "chip_id": ["N1_001"],
            "electrode_id": [42],
            "spike_amplitude": [250.0],
            "waveform_features": [[1.2, 3.4, 5.6, 2.1]],
            "classification": ["motor_intent"],
            "confidence": [0.92]
        })
    
    @table(
        name="motor_predictions",
        description="Motor intent predictions for closed-loop control",
        tags=["motor-control", "predictions", "closed-loop", "real-time"],
        owner="Machine Learning Team",
        schema={
            "timestamp_ns": "Int64",
            "session_id": "Utf8",
            "intended_movement": "Utf8",
            "velocity_x": "Float32",
            "velocity_y": "Float32", 
            "confidence": "Float32",
            "model_version": "Utf8",
            "latency_ms": "Float32"
        }
    )
    def motor_predictions():
        """
        Real-time motor intent predictions for cursor/robotic control.
        
        Neural decoder output predicting intended movements from spike patterns.
        Used to control external devices like computer cursors, robotic arms,
        or other assistive technologies.
        
        Latency target: <100ms from signal acquisition to prediction output.
        """
        return pl.LazyFrame({
            "timestamp_ns": [1234567890123456789],
            "session_id": ["session_20250619_001"],
            "intended_movement": ["cursor_right"],
            "velocity_x": [15.2],
            "velocity_y": [3.8],
            "confidence": [0.89],
            "model_version": ["v2.1.0"],
            "latency_ms": [85.3]
        })
    
    # Clinical Data Tables
    @table(
        name="patient_sessions",
        description="Patient session metadata and surgical information",
        tags=["clinical", "patients", "surgery", "metadata"],
        owner="Clinical Operations Team",
        schema={
            "patient_id": "Utf8",
            "session_id": "Utf8",
            "surgery_date": "Date",
            "chip_location": "Utf8",
            "surgeon": "Utf8",
            "session_start": "Datetime(time_unit='ns')",
            "session_duration_minutes": "Int32",
            "data_quality_score": "Float32"
        }
    )
    def patient_sessions():
        """
        Clinical session metadata for patient studies and trials.
        
        Tracks implant surgeries, session details, and data quality metrics
        for clinical trial participants. Includes surgical placement information
        and session performance metrics.
        
        HIPAA compliant with de-identified patient data.
        """
        return pl.LazyFrame({
            "patient_id": ["P_001_ANON"],
            "session_id": ["session_20250619_001"],
            "surgery_date": [datetime(2025, 1, 15).date()],
            "chip_location": ["primary_motor_cortex"],
            "surgeon": ["Dr. Smith"],
            "session_start": [datetime(2025, 6, 19, 9, 30, 0)],
            "session_duration_minutes": [120],
            "data_quality_score": [0.95]
        })
    
    # Research Data Tables
    @table(
        name="behavioral_metrics",
        description="Experimental task performance metrics and behavioral data",
        tags=["research", "behavioral", "tasks", "performance"],
        owner="Research Team",
        schema={
            "session_id": "Utf8",
            "task_type": "Utf8",
            "trial_number": "Int32",
            "target_reached": "Boolean",
            "time_to_target_ms": "Float32",
            "accuracy_score": "Float32",
            "difficulty_level": "Int32"
        }
    )
    def behavioral_metrics():
        """
        Task performance and behavioral metrics from research sessions.
        
        Quantitative measures of patient performance during various experimental
        tasks including cursor control, typing, and other motor control paradigms.
        
        Used for:
        - Decoder performance evaluation
        - Clinical efficacy assessment
        - Research outcome analysis
        """
        return pl.LazyFrame({
            "session_id": ["session_20250619_001"],
            "task_type": ["cursor_control"],
            "trial_number": [1],
            "target_reached": [True],
            "time_to_target_ms": [1250.5],
            "accuracy_score": [0.94],
            "difficulty_level": [3]
        })
    
    # System Monitoring Tables  
    @table(
        name="system_telemetry",
        description="Hardware health monitoring and system telemetry",
        tags=["monitoring", "hardware", "telemetry", "alerts"],
        owner="Hardware Engineering Team",
        schema={
            "timestamp": "Datetime(time_unit='ns')",
            "chip_id": "Utf8",
            "battery_level": "Float32",
            "temperature_c": "Float32",
            "wireless_signal_strength": "Float32",
            "electrode_impedance_avg": "Float32",
            "data_throughput_mbps": "Float32",
            "error_count": "Int32"
        }
    )
    def system_telemetry():
        """
        Real-time hardware monitoring and system health metrics.
        
        Continuous monitoring of N1 chip hardware including power management,
        thermal monitoring, wireless connectivity, and electrode health.
        
        Critical for:
        - Patient safety monitoring
        - Predictive maintenance
        - Performance optimization
        - Failure detection
        """
        return pl.LazyFrame({
            "timestamp": [datetime(2025, 6, 19, 10, 30, 0)],
            "chip_id": ["N1_001"],
            "battery_level": [0.87],
            "temperature_c": [37.2],
            "wireless_signal_strength": [-45.0],
            "electrode_impedance_avg": [150.5],
            "data_throughput_mbps": [2.1],
            "error_count": [0]
        })

    # Register static Delta Lake tables (from actual delta_tables.py)
    # Note: Would be actual NeuralakeDeltaTable object in production
    register_static_table(
        table_obj=None,  # Would be NeuralakeDeltaTable("neural_stream_delta")
        name="neural_stream_delta",
        description="High-throughput neural signal streaming data stored in Delta Lake format",
        tags=["delta", "streaming", "neural-signals", "production"],
        owner="Data Engineering Team",
        schema={
            "timestamp": "Datetime(time_unit='ns')",
            "device_id": "Utf8", 
            "channel": "Int32",
            "voltage": "Float64",
            "quality_score": "Float64",
            "session_id": "Utf8",
            "patient_id": "Utf8"
        }
    )

def main():
    """Generate the Neuralink-specific catalog site."""
    print("🧠 Generating Neuralink Neural Data Catalog Site...")
    
    # Create all the demo tables
    create_neuralink_tables()
    
    # Export catalog metadata
    catalog_metadata = default_catalog.export_catalog_metadata()
    
    # Generate the static site
    generator = CatalogSiteGenerator(output_dir=Path("neuralink-catalog-site"))
    generator.generate_site(
        catalog_metadata=catalog_metadata,
        project_name="Neuralink Neural Data Catalog"
    )
    
    print("✅ Neuralink catalog site generated successfully!")
    print(f"📂 Location: {Path('neuralink-catalog-site').absolute()}")
    print(f"🌐 Open: file://{Path('neuralink-catalog-site').absolute()}/index.html")

if __name__ == "__main__":
    main() 