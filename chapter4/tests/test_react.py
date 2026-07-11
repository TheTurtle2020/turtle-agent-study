import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from react import ReActAgent


class ReActAgentTests(unittest.TestCase):
    def test_finish_action_with_multiline_content_is_parsed(self):
        agent = ReActAgent(llm_client=object(), tool_executor=object())
        response_text = "Thought: 先思考\nAction: Finish[第一行\n第二行]"

        thought, action = agent._parse_output(response_text)
        self.assertEqual(thought, "先思考")
        self.assertEqual(action, "Finish[第一行\n第二行]")

        match = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "第一行\n第二行")


if __name__ == "__main__":
    unittest.main()
