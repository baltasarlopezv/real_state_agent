import unittest

import real_state_agent


class RealStateAgentTests(unittest.TestCase):
    def test_build_chat_payload_contains_expected_fields(self) -> None:
        payload = real_state_agent.build_chat_payload("Looking for a house in Valencia", model="gpt-4o-mini")

        self.assertEqual(payload["model"], "gpt-4o-mini")
        self.assertEqual(payload["temperature"], 0.3)
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertIn("real estate assistant", payload["messages"][0]["content"])
        self.assertEqual(payload["messages"][1]["role"], "user")
        self.assertIn("Looking for a house in Valencia", payload["messages"][1]["content"])

    def test_generate_real_state_response_requires_api_key(self) -> None:
        with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY is required"):
            real_state_agent.generate_real_state_response("Need a studio in Barcelona", api_key=None)


if __name__ == "__main__":
    unittest.main()
