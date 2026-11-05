import pymysql
pymysql.install_as_MySQLdb()

from django.db.backends.mysql.base import DatabaseWrapper, DatabaseFeatures

# 1. Ignorar la versión de MariaDB
DatabaseWrapper.check_database_version_supported = lambda self: None

# 2. Desactivar el soporte de RETURNING a nivel de características globales
DatabaseFeatures.can_return_columns_from_insert = False
DatabaseFeatures.can_return_rows_from_bulk_insert = False