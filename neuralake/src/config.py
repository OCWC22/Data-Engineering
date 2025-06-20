"""
Production-ready configuration management for Neuralake data platform.

This module implements secure, environment-aware configuration management
following data engineering best practices and the Neuralake architecture principles.

Key Features:
- Environment-based configuration (LOCAL, DEVELOPMENT, STAGING, PRODUCTION)
- Secure credential management through environment variables
- Data quality and validation configuration
- Comprehensive logging setup
- Configuration validation and error handling
- Support for both config files and environment-specific settings

Design Philosophy:
- "Systems must scale down to a single developer machine and up to stateless clusters"
- Security by default with no hardcoded credentials
- Fail-fast configuration validation
- Observability through structured logging
"""

import os
import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import warnings


class Environment(Enum):
    """Supported deployment environments."""
    LOCAL = "local"
    DEVELOPMENT = "development" 
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(Enum):
    """Supported logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class S3Config:
    """S3 configuration with security best practices."""
    
    # Connection settings
    endpoint_url: Optional[str] = None
    region: str = "us-west-2"
    
    # Security settings
    allow_http: bool = False
    allow_unsafe_rename: bool = False
    
    # Performance settings
    max_connections: int = 100
    connect_timeout: int = 60
    read_timeout: int = 60
    
    # Retry configuration
    max_retries: int = 3
    retry_mode: str = "adaptive"
    
    def get_storage_options(self) -> Dict[str, str]:
        """Get storage options for data engines (polars, delta-rs, etc.)."""
        options = {}
        
        # Credentials from environment variables only
        if os.getenv("AWS_ACCESS_KEY_ID"):
            options["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
        if os.getenv("AWS_SECRET_ACCESS_KEY"):
            options["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
        if os.getenv("AWS_SESSION_TOKEN"):
            options["AWS_SESSION_TOKEN"] = os.getenv("AWS_SESSION_TOKEN")
            
        # Connection settings
        if self.endpoint_url:
            options["AWS_ENDPOINT_URL"] = self.endpoint_url
        options["AWS_REGION"] = self.region
        
        # Security settings (only for local development)
        if self.allow_http:
            options["AWS_ALLOW_HTTP"] = "true"
        if self.allow_unsafe_rename:
            options["AWS_S3_ALLOW_UNSAFE_RENAME"] = "true"
            
        # Performance settings
        options["AWS_MAX_CONNECTIONS"] = str(self.max_connections)
        options["AWS_CONNECT_TIMEOUT"] = str(self.connect_timeout)
        options["AWS_READ_TIMEOUT"] = str(self.read_timeout)
        options["AWS_MAX_RETRIES"] = str(self.max_retries)
        options["AWS_RETRY_MODE"] = self.retry_mode
        
        return options
    
    def validate(self, environment: Environment) -> None:
        """Validate S3 configuration for the given environment."""
        if environment == Environment.PRODUCTION:
            if self.allow_http:
                raise ValueError("HTTP connections not allowed in production")
            if self.allow_unsafe_rename:
                raise ValueError("Unsafe S3 rename not allowed in production")
            if self.endpoint_url and "localhost" in self.endpoint_url:
                raise ValueError("Localhost endpoints not allowed in production")


@dataclass 
class DataQualityConfig:
    """Data quality and validation configuration."""
    
    # Schema validation
    enforce_schema: bool = True
    allow_schema_evolution: bool = True
    strict_column_types: bool = True
    
    # Data validation
    validate_on_read: bool = True
    validate_on_write: bool = True
    null_value_threshold: float = 0.1  # Maximum allowed null percentage
    
    # Data freshness
    max_staleness_hours: int = 24
    freshness_check_enabled: bool = True
    
    # Quality checks
    enable_duplicate_detection: bool = True
    enable_outlier_detection: bool = False
    outlier_detection_method: str = "iqr"  # iqr, zscore, isolation_forest
    
    # Monitoring
    quality_metrics_enabled: bool = True
    alert_on_quality_degradation: bool = True
    quality_threshold: float = 0.95  # Minimum acceptable quality score


@dataclass
class PartitioningConfig:
    """Table partitioning configuration."""
    
    # Default partitioning strategies
    time_column: str = "created_at"
    partition_granularity: str = "day"  # hour, day, month, year
    
    # Partition management
    auto_partition: bool = True
    max_partitions_per_table: int = 1000
    partition_pruning_enabled: bool = True
    
    # Compaction settings
    auto_compaction: bool = True
    compaction_trigger_files: int = 10
    compaction_schedule: str = "0 2 * * *"  # Daily at 2 AM


@dataclass
class LoggingConfig:
    """Logging configuration following observability best practices."""
    
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Structured logging
    enable_json_logging: bool = False
    include_trace_id: bool = True
    
    # Log destinations
    console_enabled: bool = True
    file_enabled: bool = True
    file_path: Optional[str] = None
    
    # Log rotation
    max_file_size_mb: int = 100
    backup_count: int = 5
    
    # Performance
    async_logging: bool = False
    buffer_size: int = 1000


@dataclass
class SecurityConfig:
    """Security configuration."""
    
    # Encryption
    encrypt_at_rest: bool = True
    encrypt_in_transit: bool = True
    kms_key_id: Optional[str] = None
    
    # Access control
    enable_rbac: bool = True
    require_mfa: bool = False
    
    # Audit logging
    audit_enabled: bool = True
    audit_sensitive_operations: bool = True
    
    # Data privacy
    enable_pii_detection: bool = True
    auto_redact_pii: bool = False


@dataclass
class PerformanceConfig:
    """Performance optimization configuration."""
    
    # Query optimization
    enable_query_cache: bool = True
    cache_ttl_seconds: int = 3600
    max_cache_size_mb: int = 1024
    
    # Parallel processing
    max_worker_threads: int = 0  # 0 = auto-detect CPU cores
    enable_vectorization: bool = True
    
    # Memory management
    max_memory_usage_mb: int = 0  # 0 = auto-detect available memory
    spill_to_disk_threshold: float = 0.8
    
    # I/O optimization
    prefetch_enabled: bool = True
    async_io: bool = True
    io_buffer_size_kb: int = 64


@dataclass
class NeuralakeConfig:
    """Main Neuralake configuration combining all subsystems."""
    
    # Environment
    environment: Environment = Environment.LOCAL
    project_name: str = "neuralake"
    version: str = "0.1.0"
    created_at: datetime = field(default_factory=datetime.now)
    
    # Core configurations
    s3: S3Config = field(default_factory=S3Config)
    data_quality: DataQualityConfig = field(default_factory=DataQualityConfig)
    partitioning: PartitioningConfig = field(default_factory=PartitioningConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # Data locations
    default_bucket: str = "neuralake-data"
    bronze_prefix: str = "bronze"
    silver_prefix: str = "silver"
    gold_prefix: str = "gold"
    
    # Catalog settings
    catalog_name: str = "neuralake_catalog"
    default_database: str = "default"
    
    # Feature flags
    enable_experimental_features: bool = False
    enable_debug_mode: bool = False
    
    def __post_init__(self):
        """Post-initialization validation and setup."""
        self.validate()
        self._setup_logging()
        self._log_configuration_summary()
    
    def validate(self) -> None:
        """Validate the complete configuration."""
        # Validate S3 configuration
        self.s3.validate(self.environment)
        
        # Environment-specific validations
        if self.environment == Environment.PRODUCTION:
            self._validate_production_config()
        elif self.environment == Environment.LOCAL:
            self._validate_local_config()
    
    def _validate_production_config(self) -> None:
        """Validate production-specific requirements."""
        required_env_vars = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY"
        ]
        
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables for production: {missing_vars}")
        
        # Security requirements
        if not self.security.encrypt_at_rest:
            raise ValueError("Encryption at rest is required in production")
        if not self.security.encrypt_in_transit:
            raise ValueError("Encryption in transit is required in production")
        if not self.security.audit_enabled:
            raise ValueError("Audit logging is required in production")
    
    def _validate_local_config(self) -> None:
        """Validate local development configuration."""
        # Warn about local development settings
        if self.s3.allow_http:
            warnings.warn("HTTP connections enabled - only use for local development")
        if self.s3.allow_unsafe_rename:
            warnings.warn("Unsafe S3 rename enabled - only use for local development")
    
    def _setup_logging(self) -> None:
        """Configure logging based on the logging configuration."""
        logger = logging.getLogger("neuralake")
        logger.setLevel(getattr(logging, self.logging.level.value))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Console handler
        if self.logging.console_enabled:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(self.logging.format))
            logger.addHandler(console_handler)
        
        # File handler
        if self.logging.file_enabled:
            log_file = self.logging.file_path or f"{self.project_name}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(self.logging.format))
            logger.addHandler(file_handler)
    
    def _log_configuration_summary(self) -> None:
        """Log a summary of the current configuration."""
        logger = logging.getLogger("neuralake.config")
        logger.info(f"Neuralake configuration loaded for environment: {self.environment.value}")
        logger.info(f"Project: {self.project_name} v{self.version}")
        logger.info(f"S3 endpoint: {self.s3.endpoint_url or 'AWS default'}")
        logger.info(f"Default bucket: {self.default_bucket}")
        logger.info(f"Data quality validation: {'enabled' if self.data_quality.enforce_schema else 'disabled'}")
        logger.info(f"Security features: encryption={'enabled' if self.security.encrypt_at_rest else 'disabled'}")
    
    @classmethod
    def from_environment(cls, env_name: Optional[str] = None) -> 'NeuralakeConfig':
        """Create configuration from environment variables."""
        if env_name is None:
            env_name = os.getenv("NEURALAKE_ENV", "local")
        
        try:
            environment = Environment(env_name.lower())
        except ValueError:
            raise ValueError(f"Invalid environment: {env_name}. Must be one of: {[e.value for e in Environment]}")
        
        # Create base configuration for the environment
        config = cls._create_environment_config(environment)
        
        # Override with environment variables
        config = cls._apply_environment_overrides(config)
        
        return config
    
    @classmethod
    def from_file(cls, config_path: Union[str, Path]) -> 'NeuralakeConfig':
        """Load configuration from a JSON file."""
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            # Convert nested dictionaries to dataclass instances
            return cls._from_dict(config_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    @classmethod
    def _create_environment_config(cls, environment: Environment) -> 'NeuralakeConfig':
        """Create environment-specific default configuration."""
        if environment == Environment.LOCAL:
            return cls(
                environment=environment,
                s3=S3Config(
                    endpoint_url="http://localhost:9000",
                    allow_http=True,
                    allow_unsafe_rename=True,
                    region="us-east-1"  # MinIO default
                ),
                data_quality=DataQualityConfig(
                    enforce_schema=False,  # More lenient for development
                    validate_on_write=False
                ),
                logging=LoggingConfig(level=LogLevel.DEBUG),
                security=SecurityConfig(
                    encrypt_at_rest=False,
                    encrypt_in_transit=False,
                    audit_enabled=False
                ),
                default_bucket="neuralake-bucket",
                enable_debug_mode=True
            )
        
        elif environment == Environment.DEVELOPMENT:
            return cls(
                environment=environment,
                s3=S3Config(
                    region="us-west-2",
                    allow_http=False,
                    allow_unsafe_rename=False
                ),
                data_quality=DataQualityConfig(
                    enforce_schema=True,
                    validate_on_write=True
                ),
                logging=LoggingConfig(level=LogLevel.INFO),
                security=SecurityConfig(
                    encrypt_at_rest=True,
                    encrypt_in_transit=True,
                    audit_enabled=True
                ),
                default_bucket="neuralake-dev"
            )
        
        elif environment == Environment.STAGING:
            return cls(
                environment=environment,
                s3=S3Config(
                    region="us-west-2",
                    max_connections=200
                ),
                data_quality=DataQualityConfig(
                    enforce_schema=True,
                    validate_on_write=True,
                    alert_on_quality_degradation=True
                ),
                logging=LoggingConfig(
                    level=LogLevel.INFO,
                    enable_json_logging=True
                ),
                security=SecurityConfig(
                    encrypt_at_rest=True,
                    encrypt_in_transit=True,
                    audit_enabled=True,
                    enable_rbac=True
                ),
                default_bucket="neuralake-staging"
            )
        
        elif environment == Environment.PRODUCTION:
            return cls(
                environment=environment,
                s3=S3Config(
                    region="us-west-2",
                    max_connections=500,
                    max_retries=5
                ),
                data_quality=DataQualityConfig(
                    enforce_schema=True,
                    validate_on_write=True,
                    validate_on_read=True,
                    alert_on_quality_degradation=True,
                    quality_threshold=0.99
                ),
                logging=LoggingConfig(
                    level=LogLevel.WARNING,
                    enable_json_logging=True,
                    async_logging=True
                ),
                security=SecurityConfig(
                    encrypt_at_rest=True,
                    encrypt_in_transit=True,
                    audit_enabled=True,
                    enable_rbac=True,
                    require_mfa=True,
                    enable_pii_detection=True
                ),
                performance=PerformanceConfig(
                    enable_query_cache=True,
                    max_cache_size_mb=4096,
                    async_io=True
                ),
                default_bucket="neuralake-prod"
            )
        
        else:
            raise ValueError(f"Unsupported environment: {environment}")
    
    @classmethod
    def _apply_environment_overrides(cls, config: 'NeuralakeConfig') -> 'NeuralakeConfig':
        """Apply environment variable overrides to configuration."""
        # S3 overrides
        if os.getenv("AWS_ENDPOINT_URL"):
            config.s3.endpoint_url = os.getenv("AWS_ENDPOINT_URL")
        if os.getenv("AWS_REGION"):
            config.s3.region = os.getenv("AWS_REGION")
        
        # Bucket overrides
        if os.getenv("NEURALAKE_BUCKET"):
            config.default_bucket = os.getenv("NEURALAKE_BUCKET")
        
        # Logging overrides
        if os.getenv("NEURALAKE_LOG_LEVEL"):
            try:
                config.logging.level = LogLevel(os.getenv("NEURALAKE_LOG_LEVEL").upper())
            except ValueError:
                warnings.warn(f"Invalid log level: {os.getenv('NEURALAKE_LOG_LEVEL')}")
        
        # Performance overrides
        if os.getenv("NEURALAKE_MAX_WORKERS"):
            try:
                config.performance.max_worker_threads = int(os.getenv("NEURALAKE_MAX_WORKERS"))
            except ValueError:
                warnings.warn(f"Invalid max workers value: {os.getenv('NEURALAKE_MAX_WORKERS')}")
        
        return config
    
    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> 'NeuralakeConfig':
        """Create configuration from dictionary (used for JSON loading)."""
        # This is a simplified implementation - in practice, you'd want
        # more sophisticated dictionary to dataclass conversion
        environment = Environment(data.get("environment", "local"))
        config = cls._create_environment_config(environment)
        
        # Override with values from dictionary
        # Implementation would recursively update nested dataclasses
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        # Simplified implementation - would need recursive conversion
        return {
            "environment": self.environment.value,
            "project_name": self.project_name,
            "version": self.version,
            "default_bucket": self.default_bucket
        }
    
    def save_to_file(self, config_path: Union[str, Path]) -> None:
        """Save configuration to a JSON file."""
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


# Global configuration instance
_config: Optional[NeuralakeConfig] = None


def get_config() -> NeuralakeConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = NeuralakeConfig.from_environment()
    return _config


def set_config(config: NeuralakeConfig) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config


def reset_config() -> None:
    """Reset the global configuration instance."""
    global _config
    _config = None


# Convenience functions for common configuration access patterns
def get_s3_storage_options() -> Dict[str, str]:
    """Get S3 storage options for data engines."""
    return get_config().s3.get_storage_options()


def get_default_bucket() -> str:
    """Get the default S3 bucket name."""
    return get_config().default_bucket


def is_production() -> bool:
    """Check if running in production environment."""
    return get_config().environment == Environment.PRODUCTION


def is_local_development() -> bool:
    """Check if running in local development environment."""
    return get_config().environment == Environment.LOCAL


# Example usage and testing
if __name__ == "__main__":
    # Example: Create configuration for different environments
    
    print("=== Local Development Configuration ===")
    local_config = NeuralakeConfig.from_environment("local")
    print(f"Environment: {local_config.environment.value}")
    print(f"S3 Endpoint: {local_config.s3.endpoint_url}")
    print(f"Allow HTTP: {local_config.s3.allow_http}")
    print(f"Default Bucket: {local_config.default_bucket}")
    print()
    
    print("=== Production Configuration ===")
    try:
        # This will fail without proper environment variables
        prod_config = NeuralakeConfig.from_environment("production")
        print(f"Environment: {prod_config.environment.value}")
        print(f"S3 Endpoint: {prod_config.s3.endpoint_url}")
        print(f"Security: Encryption at rest = {prod_config.security.encrypt_at_rest}")
    except ValueError as e:
        print(f"Production config validation failed (expected): {e}")
    print()
    
    print("=== S3 Storage Options ===")
    storage_options = local_config.s3.get_storage_options()
    for key, value in storage_options.items():
        print(f"{key}: {value}") 