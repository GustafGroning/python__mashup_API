import unittest 
import requests



class TestStringMethods(unittest.TestCase):
    def test_mashup_correct_output(self): #prövar ifall output från api:t tar rätt form, genom att se efter ifall inmatade URLn
        # (som leder till Nirvana) anger att album #1 har title: Before We Ever Minded
        response = requests.get("http://localhost:5000/search/5b11f4ce-a62d-471e-81fc-a69a8278c7da")

        response_body = response.json()
        self.assertEqual(response_body['albums'][0]['title'], "Bleach")


# assert true if response.data['albums'][0] == 'Baby penis'


if __name__ == '__main__':
    unittest.main()


#"http://musicbrainz.org/ws/2/artist/5b11f4ce-a62d-471e-81fc-a69a8278c7da?&f%20mt=json&inc=url-rels+release-groups&fmt=json"