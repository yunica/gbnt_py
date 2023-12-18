from django.test import TestCase
import requests

# test api

HOST_URL = "http://localhost:8000"
END_POINTS = ["employees_by_departments_jobs_quarter", "employees_hired_by_department"]


class TestEndPoints(TestCase):
    def test_general_state(self):
        for end_point in END_POINTS:
            r = requests.get(f"{HOST_URL}/api/{end_point}")
            self.assertEqual(
                first=r.status_code, second=200, msg=f"status code {end_point}"
            )
            self.assertEqual(
                first=type(r.json()), second=list, msg=f"type data {end_point}"
            )

    def test_ebdj_quarter_dtypes(self):
        r = requests.get(f"{HOST_URL}/api/employees_by_departments_jobs_quarter")
        data = r.json()
        self.assertNotEqual(
            first=len(data),
            second=0,
            msg=f"empty data for employees_by_departments_jobs_quarter",
        )
        if len(data) != 0:
            test_data = data[0]
            expected_keys_types = {
                "departments": str,
                "jobs": str,
                "Q1": int,
                "Q2": int,
                "Q3": int,
                "Q4": int,
            }
            self.assertEqual(
                set(test_data.keys()), set(expected_keys_types.keys()), "key tests"
            )
            # test types
            for key, d_type in expected_keys_types.items():
                self.assertIsInstance(
                    test_data.get(key), d_type, f"key: '{key}' not is {d_type}."
                )

    def test_ehb_department_dtypes(self):
        r = requests.get(f"{HOST_URL}/api/employees_hired_by_department")
        data = r.json()
        self.assertNotEqual(
            first=len(data),
            second=0,
            msg=f"empty data for employees_hired_by_department",
        )
        if len(data) != 0:
            test_data = data[0]
            expected_keys_types = {
                "department__id": int,
                "department__department": str,
                "hired": int,
            }
            self.assertEqual(
                set(test_data.keys()), set(expected_keys_types.keys()), "key tests"
            )
            # test types
            for key, d_type in expected_keys_types.items():
                self.assertIsInstance(
                    test_data.get(key), d_type, f"key: '{key}' not is {d_type}."
                )
