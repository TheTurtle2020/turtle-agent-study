from llm_client import HelloAgentsLLM
from tools import ToolExecutor, search
import re

# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """

你的角色：请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。

Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}

"""

class ReActAgent:
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def _print_step_header(self, step: int):
        print(f"\n🧭 第 {step} 步")

    def _print_message(self, title: str, content: str):
        content = content.strip()
        if not content:
            return
        print(f"\n[{title}]")
        print(content)

    # run 方法是智能体的入口。它的 while 循环构成了 ReAct 范式的主体，max_steps 参数则是一个重要的安全阀，防止智能体陷入无限循环而耗尽资源。
    def run(self, question: str):
        """
        运行ReAct智能体来回答一个问题。
        """
        self.history = [] # 每次运行时重置历史记录
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            self._print_step_header(current_step)

            # 1. 格式化提示词
            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc,
                question=question,
                history=history_str
            )

            # 2. 调用LLM进行思考
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)
            
            if not response_text:
                print("错误:LLM未能返回有效响应。")
                break
            
            self._print_message("🧠 模型回复", response_text)
            
            # 3. 解析LLM的输出
            thought, action = self._parse_output(response_text)
            
            if thought:
                self._print_message("💭 思考", thought)

            if not action:
                print("⚠️ 未能解析出有效的 Action，流程终止。")
                break

            # 4. 执行Action
            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                finish_match = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
                if finish_match:
                    final_answer = finish_match.group(1)
                    self._print_message("🎉 最终答案", final_answer)
                    return final_answer

                print("⚠️ 未能解析 Finish 指令中的最终答案。")
                return None
            
            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                # ... 处理无效Action格式 ...
                continue

            print(f"\n🛠️ 执行动作: {tool_name}[{tool_input}]")
            tool_function = self.tool_executor.getTool(tool_name)
            if not tool_function:
                observation = f"错误:未找到名为 '{tool_name}' 的工具。"
            else:
                observation = tool_function(tool_input) # 调用真实工具
            # 5. 打印观察结果
            self._print_message("👀 观察结果", observation)
            
            # 6. 将本轮的Action和Observation添加到历史记录中
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 循环结束
        print("\n🛑 已达到最大步数，流程终止。")
        return None


    # (这些方法是 ReActAgent 类的一部分)
    # 负责从LLM的完整响应中分离出Thought和Action两个主要部分。
    def _parse_output(self, text: str):
        """解析LLM的输出，提取Thought和Action。
        """
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    # 负责进一步解析Action字符串，例如从 Search[华为最新手机] 中提取出工具名 Search 和工具输入 华为最新手机。
    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名称和输入。
        """
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

if __name__ == '__main__':
    llm = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_desc, search)
    agent = ReActAgent(llm_client=llm, tool_executor=tool_executor)
    question = "苹果最新的airpods是哪一款？它的主要卖点是什么？"
    agent.run(question)