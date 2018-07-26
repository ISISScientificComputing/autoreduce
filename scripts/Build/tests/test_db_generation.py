import MySQLdb
import unittest

# All TABLES in the database Schema
ALL_TABLES = {"auth_group",
              "auth_group_permissions",
              "auth_permission",
              "auth_user",
              "auth_user_groups",
              "auth_user_user_permissions",
              "django_admin_log",
              "django_content_type",
              "django_migrations",
              "django_session",
              "reduction_variables_runvariable",
              "reduction_variables_variable",
              "reduction_variables_instrumentvariable",
              "reduction_viewer_datalocation",
              "reduction_viewer_experiment",
              "reduction_viewer_instrument",
              "reduction_viewer_notification",
              "reduction_viewer_reductionlocation",
              "reduction_viewer_reductionrun",
              "reduction_viewer_setting",
              "reduction_viewer_status"}


class TestDatabaseGeneration(unittest.TestCase):

    def test_localhost_db_construction(self):
        """
        Test that the local host database on travis is correctly
        generated from the .sql construction files
        """
        db = MySQLdb.connect(host="localhost",
                             user="test-user",
                             passwd="pass",
                             db="autoreduction")

        cur = db.cursor()
        cur.execute("SHOW TABLES")
        all_tables = set()
        for row in cur.fetchall():
            all_tables.add(row[0])
        self.assertEqual(ALL_TABLES, all_tables)
        db.close()

    def test_localhost_reduction_viewer_db_population(self):
        """
        Test that the local host database has been populated with data
        Current test data adds 3 rows per table (so check this)
        exception to this is status that has 5 columns
        """
        db = MySQLdb.connect(host="localhost",
                             user="test-user",
                             passwd="pass",
                             db="autoreduction")
        cur = db.cursor()
        for table in list(ALL_TABLES):
            if "reduction_viewer" in table:
                cur.execute("SELECT * FROM {};".format(table))
                if table == "reduction_viewer_status":
                    self.assertTrue(len(cur.fetchall()) == 5,
                                    "{} does not contain 5 rows.{} : {}".
                                    format(table, table, cur.fetchall()))
                else:
                    self.assertTrue(len(cur.fetchall()) >= 3,
                                    "{} does not contain at least 3 rows.{} : {}".
                                    format(table, table, cur.fetchall()))
        db.close()