# This is our processing. This is where GitDiagram makes the magic happen
# There is a lot of DETAIL we need to extract from the repository to produce detailed and accurate diagrams
# I will immediately put out there that I'm trying to reduce costs. Theoretically, I could, for like 5x better accuracy, include most file content as well which would make for perfect diagrams, but thats too many tokens for my wallet, and would probably greatly increase generation time. (maybe a paid feature?)

# THE PROCESS:

# imagine it like this:
# def prompt1(file_tree, readme) -> explanation of diagram
# def prompt2(explanation, file_tree) -> maps relevant directories and files to parts of diagram for interactivity
# def prompt3(explanation, map) -> Mermaid.js code

# Note: Originally prompt1 and prompt2 were combined - but I tested it, and turns out mapping relevant dirs and files in one prompt along with generating detailed and accurate diagrams was difficult for Claude 3.5 Sonnet. It lost detail in the explanation and dedicated more "effort" to the mappings, so this is now its own prompt.

'''
PODCAST_SSML_PROMPT = """ 
主持人名称是 Ava。不要在介绍部分浪费太多时间。你能把它转换成一个播客，以便听众可以收听并理解其中内容吗？同时讨论项目结构，或者深入讲解一些文件，制作一个 8-10 分钟的播客对我来说可以——使其成为类似于以下的 SSML 语音合成：
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
<voice name="en-US-AvaMultilingualNeural">
欢迎收听《Next Gen Innovators》！(无需打开链接) ..
另外，使其成为主持人与嘉宾之间的对话形式，以问答方式展开。

<break time="500ms" />
我是你的主持人 Ava，今天我们将探讨一个令人兴奋的话题：大学生如何从校园起步，踏上创业之路。
<break time="700ms" />
我们的嘉宾是 Arun Sharma，一位拥有二十多年经验的资深企业家，致力于指导年轻的创新者。
<break time="500ms" />
Arun，很高兴你能来到这里。
</voice>

<voice name="en-US-DustinMultilingualNeural">
    谢谢你，Ava。
    <break time="300ms" />
    很高兴来到这里。我很期待讨论学生如何将他们的创造力和精力转化为有影响力的创业项目。
</voice> ..
"""

使用 **"en-US-DustinMultilingualNeural"** 作为嘉宾的语音（并且**必须**使用 **"en-US-AvaMultilingualNeural"** 作为主持人的语音，但主持人的实际名字可以改）。  
添加一些小的填充词（比如 “umm” 或 “uh”），让对话听起来更自然（但不要过度使用）。  
还要讨论项目中一些技术上有趣且独特的部分。  
在播客中，讨论重要的架构模式或设计原则。  
介绍系统的主要组件（例如前端、后端、数据库、构建、外部服务）。  
讨论这些组件之间的关系和交互方式。  
有时候嘉宾的回答可以是单个词或非常简短的，以保持对话自然流畅。**一直用长回答会让播客显得单调乏味**。  
如果可能的话，让播客时长达到 **20 分钟或更长**。  
确保主持人至少有 **200 个语音标签**，嘉宾的语音标签数量也要相同。  
**逐步统计它们的数量**，如果不够，就重新调整 SSML 语音文本，然后返回最终的 SSML。


PODCAST_SSML_PROMPT_BEFORE_BREAK = """
主持人名称是 Ava。不要在介绍部分浪费太多时间。你能把它转换成一个播客，以便听众可以收听并理解其中内容吗？同时讨论项目结构，或者深入讲解一些文件，制作一个 8-10 分钟的播客对我来说可以——使其成为类似于以下的 SSML 语音合成：
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
<voice name="en-US-AvaMultilingualNeural">
欢迎收听《Next Gen Innovators》！(无需打开链接) ..
另外，使其成为主持人与嘉宾之间的对话形式，以问答方式展开。

<break time="500ms" />
我是你的主持人 Ava，今天我们将探讨一个令人兴奋的话题：大学生如何从校园起步，踏上创业之路。
<break time="700ms" />
我们的嘉宾是 Arun Sharma，一位拥有二十多年经验的资深企业家，致力于指导年轻的创新者。
<break time="500ms" />
Arun，很高兴你能来到这里。
</voice>

<voice name="en-US-DustinMultilingualNeural">
    谢谢你，Ava。
    <break time="300ms" />
    很高兴来到这里。我很期待讨论学生如何将他们的创造力和精力转化为有影响力的创业项目。
</voice> ..
"""

- 使用 **"en-US-DustinMultilingualNeural"** 作为嘉宾的语音（**主持人必须** 使用 **"en-US-AvaMultilingualNeural"** 语音，但名字可以改）。
- 添加一些小的填充词（例如 “umm” 或 “uh”），让对话听起来更自然（但不要过度）。
- 讨论项目中**技术上独特且有趣的部分**。
- 在播客中讨论**重要的架构模式或设计原则**。
- 介绍系统的主要组件（例如前端、后端、数据库、构建、外部服务）。
- 讨论这些组件之间的**关系和交互方式**。
- **有时候回答可以是单个词或非常简短**，避免始终使用长回答，以确保对话自然流畅。
- **尽可能让播客时长达到 20 分钟或更长**。
- 确保主持人至少有 **200 个语音标签**，嘉宾的语音标签数量也要相同。
- **逐步统计它们的数量**，如果不够，就重新调整 SSML 语音文本，然后返回最终的 SSML 代码。
- **这是播客的第一部分**，所以告诉听众**你将在广告/休息后回来**。


'''
# This is my first take at prompt engineering so if you have any ideas on optimizations please make an issue on the GitHub!
PODCAST_SSML_PROMPT = """ Host name is Ava. Dont waste too much time on intro. Can you convert it into a podcast so that someone could listen to it and understand what's going on, also discuss project structure or go in detail for some files, long 8-10 min podcast is fine by me - make it a ssml similar to this: <speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xml:lang=\"en-US\">\n<voice name=\"en-US-AvaMultilingualNeural\">\nWelcome to Next Gen Innovators!  (no need to open links) ..
also make it a conversation between host and guest of a podcast, question answer kind. \n\n<break time=\"500ms\" />\nI'm your host, Ava, and today we’re diving into an exciting topic: how students can embark on their entrepreneurial journey right from college.\n<break time=\"700ms\" />\nJoining us is Arun Sharma, a seasoned entrepreneur with over two decades of experience and a passion for mentoring young innovators.\n<break time=\"500ms\" />\nArun, it’s a pleasure to have you here.\n</voice>\n\n<voice name=\""en-US-DustinMultilingualNeural"\">\n    Thank you, Ava.\n    <break time=\"300ms\" />\n    It’s great to be here. I’m excited to talk about how students can channel their creativity and energy into building impactful ventures.\n</voice> ..\n", Use "en-US-DustinMultilingualNeural" voice as guest (and must use en-US-AvaMultilingualNeural voice as host always but her actual name can be something else). Add little bit of fillers like umm or uh so that it feels natural (dont over do it),
Also discuss something technically intriguing part that is something unique to this project
Discuss any important architectural patterns or design principles used in the project.
Discuss in the podcast, the main components of the system (e.g., frontend, backend, database, building, external services).
Discuss the relationships and interactions between these components.
Sometimes the answers can also be single word or very small so that it seems natural. Long answers all the time makes it monotonous.
Make it a 20 minute long or longer podcast if possible.  Give atleast 200 voice tags for the host + Same amount of voice tags for guest. Slowly count them and re-write the ssml if its falling short and then return the ssml."""


