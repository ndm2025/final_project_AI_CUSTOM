import json
import threading
import unittest
from urllib.request import Request, urlopen

from backend.server import create_server


class CagOwnTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def url(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def get_json(self, path):
        with urlopen(self.url(path), timeout=5) as r:
            return r.status, json.loads(r.read().decode("utf-8"))

    def post_json(self, path, payload):
        req = Request(
            self.url(path),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read().decode("utf-8"))

    def test_context_empty_for_new_user(self):
        status, body = self.get_json("/api/context?user_id=nuevo")
        self.assertEqual(status, 200)
        self.assertEqual(body["context"], [])

    def test_save_overwrites_existing_key(self):
        self.post_json("/api/context", {"user_id": "u1", "key": "lang", "value": "es"})
        self.post_json("/api/context", {"user_id": "u1", "key": "lang", "value": "en"})
        status, body = self.get_json("/api/context?user_id=u1")
        self.assertEqual(status, 200)
        items = body["context"]
        en_items = [i for i in items if i["key"] == "lang" and i["value"] == "en"]
        self.assertEqual(len(en_items), 1)
        es_items = [i for i in items if i["value"] == "es"]
        self.assertEqual(len(es_items), 0)

    def test_multiple_users_context_isolated(self):
        self.post_json("/api/context", {"user_id": "a", "key": "city", "value": "guatemala"})
        self.post_json("/api/context", {"user_id": "b", "key": "city", "value": "quetzaltenango"})
        _, body_a = self.get_json("/api/context?user_id=a")
        _, body_b = self.get_json("/api/context?user_id=b")
        values_a = [i["value"] for i in body_a["context"] if i["key"] == "city"]
        values_b = [i["value"] for i in body_b["context"] if i["key"] == "city"]
        self.assertIn("guatemala", values_a)
        self.assertNotIn("quetzaltenango", values_a)
        self.assertIn("quetzaltenango", values_b)
        self.assertNotIn("guatemala", values_b)

    def test_ask_without_context_returns_normal_answer(self):
        status, body = self.post_json("/api/ask", {"user_id": "noctx", "question": "Que es RAG?"})
        self.assertEqual(status, 200)
        self.assertEqual(body["context_used"], [])
        self.assertIn("RAG recupera", body["answer"])

    def test_ask_with_multiple_context_items(self):
        self.post_json("/api/context", {"user_id": "multi", "key": "audience", "value": "experto"})
        self.post_json("/api/context", {"user_id": "multi", "key": "preferred_style", "value": "detalles tecnicos"})
        status, body = self.post_json("/api/ask", {"user_id": "multi", "question": "Que es CAG?"})
        self.assertEqual(status, 200)
        self.assertIn("audience", body["context_used"])
        self.assertIn("preferred_style", body["context_used"])

    def test_unknown_context_key_does_not_break(self):
        self.post_json("/api/context", {"user_id": "unk", "key": "some_random_key", "value": "test"})
        status, body = self.post_json("/api/ask", {"user_id": "unk", "question": "Que es BDD?"})
        self.assertEqual(status, 200)
        self.assertNotIn("some_random_key", body["context_used"])


if __name__ == "__main__":
    unittest.main()
