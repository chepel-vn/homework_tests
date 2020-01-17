import unittest
import json
import commands_for_docs
from unittest.mock import patch


documents = []
directories = {}


def setUpModule():
    with open('fixtures/documents.json', 'r', encoding='utf-8') as out_docs:
        documents.extend(json.load(out_docs))

    with open('fixtures/directories.json', 'r', encoding='utf-8') as out_dirs:
        directories.update(json.load(out_dirs))


@patch('commands_for_docs.documents', documents, create=True)
@patch('commands_for_docs.directories', directories, create=True)
class TestCommandsForDocs(unittest.TestCase):

    def setUp(self):
        self.documents = documents.copy()
        self.directories = directories.copy()

    def test_test_first_symbol_digits(self):
        result = commands_for_docs.test_first_symbol_digits('4fghsdh', 0, 9)
        self.assertTrue(result)
        result = commands_for_docs.test_first_symbol_digits('ffghsdh', 0, 9)
        self.assertFalse(result)
        result = commands_for_docs.test_first_symbol_digits('', 0, 9)
        self.assertFalse(result)

    def test_test_string_digits(self):
        result = commands_for_docs.test_string_digits('gfhgf')
        self.assertFalse(result)
        result = commands_for_docs.test_string_digits('gf346gfh')
        self.assertFalse(result)
        result = commands_for_docs.test_string_digits('3546409')
        self.assertTrue(result)

        # Negative test case
        result = commands_for_docs.test_string_digits('')
        self.assertFalse(result)

    @patch('commands_for_docs.test_first_symbol_digits')
    @patch('commands_for_docs.input')
    def test_input_number_document(self, mock_input, mock_test_first_symbol_digits):
        mock_input.return_value = '1'
        input_number = commands_for_docs.input_number_document()
        self.assertIsNotNone(input_number)

        mock_input.return_value = 'test'
        mock_test_first_symbol_digits.return_value = True
        input_number = commands_for_docs.input_number_document()
        self.assertEqual(input_number, 'test')

    @patch('commands_for_docs.input')
    def test_input_type_document(self, mock_input):
        mock_input.return_value = '0'
        result_string = commands_for_docs.input_type_document()
        self.assertEqual(result_string, 'passport')

        mock_input.return_value = '1'
        result_string = commands_for_docs.input_type_document()
        self.assertEqual(result_string, 'invoice')

        mock_input.return_value = '2'
        result_string = commands_for_docs.input_type_document()
        self.assertEqual(result_string, 'insurance')

    @patch('commands_for_docs.input_number_document')
    @patch('commands_for_docs.input_type_document')
    @patch('commands_for_docs.input_name_owner')
    @patch('commands_for_docs.input_number_exist_shelf')
    @patch('commands_for_docs.print')
    def test_execute_command_add(self, mock_print, mock_input_number_exist_shelf,
                                 mock_input_name_owner, mock_input_type_document, mock_input_number_document):
        # add document_number=1676 passport=0 name_owner='Геннадий Сидоров' to self_number='3'
        mock_input_number_document.return_value = 1676
        mock_input_type_document.return_value = 0
        mock_input_name_owner.return_value = 'Геннадий Сидоров'
        mock_input_number_exist_shelf.return_value = '3'
        mock_print.return_value = ''
        count_docs_shelf3 = len(self.directories['3'])
        with patch('commands_for_docs.directories', self.directories):
            commands_for_docs.execute_command_add()
        self.assertGreater(len(self.directories['3']), count_docs_shelf3)

    @patch('commands_for_docs.input_number_shelf')
    @patch('commands_for_docs.print')
    def test_execute_command_add_shelf(self, mock_print, mock_input_number_shelf):
        shelf_found = self.directories.get('4')
        self.assertIsNone(shelf_found)
        mock_input_number_shelf.return_value = '4'
        mock_print.return_value = ''
        with patch('commands_for_docs.directories', self.directories):
            commands_for_docs.execute_command_add_shelf()
        shelf_found = self.directories.get('4')
        self.assertIsNotNone(shelf_found)
        self.assertEqual(len(shelf_found), 0)

    def test_get_document_by_number(self):
        document_found = commands_for_docs.get_document_by_number('11-2')
        # {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        self.assertIsNotNone(document_found)
        self.assertEqual(document_found['type'], 'invoice')
        self.assertEqual(document_found['name'], 'Геннадий Покемонов')

        document_found = commands_for_docs.get_document_by_number('11-45')
        self.assertIsNone(document_found)

    def test_get_shelf_number_by_number_document(self):
        shelf_found = commands_for_docs.get_shelf_number_by_number_document(1676)
        self.assertIsNotNone(shelf_found)
        self.assertEqual(shelf_found, '3')

        shelf_found = commands_for_docs.get_shelf_number_by_number_document(12468)
        self.assertIsNone(shelf_found)

    def test_delete_document_from_shelfs(self):
        shelf_found = commands_for_docs.get_shelf_number_by_number_document(1676)
        self.assertEqual(shelf_found, '3')
        shelf_number = commands_for_docs.delete_document_from_shelfs(1676)
        self.assertEqual(shelf_number, '3')
        shelf_found = commands_for_docs.get_shelf_number_by_number_document(1676)
        self.assertIsNone(shelf_found)

        shelf_found = commands_for_docs.get_shelf_number_by_number_document(1000)
        self.assertIsNone(shelf_found)
        shelf_number = commands_for_docs.delete_document_from_shelfs(1000)
        self.assertIsNone(shelf_number)

    def test_delete_document_from_catalog(self):
        document_found = commands_for_docs.get_document_by_number('11-2')
        self.assertIsNotNone(document_found)
        result_ok = commands_for_docs.delete_document_from_catalog('11-2')
        self.assertTrue(result_ok)
        document_found = commands_for_docs.get_document_by_number('11-2')
        self.assertIsNone(document_found)

        document_found = commands_for_docs.get_document_by_number('11-45')
        self.assertIsNone(document_found)
        result_ok = commands_for_docs.delete_document_from_catalog('11-45')
        self.assertFalse(result_ok)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCommandsForDocs('test_execute_command_add_shelf'))
    suite.addTest(TestCommandsForDocs('test_test_first_symbol_digits'))
    suite.addTest(TestCommandsForDocs('test_test_string_digits'))
    suite.addTest(TestCommandsForDocs('test_input_number_document'))
    suite.addTest(TestCommandsForDocs('test_input_type_document'))
    suite.addTest(TestCommandsForDocs('test_execute_command_add'))
    suite.addTest(TestCommandsForDocs('test_get_document_by_number'))
    suite.addTest(TestCommandsForDocs('test_get_shelf_number_by_number_document'))
    suite.addTest(TestCommandsForDocs('test_delete_document_from_shelfs'))
    suite.addTest(TestCommandsForDocs('test_delete_document_from_catalog'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(create_suite())
