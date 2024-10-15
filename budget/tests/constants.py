"""
Модуль с константами для тестирования API бюджета
"""
BUDGET = {
                "income": {
                    "Salary": {
                        "forecast": 1000.0,
                        "actual": 800.0,
                        "is_notified": False,
                        "date_notified": None
                    }
                },
                "expense": {
                    "Food": {
                        "forecast": 300.0,
                        "actual": 250.0,
                        "is_notified": False,
                        "date_notified": None
                    }
                }
            }
