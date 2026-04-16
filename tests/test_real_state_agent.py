import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import real_state_agent as rsa


class RealStateAgentTests(unittest.TestCase):
    def setUp(self):
        self._old_env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._old_env)

    def test_get_openai_api_key_loads_from_env_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / ".env"
            env_path.write_text("OPENAI_API_KEY=sk-test-12345678\n", encoding="utf-8")
            key = rsa.get_openai_api_key(str(env_path))
            self.assertEqual(key, "sk-test-12345678")

    def test_get_openai_api_key_raises_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / ".env"
            env_path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                rsa.get_openai_api_key(str(env_path))

    def test_run_test_interface_reads_prompt_and_exits(self):
        outputs = []
        user_inputs = iter(["Casa de 2 habitaciones", "exit"])

        def fake_input(_):
            return next(user_inputs)

        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-1234567890"}, clear=True):
            rsa.run_test_interface(input_fn=fake_input, output_fn=outputs.append)

        self.assertIn("=== Real State Agent Test Interface ===", outputs)
        self.assertTrue(any("API key loaded" in line for line in outputs))
        self.assertIn("Test request received: Casa de 2 habitaciones", outputs)
        self.assertIn("Goodbye!", outputs)


if __name__ == "__main__":
    unittest.main()
