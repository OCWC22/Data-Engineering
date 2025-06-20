#!/usr/bin/env python3
"""
Unified verification script for the Neuralake data platform.

This script runs a suite of tests to verify that the core components
(configuration, tables, catalog, and query execution) function correctly
in both LOCAL and PRODUCTION environments. It uses environment variables
to switch between configurations and ensures that the system behaves as
expected in each mode.
"""

import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

# Add the 'src' directory to sys.path to allow direct imports of modules like 'config'
SCRIPT_DIR = Path(__file__).parent
SRC_DIR = SCRIPT_DIR.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# --- Path Setup ---
# Add the source directory to the Python path to allow importing the 'neuralake' package
SRC_ROOT = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(SRC_ROOT))


class TestNeuralakePlatform(unittest.TestCase):
    """
    A suite of integration tests for the Neuralake platform.
    It uses context managers to simulate different environments.
    """

    def test_01_local_configuration(self):
        """Verify that the LOCAL environment loads correctly."""
        print("\\n🔧 Verifying LOCAL Configuration...")
        with self.env_context("local"):
            from config import get_config, is_local_development, is_production

            config = get_config()
            self.assertIsNotNone(config)
            self.assertTrue(is_local_development())
            self.assertFalse(is_production())
            self.assertIn("localhost", config.s3.endpoint_url)
            print("  ✓ LOCAL config loaded successfully.")

    def test_02_production_configuration(self):
        """Verify that the PRODUCTION environment loads and validates correctly."""
        print("\\n🔧 Verifying PRODUCTION Configuration...")

        # Production requires credentials
        mock_creds = {
            "AWS_ACCESS_KEY_ID": "test-key",
            "AWS_SECRET_ACCESS_KEY": "test-secret",
        }

        with self.env_context("production", mock_creds):
            from config import get_config, is_local_development, is_production

            config = get_config()
            self.assertIsNotNone(config)
            self.assertFalse(is_local_development())
            self.assertTrue(is_production())
            # In our default prod config, endpoint_url is None to use AWS default
            self.assertIsNone(config.s3.endpoint_url)
            print("  ✓ PRODUCTION config loaded successfully.")

    def test_03_table_creation_in_local_env(self):
        """Verify table creation in a LOCAL environment (no partitioning)."""
        print("\\n📊 Verifying Table Creation (LOCAL)...")
        with self.env_context("local"):
            from config import get_s3_storage_options
            from my_tables import part

            # In local env, partitioning should be off by default
            self.assertEqual(len(part.partitioning), 0)
            self.assertIn(
                "localhost", get_s3_storage_options().get("AWS_ENDPOINT_URL", "")
            )
            print("  ✓ 'part' table created correctly for LOCAL (no partitioning).")

    def test_04_table_creation_in_prod_env(self):
        """Verify table creation in a PRODUCTION environment (with partitioning)."""
        print("\\n📊 Verifying Table Creation (PRODUCTION)...")
        mock_creds = {"AWS_ACCESS_KEY_ID": "test", "AWS_SECRET_ACCESS_KEY": "test"}
        with self.env_context("production", mock_creds):
            from config import get_s3_storage_options
            from my_tables import part

            # In production, partitioning should be ON by default
            self.assertGreater(len(part.partitioning), 0)
            self.assertEqual(part.partitioning[0].column, "p_brand")
            self.assertIsNone(get_s3_storage_options().get("AWS_ENDPOINT_URL"))
            print(
                "  ✓ 'part' table created correctly for PRODUCTION (with partitioning)."
            )

    def test_05_catalog_creation(self):
        """Verify that the DemoCatalog can be created in any environment."""
        print("\\n📚 Verifying Catalog Creation...")
        with self.env_context("local"):
            from my_catalog import DemoCatalog

            self.assertIsNotNone(DemoCatalog)
            self.assertIn("demo_db", DemoCatalog.dbs())
        print("  ✓ Catalog created successfully in LOCAL env.")

        mock_creds = {"AWS_ACCESS_KEY_ID": "test", "AWS_SECRET_ACCESS_KEY": "test"}
        with self.env_context("production", mock_creds):
            from my_catalog import DemoCatalog

            self.assertIsNotNone(DemoCatalog)
            self.assertIn("demo_db", DemoCatalog.dbs())
        print("  ✓ Catalog created successfully in PRODUCTION env.")

    def test_06_query_script_execution(self):
        """Verify that the query script can run without errors (mocking the final collect call)."""
        print("\\n⚡ Verifying Query Script Execution...")

        with self.env_context("local"):
            import query_data

            # We patch the 'collect' method to avoid actually hitting S3
            with patch("neuralake.core.NlkDataFrame.collect") as mock_collect:
                mock_collect.return_value = "Mocked Data"
                try:
                    query_data.main()
                    print("  ✓ Query script ran successfully in LOCAL env.")
                except Exception as e:
                    self.fail(f"query_data.main() failed in local env: {e}")

    @classmethod
    def env_context(cls, env: str, temp_vars: dict = None):
        """A context manager to temporarily set environment variables."""
        from config import reset_config

        # Unload modules to force re-import with new env vars
        modules_to_unload = ["config", "my_tables", "my_catalog", "query_data"]
        for mod in modules_to_unload:
            if mod in sys.modules:
                del sys.modules[mod]

        reset_config()  # Reset the global config state

        env_vars = {"NEURALAKE_ENV": env}
        if temp_vars:
            env_vars.update(temp_vars)

        return patch.dict(os.environ, env_vars)


if __name__ == "__main__":
    print("--- Running Neuralake Platform Verification Suite ---")
    suite = unittest.TestSuite()
    # Add tests in a specific order
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestNeuralakePlatform))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\\n✅ All verification checks passed successfully!")
        sys.exit(0)
    else:
        print("\\n❌ Verification failed.")
        sys.exit(1)