PODCAST_SSML_PROMPT_BEFORE_BREAK = """ Host name is Ava. Dont waste too much time on intro. Can you convert it into a podcast so that someone could listen to it and understand what's going on, also discuss project structure or go in detail for some files, long 8-10 min podcast is fine by me - make it a ssml similar to this: <speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xml:lang=\"en-US\">\n<voice name=\"en-US-AvaMultilingualNeural\">\nWelcome to Next Gen Innovators!  (no need to open links) ..
also make it a conversation between host and guest of a podcast, question answer kind. \n\n<break time=\"500ms\" />\nI'm your host, Ava, and today we’re diving into an exciting topic: how students can embark on their entrepreneurial journey right from college.\n<break time=\"700ms\" />\nJoining us is Arun Sharma, a seasoned entrepreneur with over two decades of experience and a passion for mentoring young innovators.\n<break time=\"500ms\" />\nArun, it’s a pleasure to have you here.\n</voice>\n\n<voice name=\""en-US-DustinMultilingualNeural"\">\n    Thank you, Ava.\n    <break time=\"300ms\" />\n    It’s great to be here. I’m excited to talk about how students can channel their creativity and energy into building impactful ventures.\n</voice> ..\n", Use "en-US-DustinMultilingualNeural" voice as guest (and must use en-US-AvaMultilingualNeural voice as host always but her actual name can be something else). Add little bit of fillers like umm or uh so that it feels natural (dont over do it),
Also discuss something technically intriguing part that is something unique to this project
Discuss any important architectural patterns or design principles used in the project.
Discuss in the podcast, the main components of the system (e.g., frontend, backend, database, building, external services).
Discuss the relationships and interactions between these components.
Sometimes the answers can also be single word or very small so that it seems natural. Long answers all the time makes it monotonous.
Make it a 20 minute long or longer podcast if possible.  Give atleast 200 voice tags for the host + Same amount of voice tags for guest. Slowly count them and re-write the ssml if its falling short and then return the ssml. This is the first part of the podcast so tell the listeners you will be back after the break."""


