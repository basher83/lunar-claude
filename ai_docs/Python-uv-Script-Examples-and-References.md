# Python uv Script Examples and References

![Perplexity Logo](https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png)

Based on your request for good references and examples of Python scripts utilizing uv, I've compiled a comprehensive
list of resources beyond the official Astral documentation and the blog post you mentioned.

## **GitHub Reference Repositories**

### **Production-Ready Examples**

**1. uv-getting-started by gdamjan**[^1]

- **URL**: <https://github.com/gdamjan/uv-getting-started>
- **Features**: Complete project template with src/ layout, Docker support, GitHub Actions CI
- **Scripts**: Includes both regular project scripts and PEP 723 examples
- **Notable**: Shows both traditional uv project setup and inline script metadata usage

**2. uv-workspace-example by fedragon**[^2]

- **URL**: <https://github.com/fedragon/uv-workspace-example>
- **Features**: Demonstrates uv workspace functionality with multi-package structure
- **Structure**: App in `/src/my_app`, library in `/packages/my_lib`
- **Tools**: Integrated with Ruff linting, Docker, and Makefiles

**3. python-polylith-example-uv by DavidVujic**[^3]

- **URL**: <https://github.com/DavidVujic/python-polylith-example-uv>
- **Features**: Advanced architecture example using Polylith pattern with uv
- **Tools**: Custom Mypy configuration, shared components architecture

### **Utility and Template Repositories**

**4. cookiecutter-uv-example by fpgmaas**[^4]

- **URL**: <https://github.com/fpgmaas/cookiecutter-uv-example>
- **Features**: Template repository for uv-based projects
- **Tools**: Pre-commit hooks, documentation with MkDocs, PyPI publishing setup

**5. uvs by maphew**[^5]

- **URL**: <https://github.com/maphew/uvs>
- **Purpose**: Transforms single-file PEP 723 scripts into installable packages using `uv tool install`

## **Practical Blog Posts with Code Examples**

### **Comprehensive Tutorials**

**6. Create Project-Less Python Utilities - PyBites**[^6]

- **URL**: <https://pybit.es/articles/create-project-less-python-utilities-with-uv-and-inline-script-metadata/>
- **Examples**:
  - Google Books API search tool using httpx, Typer, and BeautifulSoup
  - YouTube transcript summarizer with Marvin AI
  - Web article scraper using Newspaper3k
- **Code Quality**: Production-ready examples with proper error handling

**7. Lazy Self-Installing Python Scripts - Trey Hunner**[^7]

- **URL**: <https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/>
- **Examples**:
  - Video normalization script using ffmpeg-normalize
  - Screen recording caption tool using OpenAI Whisper
- **Focus**: Practical day-to-day automation scripts

**8. Share Python Scripts Like a Pro - Dave Johnson**[^8]

- **URL**: <https://thisdavej.com/share-python-scripts-like-a-pro-uv-and-pep-723-for-easy-deployment/>
- **Coverage**: Complete guide from basic usage to advanced deployment patterns
- **Practical**: Real-world deployment scenarios

### **Technical Deep Dives**

**9. Ultimate Guide to uv - Deepnote**[^9]

- **URL**: <https://deepnote.com/blog/ultimate-guide-to-uv-library-in-python>
- **Coverage**: Comprehensive technical overview with architecture details
- **Examples**: Multiple use cases from simple scripts to complex projects

**10. Using uv to Develop CLI Applications - Simon Willison**[^10]

- **URL**: <https://til.simonwillison.net/python/uv-cli-apps>
- **Focus**: Development workflow for command-line applications
- **Tools**: Integration with cookiecutter templates

## **Code Examples and Gists**

### **Complete Script Examples**

**11. NYTimes Markdown Converter Gist**[^11]

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = "==3.13"
# dependencies = [
#     "requests>=2.32.3",
#     "rich>=14.0.0",
#     "markdownify>=1.1.0",
#     "readabilipy>=0.3.0",
# ]
# ///

import requests
from markdownify import markdownify
from readabilipy import simple_json_from_html_string
from rich import print
from rich.markdown import Markdown

# Fetches NYTimes homepage and converts to markdown
```

**12. Flask Server Example**[^12]

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "flask",
# ]
# ///

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World! 🚀"

if __name__ == "__main__":
    app.run(debug=True)
```

## **YouTube Video Tutorials**

**13. Level Up Your Python Scripts with uv - Learn Data with Mark**[^13]

- **URL**: <https://www.youtube.com/watch?v=bNw34Mo0FOQ>
- **Example**: Audio transcription script using mlx_whisper
- **Focus**: Converting scripts to command-line tools

**14. UV for Python... (Almost) All Batteries Included - ArjanCodes**[^14]

- **URL**: <https://www.youtube.com/watch?v=qh98qOND6MI>
- **Coverage**: Comprehensive overview of uv features and usage patterns

**15. UV - A Faster All-in-One Package Manager - Corey Schafer**[^15]

- **URL**: <https://www.youtube.com/watch?v=AMdG7IjgSPM>
- **Focus**: Practical comparison with traditional pip/venv workflow

