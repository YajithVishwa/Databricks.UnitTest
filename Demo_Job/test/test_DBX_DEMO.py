# Databricks notebook source
# MAGIC %run ../src/DBX_DEMO

# COMMAND ----------

import os
import sys
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
target_folder_path = os.path.join(parent_dir, 'src')
sys.path.append(target_folder_path)

try:
    import DBX_DEMO
    from DBX_DEMO import main
except:
    pass

# COMMAND ----------

os.environ['RUN_MODE'] = 'dbx'

# COMMAND ----------

import unittest
from unittest.mock import patch, MagicMock

mock_dbutils = MagicMock()
mock_dbutils.secrets.get.side_effect = lambda scope, key: f"{scope}_{key}_value"
sys.modules['databricks'] = MagicMock()
sys.modules['databricks.sdk'] = MagicMock()
sys.modules['databricks.sdk.runtime'] = MagicMock()
sys.modules['databricks.sdk.runtime.dbutils'] = mock_dbutils


class testDbxDemo(unittest.TestCase):
    def setUp(self):
        if os.getenv('RUN_MODE', 'test') == 'test':
            self.mock_spark = MagicMock()
            self.mock_spark.createDataFrame.return_value = MagicMock()
            setattr(DBX_DEMO, 'spark', self.mock_spark)
            setattr(DBX_DEMO, 'display', lambda df: None)
        else:
            global spark
            self.mock_spark = MagicMock()
            spark = self.mock_spark
            global display
            display = lambda df: None
    
    def test_main(self):
        main()
        self.mock_spark.createDataFrame.assert_called_once_with(
        [(1, 'yajith', 100), (2, 'vishwa', 200)],
        schema='id int, name string, mark int'
        )

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)