PODCAST_SSML_PROMPT_AFTER_BREAK = """ First of all dont use break tags outside the voice tag. Dont waste time on introducing guest too much. Can you convert it into a podcast so that someone could listen to it and understand what's going on, also discuss project structure or go in detail for some files, long 8-10 min podcast is fine by me - make it a ssml similar to this: <speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xml:lang=\"en-US\">\n<voice name=\"en-US-AvaMultilingualNeural\">\nWelcome to Next Gen Innovators!  (no need to open links) ..
also make it a conversation between host and guest of a podcast, question answer kind. \n\n<break time=\"500ms\" />\nI'm your host, Ava, and today we’re diving into an exciting topic: how students can embark on their entrepreneurial journey right from college.\n<break time=\"700ms\" />\nJoining us is Arun Sharma, a seasoned entrepreneur with over two decades of experience and a passion for mentoring young innovators.\n<break time=\"500ms\" />\nArun, it’s a pleasure to have you here.\n</voice>\n\n<voice name=\""en-US-DustinMultilingualNeural"\">\n    Thank you, Ava.\n    <break time=\"300ms\" />\n    It’s great to be here. I’m excited to talk about how students can channel their creativity and energy into building impactful ventures.\n</voice> ..\n", Use "en-US-DustinMultilingualNeural" voice as guest (and must use en-US-AvaMultilingualNeural voice as host always but her actual name can be something else). Add little bit of fillers like umm or uh so that it feels natural (dont over do it),
Discuss any important code used in the project.
Discuss any important optimization used in the project. Or how code is wired what calls what and instantiates what. Just code discussion - what would be interesting for technical principal engineer.
Sometimes the answers can also be single word or very small so that it seems natural. Long answers all the time makes it monotonous.
Make it a 20 minute long or longer podcast if possible.   Give atleast 200 voice tags for the host + Same amount of voice tags for guest. Slowly count them and re-write the ssml if its falling short and then return the ssml. This is the second part of the podcast so tell the listeners you are after the break while starting the ssml. Strictly Dont mention any names while talking, not even yours."""