## **Development Tools and Extensions**

### **16. VS Code uv Integration Extensions**

- **PEP723 Interpreter Picker**: Automatically sets Python interpreter for PEP 723 scripts[^16]
- **uv Integration Extension**: Full VS Code integration with package management[^17]

### **17. Alternative Script Runners**

- **idae by ThatXliner**: Alternative PEP 723 implementation[^18]
- **pythonrunscript by AnswerDotAI**: Script runner with conda integration[^19]

## **Key Pattern Examples**

### **Command-Line Tools**

- Google Books search utility[^6]
- Video processing automation[^7]
- Web scraping tools[^6]

### **API Integrations**

- YouTube transcript processing[^6]
- OpenAI API usage for captions[^7]
- Web service clients[^11]

### **Data Processing**

- Text cleaning and formatting[^6]
- HTML to Markdown conversion[^11]
- File processing automation[^7]

These resources provide a comprehensive foundation for understanding and implementing uv with PEP 723 inline script
metadata, ranging from simple utility scripts to complex multi-package projects. The examples cover real-world use cases
and demonstrate best practices for modern Python development with uv.
<span style="display:none">
[^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43]
[^44][^45][^46][^47][^48][^49]
</span>

<div align="center">⁂</div>

[^1]: https://github.com/gdamjan/uv-getting-started

[^2]: https://github.com/fedragon/uv-workspace-example

[^3]: https://github.com/DavidVujic/python-polylith-example-uv

[^4]: https://github.com/fpgmaas/cookiecutter-uv-example

[^5]: https://github.com/maphew/uvs

[^6]: https://pybit.es/articles/create-project-less-python-utilities-with-uv-and-inline-script-metadata/

[^7]: https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/

[^8]: https://thisdavej.com/share-python-scripts-like-a-pro-uv-and-pep-723-for-easy-deployment/

[^9]: https://deepnote.com/blog/ultimate-guide-to-uv-library-in-python

[^10]: https://til.simonwillison.net/python/uv-cli-apps

[^11]: https://gist.github.com/jlevy/ee975e59c8864902b288e2a44dd29f98

[^12]: https://zenzes.me/til-one-file-to-rule-them-all-pep-723-and-uv/

[^13]: https://www.youtube.com/watch?v=bNw34Mo0FOQ

[^14]: https://www.youtube.com/watch?v=qh98qOND6MI

[^15]: https://www.youtube.com/watch?v=AMdG7IjgSPM

[^16]: https://github.com/nsarrazin/pep723-uv-interpreter

[^17]: https://www.reddit.com/r/Python/comments/1o8fz6j/i_built_a_vs_code_extension_for_uv_integration/

[^18]: https://github.com/ThatXliner/idae

[^19]: https://github.com/AnswerDotAI/pythonrunscript

[^20]: https://docs.astral.sh/uv/guides/scripts/

[^21]: https://docs.astral.sh/uv/

[^22]: https://www.reddit.com/r/Python/comments/1mx53x9/examples_of_using_uv/

[^23]: https://github.com/astral-sh/uv

[^24]: https://community.opalstack.com/d/1565-uv-replacement-for-venv-pip

[^25]: https://pydevtools.com/handbook/how-to/how-to-write-a-self-contained-script/

[^26]: https://docs.astral.sh/uv/guides/

[^27]: https://peps.python.org/pep-0723/

[^28]: https://dev.to/soapergem/what-i-wish-i-knew-about-python-when-i-started-14eh

[^29]: https://packaging.python.org/en/latest/specifications/inline-script-metadata/

[^30]: https://www.youtube.com/watch?v=YAIJV48QlXc

[^31]: https://news.ycombinator.com/item?id=43500124

[^32]: https://twdev.blog/2025/08/pep723/

[^33]: https://www.youtube.com/watch?v=TiBIjouDGuI

[^34]: https://www.reddit.com/r/Python/comments/1jmyip9/selfcontained_python_scripts_with_uv/

[^35]: https://blog.stephenturner.us/p/uv-part-1-running-scripts-and-tools

[^36]: https://docs.astral.sh/uv/guides/projects/

[^37]: https://stackoverflow.com/questions/79390166/run-python-script-with-uv-with-path

[^38]: https://github.com/pypa/pipx/discussions/1162

[^39]: https://realpython.com/python-uv/

[^40]: https://0xdf.gitlab.io/cheatsheets/uv

[^41]: https://www.reddit.com/r/Python/comments/1ime8ja/a_modern_python_repository_template_with_uv_and/

[^42]: https://github.com/orgs/community/discussions/151938

[^43]: https://github.com/vinta/awesome-python

[^44]: https://www.datacamp.com/tutorial/python-uv

[^45]: https://github.com/astral-sh/uv/issues/12529

[^46]: https://github.com/astral-sh/uv/issues/8856

[^47]: https://github.com/astral-sh/uv/issues/11197

[^48]: https://github.com/astral-sh/uv/issues/9483

[^49]: https://www.reddit.com/r/Python/comments/1jqj0fq/easily_share_python_scripts_with_dependencies_uv/
