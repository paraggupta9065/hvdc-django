import random
import openpyxl
from api.models import Category, PathologyTest
from user.models import Pathology


def upload_tests():
    wb = openpyxl.load_workbook("./tests.xlsx")
    sheet = wb.active
    i = 1
    for row in sheet.iter_rows(min_row=2, values_only=True):
        name = list(row)[5]
        print(name)

        regular_price = random.randint(1000, 2000)
        PathologyTest.objects.create(name = name,
                                    description = name,
                                    test_type="Blood Test",
                                    pathology = Pathology.objects.get(id=1),
                                    category = Category.objects.get(id = 1),
                                    regular_price = regular_price,
                                    price = regular_price - random.randint(10, 100),
                                    )