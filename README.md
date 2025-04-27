# AWS Voice Agent

## NOTICE
Fork from [https://github.com/Chen188/TEN-Agent](https://github.com/Chen188/TEN-Agent)


![Astra banner image](https://github.com/TEN-framework/docs/blob/main/assets/jpg/astra_banner.jpg?raw=true)
<div align="center">

[![Follow on X](https://img.shields.io/twitter/follow/AstraAIAgent?logo=X&color=%20%23f5f5f5)](https://twitter.com/intent/follow?screen_name=AstraAIAgent)
![Product fee](https://img.shields.io/badge/pricing-free-blue.svg?labelColor=%20%239b8afb&color=%20%237a5af8)
[![Discussion posts](https://img.shields.io/github/discussions/TEN-framework/astra.ai?labelColor=%20%23FDB062&color=%20%23f79009)](https://github.com/TEN-framework/astra.ai/discussions/)
[![Commits](https://img.shields.io/github/commit-activity/m/TEN-framework/astra.ai?labelColor=%20%237d89b0&color=%20%235d6b98)](https://github.com/TEN-framework/astra.ai/graphs/commit-activity)
[![Issues closed](https://img.shields.io/github/issues-search?query=repo%3ATEN-framework%2Fastra.ai%20is%3Aclosed&label=issues%20closed&labelColor=green&color=green)](https://github.com/TEN-framework/ASTRA.ai/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/TEN-framework/ASTRA.ai/pulls)
[![GitHub license](https://img.shields.io/badge/License-Apache_2.0-blue.svg?labelColor=%20%23155EEF&color=%20%23528bff)](https://github.com/TEN-framework/ASTRA.ai/blob/main/LICENSE)

[![Discord TEN Community](https://dcbadge.vercel.app/api/server/VnPftUzAMJ)](https://discord.gg/VnPftUzAMJ)

[![GitHub watchers](https://img.shields.io/github/watchers/TEN-framework/astra.ai?style=social&label=Watch)](https://GitHub.com/TEN-framework/astra.ai/watchers/?WT.mc_id=academic-105485-koreyst)
[![GitHub forks](https://img.shields.io/github/forks/TEN-framework/astra.ai?style=social&label=Fork)](https://GitHub.com/TEN-framework/astra.ai/network/?WT.mc_id=academic-105485-koreyst)
[![GitHub stars](https://img.shields.io/github/stars/TEN-framework/astra.ai?style=social&label=Star)](https://GitHub.com/TEN-framework/astra.ai/stargazers/?WT.mc_id=academic-105485-koreyst)

<a href="https://github.com/Chen188/ASTRA.ai/blob/main/README.md"><img alt="README in English" src="https://img.shields.io/badge/English-lightgrey"></a>
<a href="https://github.com/Chen188/astra.ai/blob/main/docs/readmes/README-CN.md"><img alt="简体中文操作指南" src="https://img.shields.io/badge/简体中文-lightgrey"></a>


[Documentation](https://doc.theten.ai)
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
[Getting Started](https://doc.theten.ai/getting-started/quickstart)
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
[Tutorials](https://doc.theten.ai/getting-started/create-a-hello-world-extension)

</div>

<br>
<h2>Astra Agent</h2>

[Astra multimodal agent](https://theastra.ai)

Astra is a multimodal agent powered by [ TEN ](https://doc.theten.ai), demonstrating its capabilities in speech, vision, and reasoning through  RAG from local documentation.

[![Showcase Astra multimodal agent](https://github.com/TEN-framework/docs/blob/main/assets/gif/astra_voice_agent.gif?raw=true)](https://theastra.ai)
<br>
<h2>How to build Astra locally

### Prerequisites

#### Keys
- Agora [ App ID ](https://docs.agora.io/en/video-calling/get-started/manage-agora-account?platform=web#create-an-agora-project) and [ App Certificate ](https://docs.agora.io/en/video-calling/get-started/manage-agora-account?platform=web#create-an-agora-project)(certificate is not required)
- [AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) IAM User's Access key and Secret key

#### Installation
  - [Docker](https://www.docker.com/) / [Docker Compose](https://docs.docker.com/compose/)
  - [Node.js(LTS) v18](https://nodejs.org/en)

#### Minimum system requirements
  - CPU >= 2 Core
  - RAM >= 4 GB

#### Docker setting on Apple Silicon
You will need to uncheck "Use Rosetta for x86_64/amd64 emulation on Apple Silicon" option for Docker if you are on Apple Silicon, otherwise the server is not going to work.

![Docker Setting](https://github.com/TEN-framework/docs/blob/main/assets/gif/docker_setting.gif?raw=true)

### Next step

#### 1. Modify config files
In the root of the project, use `cp` command to create `.env` from the example.

It will be used to store information for `docker compose` later.
```bash
cp ./.env.example ./.env
```

#### 2. Setup API keys
Open the `.env` file and fill in the `keys` and `regions`. This is also where you can choose to use any different `extensions`:
```bash
# Agora App ID and Agora App Certificate
AGORA_APP_ID=
# Leave empty unless you have enabled the certificate within the Agora account.
AGORA_APP_CERTIFICATE=

# Extension: bedrock_llm
# Extension: polly_tts
# Extension: transcribe_asr
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# model id supported by Bedrock Converse API, the model you choose should support system prompt. https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
AWS_BEDROCK_MODEL=mistral.mistral-large-2407-v1:0

AWS_REGION=us-east-1 # the Region you're using
```

#### 3. Start agent development containers
In the same directory, run the `docker compose up` command to compose containers:
```bash
docker compose up
```

### Finish and verify 🎉

#### Astra multimodal agent
Open up http://localhost:3000 in browser to play and test the Astra agent.

#### Graph designer

Open up another tab go to http://localhost:3001, and use Graph Designer to create, connect and edit extensions on canvas.

![TEN Graph Designer](https://github.com/TEN-framework/docs/blob/main/assets/gif/graph_designer.gif?raw=true)

<br>
<h2>Astra Agent Comparison</h2>

<div align="center">

| **Features**                             | **Astra Agent** | **Pipecat** | **LiveKit:KITT** | **Vapi.ai** | **DailyBots** | **Play.ai** |
|:----------------------------------------:|:-------:|:--------:|:-------------:|:----------------:|:----------------:|:----------------:|
| **Vision**                               |   ✅    |    ❌    |      ❌       |     ❌     |     ❌      |     ❌       |
| **Rich TTS Support for different languages** |   ✅    |    ❌    |      ❌       |     ❌      |     ❌      |     ❌      |
| **Go support for extension**              |   ✅    |    ❌    |      ❌       |     ❌     |      ❌     |     ❌      |
| **C++ support for extension**             |   ✅    |    ❌    |      ❌       |     ❌     |      ❌     |     ❌      |
| **RAG support**                          |   ✅    |    ❌    |      ❌       |     ❌     |      ❌     |     ❌      |
| **Workflow builder for extension**        |   ✅    |    ❌    |      ❌       |     ✅      |     ❌     |     ❌      |
| **Rich LLM Support**                      |   ✅    |    ✅    |      ✅       |     ✅     |     ✅     |    ✅      |
| **Python support for extension**          |   ✅    |    ✅    |      ✅       |     ✅     |     ✅      |     ✅     |
| **Open source**                          |   ✅    |    ✅    |      ✅       |     ❌     |     ❌      |     ❌      |

</div>

<br>
<h2>Stay Tuned</h2>

Before we dive further, be sure to star our repository and get instant notifications for all new releases!

![TEN star us gif](https://github.com/TEN-framework/docs/blob/main/assets/gif/star_the_repo_confetti_higher_quality.gif?raw=true)

<br>
<h2>Join Community</h2>

- [Discord](https://discord.gg/VnPftUzAMJ): Ideal for sharing your applications and engaging with the community.
- [GitHub Discussion](https://github.com/TEN-framework/astra.ai/discussions): Perfect for providing feedback and asking questions.
- [GitHub Issues](https://github.com/TEN-framework/astra.ai/issues): Best for reporting bugs and proposing new features. Refer to our [contribution guidelines](./docs/code-of-conduct/contributing.md) for more details.
- [X (formerly Twitter)](https://img.shields.io/twitter/follow/AstraAIAgent?logo=X&color=%20%23f5f5f5): Great for sharing your agents and interacting with the community.


 <br>
 <h2>Code Contributors</h2>

[![TEN](https://contrib.rocks/image?repo=TEN-framework/astra.ai)](https://github.com/TEN-framework/astra.ai/graphs/contributors)

<br>
<h2>Contribution Guidelines</h2>

Contributions are welcome! Please read the [contribution guidelines](./docs/code-of-conduct/contributing.md) first.

<br>
<h2>License</h2>

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.