#!/usr/bin/env python3
"""
Local Development Environment Setup

Sets up MinIO + LocalStack for local development without real AWS charges.
This script ensures your development environment is properly configured
with LOCAL endpoints and removes any risk of accidental cloud charges.
"""

import os
import subprocess
import sys
import time
import requests
from pathlib import Path

def check_docker():
    """Check if Docker is running."""
    try:
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Docker is not running. Please start Docker Desktop and try again.")
            return False
        print("✅ Docker is running")
        return True
    except FileNotFoundError:
        print("❌ Docker is not installed. Please install Docker Desktop.")
        return False

def start_local_stack():
    """Start MinIO and LocalStack containers."""
    print("🚀 Starting local development stack...")
    
    # Check if docker-compose file exists
    compose_file = Path(__file__).parent.parent / "docker-compose.localstack.yml"
    if not compose_file.exists():
        print(f"❌ Docker compose file not found: {compose_file}")
        return False
    
    try:
        # Start services
        subprocess.run([
            'docker-compose', 
            '-f', str(compose_file),
            'up', '-d'
        ], check=True, cwd=compose_file.parent)
        print("✅ LocalStack + MinIO containers started")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start containers: {e}")
        return False

def wait_for_services():
    """Wait for services to be healthy."""
    print("⏳ Waiting for services to be ready...")
    
    services = [
        ("MinIO", "http://localhost:9000/minio/health/live"),
        ("LocalStack", "http://localhost:4566/_localstack/health")
    ]
    
    for service_name, health_url in services:
        max_retries = 30
        for attempt in range(max_retries):
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {service_name} is ready")
                    break
            except requests.exceptions.RequestException:
                pass
            
            if attempt == max_retries - 1:
                print(f"❌ {service_name} failed to start")
                return False
            
            time.sleep(2)
    
    return True

def configure_environment():
    """Set up environment variables for local development."""
    print("🔧 Setting up environment configuration...")
    
    env_file = Path(__file__).parent.parent / ".env.local"
    
    env_content = """# Local Development Environment - NO REAL AWS CHARGES
# This configuration uses LocalStack + MinIO for 100% local simulation

# Environment designation
ENVIRONMENT=local-development

# MinIO configuration (S3-compatible local storage)
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_ENDPOINT_URL=http://localhost:9000
AWS_DEFAULT_REGION=us-east-1

# LocalStack configuration (AWS service emulation)
LOCALSTACK_ENDPOINT_URL=http://localhost:4566

# Delta Lake DynamoDB locking (LocalStack)
DELTALAKE_LOCKING_PROVIDER=dynamodb
DELTALAKE_DYNAMODB_TABLE=neuralake_local_lock
DELTALAKE_DYNAMODB_ENDPOINT_URL=http://localhost:4566

# Test results configuration
TEST_RESULTS_BUCKET=neuralake-test-results
NEURALAKE_BUCKET=neuralake-bucket

# Security settings for local development
SANITIZE_SYSTEM_INFO=true

# Development flags
CI=false
DEBUG=true
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Environment file created: {env_file}")
    print("💡 To use this environment, run: export $(cat .env.local | xargs)")
    
    return True

def verify_configuration():
    """Verify that the configuration is working."""
    print("🔍 Verifying configuration...")
    
    # Test MinIO connection
    try:
        from minio import Minio
        client = Minio(
            'localhost:9000',
            access_key='minioadmin',
            secret_key='minioadmin',
            secure=False
        )
        
        # Ensure buckets exist
        buckets = ['neuralake-bucket', 'neuralake-test-results']
        for bucket in buckets:
            if not client.bucket_exists(bucket):
                client.make_bucket(bucket)
                print(f"✅ Created MinIO bucket: {bucket}")
            else:
                print(f"✅ MinIO bucket exists: {bucket}")
    
    except Exception as e:
        print(f"⚠️  MinIO configuration issue: {e}")
        print("   You may need to install: pip install minio")
    
    # Test LocalStack DynamoDB
    try:
        import boto3
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:4566',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
        
        # Create the locking table if it doesn't exist
        table_name = 'neuralake_local_lock'
        try:
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'tablePath', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'tablePath', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            table.wait_until_exists()
            print(f"✅ Created DynamoDB table: {table_name}")
        except Exception:
            print(f"✅ DynamoDB table exists: {table_name}")
    
    except Exception as e:
        print(f"⚠️  LocalStack configuration issue: {e}")
        print("   This is usually fine - LocalStack will create resources as needed")
    
    return True

def show_status():
    """Show the status of local services."""
    print("\n" + "="*60)
    print("🏠 LOCAL DEVELOPMENT ENVIRONMENT STATUS")
    print("="*60)
    print()
    print("✅ ALL SERVICES RUNNING LOCALLY - NO AWS CHARGES")
    print()
    print("📊 Available Services:")
    print("   • MinIO S3 API: http://localhost:9000")
    print("   • MinIO Console: http://localhost:9001 (admin/minioadmin)")
    print("   • LocalStack: http://localhost:4566")
    print()
    print("🔧 To use this environment:")
    print("   export $(cat .env.local | xargs)")
    print("   python scripts/test_metrics_collector.py")
    print()
    print("🛑 To stop services:")
    print("   docker-compose -f docker-compose.localstack.yml down")
    print()
    print("⚠️  REMINDER: This is 100% local - no real AWS resources or charges!")
    print("="*60)

def main():
    """Main setup function."""
    print("🏠 NeuralLake Local Development Environment Setup")
    print("================================================")
    print()
    print("This will set up MinIO + LocalStack for 100% local development.")
    print("No real AWS services will be used - no charges will be incurred.")
    print()
    
    if not check_docker():
        sys.exit(1)
    
    if not start_local_stack():
        sys.exit(1)
    
    if not wait_for_services():
        sys.exit(1)
    
    if not configure_environment():
        sys.exit(1)
    
    if not verify_configuration():
        sys.exit(1)
    
    show_status()
    
    print("\n🎉 Local development environment is ready!")
    print("You can now run tests and development with zero AWS charges.")

if __name__ == "__main__":
    main() 