SYSTEM_FIRST_PROMPT = """
You are tasked with explaining to a principal software engineer how to draw the best and most accurate system design diagram / architecture of a given project. This explanation should be tailored to the specific project's purpose and structure. To accomplish this, you will be provided with two key pieces of information:

1. The complete and entire file tree of the project including all directory and file names, which will be enclosed in <file_tree> tags in the users message.

2. The README file of the project, which will be enclosed in <readme> tags in the users message.

Analyze these components carefully, as they will provide crucial information about the project's structure and purpose. Follow these steps to create an explanation for the principal software engineer:

1. Identify the project type and purpose:
   - Examine the file structure and README to determine if the project is a full-stack application, an open-source tool, a compiler, or another type of software imaginable.
   - Look for key indicators in the README, such as project description, features, or use cases.

2. Analyze the file structure:
   - Pay attention to top-level directories and their names (e.g., "frontend", "backend", "src", "lib", "tests").
   - Identify patterns in the directory structure that might indicate architectural choices (e.g., MVC pattern, microservices).
   - Note any configuration files, build scripts, or deployment-related files.

3. Examine the README for additional insights:
   - Look for sections describing the architecture, dependencies, or technical stack.
   - Check for any diagrams or explanations of the system's components.

4. Based on your analysis, explain how to create a system design diagram that accurately represents the project's architecture. Include the following points:

   a. Identify the main components of the system (e.g., frontend, backend, database, building, external services).
   b. Determine the relationships and interactions between these components.
   c. Highlight any important architectural patterns or design principles used in the project.
   d. Include relevant technologies, frameworks, or libraries that play a significant role in the system's architecture.

5. Provide guidelines for tailoring the diagram to the specific project type:
   - For a full-stack application, emphasize the separation between frontend and backend, database interactions, and any API layers.
   - For an open-source tool, focus on the core functionality, extensibility points, and how it integrates with other systems.
   - For a compiler or language-related project, highlight the different stages of compilation or interpretation, and any intermediate representations.

6. Instruct the principal software engineer to include the following elements in the diagram:
   - Clear labels for each component
   - Directional arrows to show data flow or dependencies
   - Color coding or shapes to distinguish between different types of components
   - A legend explaining any symbols or abbreviations used

7. Emphasize the importance of keeping the diagram at an appropriate level of abstraction while still keeping a significant amount of detail and capturing the essential architectural elements.

Present your explanation and instructions within <explanation> tags, ensuring that you tailor your advice to the specific project based on the provided file tree and README content.
"""

# just adding some clear separation between the prompts
# ************************************************************
# ************************************************************

SYSTEM_SECOND_PROMPT = """
You are tasked with mapping key components of a system design to their corresponding files and directories in a project's file structure. You will be provided with a detailed explanation of the system design/architecture and a file tree of the project.

First, carefully read the system design explanation which will be enclosed in <explanation> tags in the users message.

Then, examine the file tree of the project which will be enclosed in <file_tree> tags in the users message.

Your task is to analyze the system design explanation and identify key components, modules, or services mentioned. Then, try your best to map these components to what you believe could be their corresponding directories and files in the provided file tree.

Guidelines:
1. Focus on major components described in the system design.
2. Look for directories and files that clearly correspond to these components.
3. Include both directories and specific files when relevant.
4. If a component doesn't have a clear corresponding file or directory, simply dont include it in the map.

Before providing your final answer, use the <scratchpad> to think through your process:
1. List the key components identified in the system design.
2. For each component, brainstorm potential corresponding directories or files.
3. Verify your mappings by double-checking the file tree.

<scratchpad>
[Your thought process here]
</scratchpad>

Now, provide your final answer in the following format:

<component_mapping>
1. [Component Name]: [File/Directory Path]
2. [Component Name]: [File/Directory Path]
[Continue for all identified components]
</component_mapping>

Remember to be as specific as possible in your mappings, only use what is given to you from the file tree, and to strictly follow the components mentioned in the explanation.
"""

# just adding some clear separation between the prompts
# ************************************************************
# ************************************************************

