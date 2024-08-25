import unittest, os
from unittest.mock import MagicMock
from llm import LLM


class TestLLM(unittest.TestCase):
    def setUp(self):
        self.llm = LLM()

    def dict_to_mock(self, d):
        """递归地将字典转换为 Mock 对象，使其支持点号访问"""
        if isinstance(d, dict):
            mock = MagicMock()
            for key, value in d.items():
                setattr(mock, key, self.dict_to_mock(value))
            return mock
        elif isinstance(d, list):
            return [self.dict_to_mock(item) for item in d]
        else:
            return d

    def test_generate_daily_report_mock(self):
        markdown_content = "Sample markdown content"
        expected_prompt = "以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\nSample markdown content"

        # Mock the OpenAI client and its response
        #self.llm.client.chat.completions.create = MagicMock(return_value={"choices": [{"message": {"content": "Generated report"}}]})
        # Mock the OpenAI client and its response
        self.llm.client.chat.completions.create = MagicMock(return_value=self.dict_to_mock({
            "choices": [
                {
                    "message": {
                        "content": "Generated report"
                    }
                }
            ]
        }))

        # Call the method under test
        result = self.llm.generate_daily_report(markdown_content)

        # Assert the expected prompt and response
        self.llm.client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": expected_prompt}]
        )
        self.assertEqual(result, "Generated report")

    # 非mock测试, dry_run
    def test_generate_daily_report_dry_run(self):
        markdown_content = "Sample markdown content"
        expected_prompt = "以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\nSample markdown content"
        result = self.llm.generate_daily_report(markdown_content, dry_run=True)
        self.assertEqual(result, "DRY RUN")
        with open("prompts/report_prompt.txt", "r") as f:
            prompt = f.read()
        self.assertEqual(prompt, expected_prompt)

    # 非mock测试, 生成报告
    def test_generate_daily_report(self):
        markdown_content = "Sample markdown content"
        result = self.llm.generate_daily_report(markdown_content)
        print(result)

if __name__ == '__main__':
    unittest.main()