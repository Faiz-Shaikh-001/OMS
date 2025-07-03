from decimal import Decimal
from datetime import date
from django.test import TestCase

from inventory.models import (
    Frame,
    SingleVision,
    Bifocal,
    ContactLens,
    Progressive,
    FrameTypes,
    MaterialTypes,
)
from inventory.serializers import (
    FrameSerializer,
    SingleVisionSerializer,
    BifocalSerializer,
    ContactLensSerializer,
    ProgressiveSerializer,
)

class FrameTests(TestCase):
    def setUp(self):
        self.valid_data = {
        "frame_type": FrameTypes.RIMLESS,
        "name": "TestFrame",
        "code": "C1",
        "color": "Black",
        "size": 48,
        "quantity": 10,
        "purchase_price": "50.00",
        "sales_price": "100.00",
        }

    def test_frame_field_boundaries(self):
        test_cases = [
            ("purchase_price", "-1.00", False),
            ("sales_price", "-0.01", False),
            ("purchase_price", "0.00", True),
            ("sales_price", "0.00", True),
            ("size", 0, True),
            ("size", -1, True),
            ("quantity", 0, True),
            ("quantity", -5, True),
            ("color", "A" * 101, False),
            ("color", "A" * 100, True),
        ]
        for field, value, expected_validity in test_cases:
            with self.subTest(field=field, value=value):
                data = self.valid_data.copy()
                data[field] = value
                serializer = FrameSerializer(data=data)
                self.assertEqual(serializer.is_valid(), expected_validity)
                if not expected_validity:
                    self.assertIn(field, serializer.errors)

    def test_frame_missing_required(self):
        serializer = FrameSerializer(data={})
        self.assertFalse(serializer.is_valid())
        for fld in self.valid_data:
            self.assertIn(fld, serializer.errors)

    def test_frame_product_code_contains_prefix_and_parts(self):
        frame = Frame(
            frame_type=FrameTypes.FULL_METAL,
            name="FM",
            code="XYZ",
            color="Yellow",
            size=52,
            quantity=1,
            purchase_price=Decimal("10.00"),
            sales_price=Decimal("20.00")
        )
        code = frame.get_product_code()
        self.assertTrue(code.startswith("FRAME-3-XYZ-Yell-52"))
        self.assertIn("-", code)

    def test_frame_str(self):
        f = Frame(
            frame_type=FrameTypes.GOGGLES,
            name="GogglesTest",
            code="GOG",
            color="Clear",
            size=55,
            quantity=1,
            purchase_price=0,
            sales_price=1
        )
        self.assertEqual(str(f), "GogglesTest")

    def test_create_then_update_frame_quantity(self):
        frame = Frame.objects.create(
            frame_type=FrameTypes.RIMLESS,
            name="Temp",
            code="TMP",
            color="Red",
            size=44,
            quantity=5,
            purchase_price=10,
            sales_price=20
        )
        frame.quantity = 2
        frame.save()
        self.assertEqual(Frame.objects.get(pk=frame.pk).quantity, 2)

    def test_datetime_fields_auto_now_add_update(self):
        frm = Frame.objects.create(
            frame_type=FrameTypes.GOGGLES,
            name="DTime",
            code="DT1",
            color="Gray",
            size=50,
            quantity=1,
            purchase_price=5,
            sales_price=10
        )
        created = frm.created_at
        self.assertEqual(created.date(), date.today())
        frm.name = "DTime2"
        frm.save()
        self.assertGreater(frm.updated_at, created)

class SingleVisionTests(TestCase):
    def setUp(self):
        self.valid_sv = {
        "company_name": "BrandSV", "name": "SVLens",
        "spherical": "0.00", "cylindrical": "0.00",
        "pair": 1, "diameter": 65,
        "purchase_price": "10.00", "sales_price": "20.00",
        "material_type": MaterialTypes.PLASTIC_LENS,
        "index": 1,
        }

    def test_singlevision_numeric_bounds(self):
        test_cases = [
            ({"spherical": "24.75"}, True),
            ({"spherical": "-24.75"}, True),
            ({"spherical": "25.00"}, False),
            ({"spherical": "-25.00"}, False),
            ({"cylindrical": "12.75"}, True),
            ({"cylindrical": "-12.75"}, True),
            ({"cylindrical": "13.00"}, False),
            ({"cylindrical": "-13.00"}, False),
            ({"purchase_price": "5.00", "sales_price": "4.00"}, False),
            ({"pair": 0}, True),
            ({"pair": -1}, False),
        ]
        for override, expected in test_cases:
            with self.subTest(override=override):
                data = self.valid_sv.copy()
                data.update(override)
                serializer = SingleVisionSerializer(data=data)
                self.assertEqual(serializer.is_valid(), expected)

    def test_singlevision_missing_fields(self):
        for field in ["material_type", "index"]:
            data = self.valid_sv.copy()
            del data[field]
            serializer = SingleVisionSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_singlevision_product_code_prefix(self):
        sv = SingleVision(**self.valid_sv)
        code = sv.get_product_code()
        self.assertTrue(code.startswith("LENS-SV-"))

