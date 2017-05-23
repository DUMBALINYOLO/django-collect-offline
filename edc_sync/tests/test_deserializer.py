import os

from django.core.serializers.base import DeserializationError
from django.test import TestCase, tag
from faker import Faker

from edc_sync_files.transaction import TransactionImporter, TransactionExporter

from ..transaction_deserializer import TransactionDeserializer, TransactionDeserializerError
from ..models import OutgoingTransaction, IncomingTransaction
from .models import TestModel, TestModelWithFkProtected, TestModelWithM2m, M2m
import tempfile
from edc_device.constants import NODE_SERVER

fake = Faker()


class TestDeserializer1(TestCase):

    multi_db = True

    def setUp(self):
        self.export_path = os.path.join(tempfile.gettempdir(), 'export')
        if not os.path.exists(self.export_path):
            os.mkdir(self.export_path)
        self.import_path = self.export_path
        OutgoingTransaction.objects.using('client').all().delete()
        IncomingTransaction.objects.all().delete()
        TestModel.objects.all().delete()
        TestModel.objects.using('client').all().delete()
        TestModel.history.all().delete()
        TestModel.history.using('client').all().delete()
        TestModel.objects.using('client').create(f1='model1')
        TestModel.objects.using('client').create(f1='model2')

        tx_exporter = TransactionExporter(
            export_path=self.export_path,
            using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        self.batch = tx_importer.import_batch(filename=batch.filename)

    def test_deserilize(self):
        tx_deserializer = TransactionDeserializer(override_role=NODE_SERVER)
        tx_deserializer.deserialize_transactions(
            transactions=self.batch.saved_transactions)

    def test_deserilized_object(self):
        tx_deserializer = TransactionDeserializer(override_role=NODE_SERVER)
        tx_deserializer.deserialize_transactions(
            transactions=self.batch.saved_transactions)

    def test_saved(self):
        """Assert transaction object is saved to default db.
        """
        tx_deserializer = TransactionDeserializer(
            override_role=NODE_SERVER,
            using='default')
        tx_deserializer.deserialize_transactions(
            transactions=self.batch.saved_transactions)
        try:
            TestModel.objects.using('default').get(f1='model1')
        except TestModel.DoesNotExist:
            self.fail('TestModel.DoesNotExist unexpectedly raised')


class TestDeserializer2(TestCase):

    multi_db = True

    def setUp(self):
        self.export_path = os.path.join(tempfile.gettempdir(), 'export')
        if not os.path.exists(self.export_path):
            os.mkdir(self.export_path)
        self.import_path = self.export_path
        M2m.objects.all().delete()
        M2m.objects.using('client').all().delete()
        OutgoingTransaction.objects.using('client').all().delete()
        IncomingTransaction.objects.all().delete()
        TestModel.objects.all().delete()
        TestModel.objects.using('client').all().delete()
        TestModel.history.all().delete()
        TestModel.history.using('client').all().delete()

    def test_saved_on_self(self):
        """Asserts can save on self if allow_self=True.
        """
        TestModel.objects.create(f1='model1')
        tx_exporter = TransactionExporter(export_path=self.export_path)
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)
        tx_deserializer = TransactionDeserializer(
            override_role=NODE_SERVER, allow_self=True)
        tx_deserializer.deserialize_transactions(
            transactions=batch.saved_transactions)
        try:
            TestModel.objects.get(f1='model1')
        except TestModel.DoesNotExist:
            self.fail('TestModel unexpectedly does not exist')

    def test_created_from_client(self):
        """Asserts "default" instance is created when "client" instance
        is created.
        """
        TestModel.objects.using('client').create(f1='model1')
        tx_exporter = TransactionExporter(
            export_path=self.export_path, using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)
        tx_deserializer = TransactionDeserializer(
            override_role=NODE_SERVER, allow_self=True)
        tx_deserializer.deserialize_transactions(
            transactions=batch.saved_transactions)
        try:
            TestModel.objects.get(f1='model1')
        except TestModel.DoesNotExist:
            self.fail('TestModel unexpectedly does not exists')

    def test_flagged_as_deserialized(self):
        """Asserts "default" instance is created when "client" instance
        is created.
        """
        TestModel.objects.using('client').create(f1='model1')
        tx_exporter = TransactionExporter(
            export_path=self.export_path, using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)
        tx_deserializer = TransactionDeserializer(
            override_role=NODE_SERVER, allow_self=True)
        tx_deserializer.deserialize_transactions(
            transactions=batch.saved_transactions)
        for transaction in batch.saved_transactions:
            self.assertTrue(transaction.is_consumed)

    def test_deleted_from_client(self):
        """Asserts "default" instance is deleted when "client" instance
        is deleted.
        """
        test_model = TestModel.objects.using('client').create(f1='model1')
        tx_exporter = TransactionExporter(
            export_path=self.export_path, using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)
        tx_deserializer = TransactionDeserializer(
            override_role=NODE_SERVER, allow_self=True)
        tx_deserializer.deserialize_transactions(
            transactions=batch.saved_transactions, deserialize_only=True)
        test_model.delete()
        tx_exporter = TransactionExporter(
            export_path=self.export_path, using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)
        tx_deserializer = TransactionDeserializer(
            override_role=NODE_SERVER, allow_self=True)
        tx_deserializer.deserialize_transactions(
            transactions=batch.saved_transactions)
        try:
            TestModel.objects.get(f1='model1')
        except TestModel.DoesNotExist:
            pass
        else:
            self.fail('TestModel unexpectedly exists')

    def test_dont_allow_saved_on_self(self):
        """Asserts cannot save on self by default.
        """
        TestModel.objects.create(f1='model1')
        tx_exporter = TransactionExporter(export_path=self.export_path)
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        tx_importer.import_batch(filename=batch.filename)
        self.assertRaises(
            TransactionDeserializerError,
            TransactionDeserializer)

    def test_allow_saved_on_self(self):
        """Asserts can save on self by default.
        """
        TestModel.objects.create(f1='model1')
        tx_exporter = TransactionExporter(export_path=self.export_path)
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        tx_importer.import_batch(filename=batch.filename)
        self.assertRaises(TransactionDeserializerError,
                          TransactionDeserializer, allow_self=True)

    def test_allow_saved_on_any_device(self):
        """Asserts can save on self by default.
        """
        TestModel.objects.create(f1='model1')
        tx_exporter = TransactionExporter(export_path=self.export_path)
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        tx_importer.import_batch(filename=batch.filename)
        self.assertRaises(TransactionDeserializerError,
                          TransactionDeserializer, allow_self=True)

    def test_deserialized_with_fk(self):
        """Asserts correctly deserialized model with FK.
        """
        test_model = TestModel.objects.using('client').create(f1='model1')
        TestModelWithFkProtected.objects.using(
            'client').create(f1='f1', test_model=test_model)
        tx_exporter = TransactionExporter(
            export_path=self.export_path, using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)
        tx_deserializer = TransactionDeserializer(
            allow_self=True, override_role=NODE_SERVER)
        tx_deserializer.deserialize_transactions(
            transactions=batch.saved_transactions)
        test_model = TestModel.objects.get(f1='model1')
        try:
            obj = TestModelWithFkProtected.objects.get(f1='f1')
        except TestModelWithFkProtected.DoesNotExist:
            self.fail('TestModel unexpectedly does not exists')
        self.assertEqual(test_model, obj.test_model)

    def test_deserialized_with_history(self):
        """Asserts correctly deserialized model with history.
        """
        TestModel.objects.using('client').create(f1='model1')
        tx_exporter = TransactionExporter(
            export_path=self.export_path, using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)
        tx_deserializer = TransactionDeserializer(
            allow_self=True, override_role=NODE_SERVER)
        tx_deserializer.deserialize_transactions(
            transactions=batch.saved_transactions)
        try:
            TestModel.history.get(f1='model1')
        except TestModel.DoesNotExist:
            self.fail('TestModel history unexpectedly does not exists')

    @tag('erik')
    def test_deserialize_with_m2m(self):
        """Asserts deserializes model with M2M as long as
        M2M instance exists on destination.
        """
        obj = TestModelWithM2m.objects.using('client').create(f1='model1')
        m2m = M2m.objects.using('client').create(name='erik', short_name='bob')
        obj.m2m.add(m2m)

        tx_exporter = TransactionExporter(
            export_path=self.export_path, using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)

        M2m.objects.create(name='erik', short_name='bob')

        tx_deserializer = TransactionDeserializer(
            allow_self=True, override_role=NODE_SERVER)
        tx_deserializer.deserialize_transactions(
            transactions=batch.saved_transactions, deserialize_only=False)
        obj = TestModelWithM2m.objects.get(f1='model1')

        obj.m2m.get(short_name='bob')

    def test_deserialize_with_m2m_missing(self):
        """Asserts deserialization error if m2m instance does not
        exist on destination.
        """
        obj = TestModelWithM2m.objects.using('client').create(f1='model1')
        m2m = M2m.objects.using('client').create(name='erik')
        obj.m2m.add(m2m)
        tx_exporter = TransactionExporter(
            export_path=self.export_path, using='client')
        batch = tx_exporter.export_batch()
        tx_importer = TransactionImporter(import_path=self.import_path)
        batch = tx_importer.import_batch(filename=batch.filename)
        tx_deserializer = TransactionDeserializer(
            allow_self=True, override_role=NODE_SERVER)
        self.assertRaises(
            DeserializationError,
            tx_deserializer.deserialize_transactions,
            transactions=batch.saved_transactions)