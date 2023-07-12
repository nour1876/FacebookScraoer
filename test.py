import unittest
from unittest.mock import patch
from facebookScraper import get_data

class TestDataFetching(unittest.TestCase):

    @patch('facebookScraper.requests.get')
    def test_get_data(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.content = b'<html>Mocked HTML content</html>'
        mock_soup = mock_response.soup
        mock_soup.find.return_value = mock_soup
        mock_soup.text = 'Mocked Page Title'
        mock_soup.__getitem__.return_value = {'content': 'Mocked Description'}
        url = 'http://example.com'
        result = get_data(url)
        self.assertEqual(result['page_title'], 'Mocked Page Title')
        self.assertEqual(result['description_content'], 'Mocked Description')
        mock_get.assert_called_once_with(url)

if __name__ == '__main__':
    unittest.main()