class BifocalTests(TestCase):
    def setUp(self):
        self.valid_bf = {
        "company_name": "BrandSV", "name": "BFLens",
        "spherical": "0.00", "cylindrical": "0.00",
        "pair": 1, "diameter": 65,
        "purchase_price": "10.00", "sales_price": "20.00",
        "material_type": MaterialTypes.PLASTIC_LENS,
        "index": 1,
        "axis": 90, "add": "1.25"
        }

    def test_bifocal_axis_add(self):
        test_cases = [
            ({"add": "0.00"}, False),
            ({"add": "5.00"}, True),
            ({"axis": 180}, True),
            ({"axis": -1}, False),
            ({"axis": 181}, False),
            ({"add": "-0.25"}, False),
        ]
        for override, expected in test_cases:
            with self.subTest(override=override):
                data = self.valid_bf.copy()
                data.update(override)
                serializer = BifocalSerializer(data=data)
                self.assertEqual(serializer.is_valid(), expected)

    def test_bifocal_missing_fields(self):
        for field in ["axis"]:
            data = self.valid_bf.copy()
            del data[field]
            serializer = BifocalSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

        data = self.valid_bf.copy()
        del data["add"]
        serializer = BifocalSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("add", serializer.errors)

    def test_bifocal_product_code_prefix(self):
        bf = Bifocal(**self.valid_bf)
        self.assertTrue(bf.get_product_code().startswith("LENS-BF-"))

class ContactLensTests(TestCase):
    def setUp(self):
        self.valid_cl = {
        "company_name": "BrandCL", "name": "CLens",
        "spherical": "-1.25", "cylindrical": "0.00",
        "pair": 2, "diameter": 14,
        "purchase_price": "100.00", "sales_price": "150.00",
        "axis": 10, "base_curve": 8,
        }

    def test_contactlens_axis_curve(self):
        test_cases = [
            ({"axis": 0}, True),
            ({"axis": 180}, True),
            ({"axis": -1}, False),
            ({"axis": 181}, False),
            ({"base_curve": None}, False),
        ]
        for override, expected in test_cases:
            with self.subTest(override=override):
                data = self.valid_cl.copy()
                data.update(override)
                serializer = ContactLensSerializer(data=data)
                self.assertEqual(serializer.is_valid(), expected)

    def test_contactlens_missing_fields(self):
        for field in ["axis", "base_curve"]:
            data = self.valid_cl.copy()
            del data[field]
            serializer = ContactLensSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_contactlens_product_code_prefix(self):
        cl = ContactLens(**self.valid_cl)
        self.assertTrue(cl.get_product_code().startswith("LENS-CL-"))

class ProgressiveLensTests(TestCase):
    def setUp(self):
        self.valid_pg = {
        "company_name": "BrandSV", "name": "PGLens",
        "spherical": "0.00", "cylindrical": "0.00",
        "pair": 1, "diameter": 65,
        "purchase_price": "10.00", "sales_price": "20.00",
        "material_type": MaterialTypes.PLASTIC_LENS,
        "index": 1,
        "axis": 90, "add": "1.25", "side": "LEFT"
        }

    def test_progressive_side_add(self):
        test_cases = [
            ({"side": "RIGHT"}, True),
            ({"side": "INVALID"}, False),
            ({"add": "0.00"}, False),
        ]
        for override, expected in test_cases:
            with self.subTest(override=override):
                data = self.valid_pg.copy()
                data.update(override)
                serializer = ProgressiveSerializer(data=data)
                self.assertEqual(serializer.is_valid(), expected)

    def test_progressive_missing_fields(self):
        for field in ["side", "axis"]:
            data = self.valid_pg.copy()
            del data[field]
            serializer = ProgressiveSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

        data = self.valid_pg.copy()
        del data["add"]
        serializer = ProgressiveSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("add", serializer.errors)

    def test_progressive_product_code_prefix(self):
        pg = Progressive(**self.valid_pg)
        self.assertTrue(pg.get_product_code().startswith("LENS-PG-"))
