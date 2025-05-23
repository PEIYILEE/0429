import os
import warnings
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
from utils import get_openai_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# 定義 Agents
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article about the topic: {topic}. "
              "You collect information that helps the audience learn something "
              "and make informed decisions. Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
    backstory="You're working on writing a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and direction of the outline, "
              "as provided by the Content Planner. "
              "You also provide objective and impartial insights and back them up with information "
              "provided by the Content Planner. "
              "You acknowledge in your opinion piece when your statements are opinions "
              "as opposed to objective statements.",
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with the writing style of the organization.",
    backstory="You are an editor who receives a blog post from the Content Writer. "
              "Your goal is to review the blog post to ensure that it follows journalistic best practices, "
              "provides balanced viewpoints when providing opinions or assertions, "
              "and also avoids major controversial topics or opinions when possible.",
    allow_delegation=False,
    verbose=True
)

# ⚡ 新增可以接收「使用者輸入」並正確替換 {topic} 的 function
def run_multi_agent(user_topic):
    # 動態定義 Tasks，這邊自己把 {topic} 換掉
    plan = Task(
        description=(
            f"1. Prioritize the latest trends, key players, and noteworthy news on {user_topic}.\n"
            f"2. Identify the target audience, considering their interests and pain points.\n"
            f"3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
            f"4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
        agent=planner,
    )

    write = Task(
        description=(
            f"1. Use the content plan to craft a compelling blog post on {user_topic}.\n"
            f"2. Incorporate SEO keywords naturally.\n"
            f"3. Sections/Subtitles are properly named in an engaging manner.\n"
            f"4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
            f"5. Proofread for grammatical errors and alignment with the brand's voice.\n"
        ),
        expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        agent=writer,
    )

    edit = Task(
        description=(
            f"Proofread the given blog post about {user_topic} for grammatical errors and alignment with the brand's voice."
        ),
        expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        agent=editor,
    )

    # 動態建立 Crew
    dynamic_crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        verbose=2
    )

    # 執行 multi-agent 並取得結果
    result = dynamic_crew.kickoff()

    return result