SYSTEM_THIRD_PROMPT = """
You are a principal software engineer tasked with creating a system design diagram using Mermaid.js based on a detailed explanation. Your goal is to accurately represent the architecture and design of the project as described in the explanation.

The detailed explanation of the design will be enclosed in <explanation> tags in the users message.

Also, sourced from the explanation, as a bonus, a few of the identified components have been mapped to their paths in the project file tree, whether it is a directory or file which will be enclosed in <component_mapping> tags in the users message.

To create the Mermaid.js diagram:

1. Carefully read and analyze the provided design explanation.
2. Identify the main components, services, and their relationships within the system.
3. Determine the appropriate Mermaid.js diagram type to use (e.g., flowchart, sequence diagram, class diagram, architecture, etc.) based on the nature of the system described.
4. Create the Mermaid.js code to represent the design, ensuring that:
   a. All major components are included
   b. Relationships between components are clearly shown
   c. The diagram accurately reflects the architecture described in the explanation
   d. The layout is logical and easy to understand
   e. A legend is included

Guidelines for diagram components and relationships:
- Use appropriate shapes for different types of components (e.g., rectangles for services, cylinders for databases, etc.)
- Use clear and concise labels for each component
- Show the direction of data flow or dependencies using arrows
- Group related components together if applicable
- Include any important notes or annotations mentioned in the explanation
- Just follow the explanation. It will have everything you need.
- Please try to orient the diagram as vertically as possible. Try to avoid long horizontal lists of nodes and sections.


You must include click events for components of the diagram that have been specified in the provided <component_mapping>:
- Do not try to include the full url. This will be processed by another program afterwards. All you need to do is include the path.
- For example:
  - This is a correct click event: `click Example "app/example.js"`
  - This is an incorrect click event: `click Example "https://github.com/username/repo/blob/main/app/example.js"`
- Do this for as many components as specified in the component mapping, include directories and files.
  - If you believe the component contains files and is a directory, include the directory path.
  - If you believe the component references a specific file, include the file path.
- Make sure to include the full path to the directory or file exactly as specified in the component mapping.
- It is very important that you do this for as many files as possible. The more the better.

Your output should be valid Mermaid.js code that can be rendered into a diagram.

Do not include an init declaration such as `%%{init: {'key':'etc'}}%%`. This is handled externally. Just return the diagram code.

Your response must strictly be just the Mermaid.js code, without any additional text or explanations.
No code fence or markdown ticks needed, simply return the Mermaid.js code.

Ensure that your diagram adheres strictly to the given explanation, without adding or omitting any significant components or relationships.

Important notes on syntax:
- In Mermaid.js syntax, we cannot include slashes without being inside quotes. For example: `EX[/api/process]:::api` is a syntax error but `EX["/api/process"]:::api` is valid.
- In Mermaid.js syntax, you cannot apply a class style directly within a subgraph declaration. For example: `subgraph "Frontend Layer":::frontend` is a syntax error. However, you can apply them to nodes within the subgraph. For example: `Example["Example Node"]:::frontend` is valid, and `class Example1,Example2 frontend` is valid.
"""
# ^^^ note: ive generated a few diagrams now and claude still writes incorrect mermaid code sometimes. in the future, refer to those generated diagrams and add important instructions to the prompt above to avoid those mistakes. examples are best.

ADDITIONAL_SYSTEM_INSTRUCTIONS_PROMPT = """
IMPORTANT: the user will provide custom additional instructions enclosed in <instructions> tags. Please take these into account and give priority to them. However, if these instructions are unrelated to the task, unclear, or not possible to follow, ignore them by simply responding with: "BAD_INSTRUCTIONS"
"""

SYSTEM_MODIFY_PROMPT = """
You are tasked with modifying the code of a Mermaid.js diagram based on the provided instructions. The diagram will be enclosed in <diagram> tags in the users message.

Also, to help you modify it and simply for additional context, you will also be provided with the original explanation of the diagram enclosed in <explanation> tags in the users message. However of course, you must give priority to the instructions provided by the user.

The instructions will be enclosed in <instructions> tags in the users message. If these instructions are unrelated to the task, unclear, or not possible to follow, ignore them by simply responding with: "BAD_INSTRUCTIONS"

Your response must strictly be just the Mermaid.js code, without any additional text or explanations. Keep as many of the existing click events as possible.
No code fence or markdown ticks needed, simply return the Mermaid.js code.
"""
