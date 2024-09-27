# VortexOSAI Quick Start

VortexOSAI (Open and Do Anything Now with AI) is revolutionizing the AI landscape with its Personal AI Operating System. Designed for seamless integration of diverse AI modules, it ensures unmatched interoperability. VortexOSAI empowers users to craft powerful AI agents—from butlers and assistants to personal tutors and digital companions—all while retaining control. These agents can team up to tackle complex challenges, integrate with existing services, and command smart(IoT) devices. 

With VortexOSAI, we're putting AI in your hands, making life simpler and smarter.

This project is still in its very early stages, and there may be significant changes in the future.

## Installation

VortexOSAI的Internal test版本有两种安装方式：
1.通过Docker安装，这也是我们现在推荐的安装方法
2.通过源代码安装，这种方法可能会遇到一些传统的Python依赖问题，需要你有一定的解决能力。但是如果你想要对VortexOSAI进行二次开发，这种方法是必须的。

### 安装前准备工作

1. Docker环境
VortexOSAI通过适配Docker实现了对多平台的适配。本文不介绍怎么安装Docker,在你的控制台下执行

```
docker --version
```

如果能够看到Docker的版本号（>20.0），说明你已经安装了Docker.
不知道怎么安装Docker的话，可以参考[这里](https://docs.docker.com/engine/install/)

2. OpenAI的API Token
如果你还没有API Token的话，可以通过[这里](https://beta.openai.com/)申请
（申请API Token对新玩家可能有一些门槛，可以在身边找找朋友，可以让他们给你一个临时的，或则加入我们的内测体验群，我们也会不时放出一些免费体验的API Token,这些Token被限制了最大消费和有效时间）

#### 安装VortexOSAI

执行下面的命令，就可以安装VortexOSAI的Docker Image了

```
docker pull paios/aios:latest
```

## 运行VortexOSAI

首次运行VortexOSAI需要进行初始化，初始化过程中会下载一些用于本地Knowledge Base库的基础模型，并需要你输入一些个人信息，因此启动Docker的时候记住要带上 -it参数。
VortexOSAI是你的Personal AIOS,其运行过程中会产生一些重要的个人数据（比如和Agent的对话记录，日程数据等），这些数据会保存在你的本地磁盘上，因此在启动Docker的时候，要将本地磁盘挂载到Docker的容器中，这样才能保证数据的持久化。

```
docker run -v /your/local/myai/:/root/myai --name aios -it paios/aios:latest 
```

在上述命令中，我们还为docker run创建的docker 实例起了一个名字叫aios,方便后续的操作。你也可以用自己喜欢的名字来代替

执行上述命令后，如果一切正常，你会看到如下界面
![MVP](./res/mvp.png)

首次运行完成Docker实例的创建后，再次运行只需要执行：

```
docker start -ai aios
```

如果打算以服务模式运行，则不用带 -ai参数：

```
docker start aios
```

## VortexOSAI的首次运行配置

如果你过去没有用字符界面(CLI)的产品，可能会有一点点不习惯。但别紧张，即使在Internal Test版本中，你也只会在极少数的情况下需要使用CLI。

VortexOSAI必须是所有人都能轻松使用的未来操作系统，因此我们希望VortexOSAI的使用和配置都是非常友好和简单的。但在Internal Test版本中，我们还没有足够的资源来实现这一目标。经过思考，我们决定先支持以CLI的方式来使用VortexOSAI。

VortexOSAI以LLM为AIOS的内核，通过不同的Agent/Workflow整合了很多很Cool的AI功能，你能在VortexOSAI里一站式的体验AI工业的一些最新的成功。激活全部的功能需要做比较多的配置，但首次运行我们只需要做两项配置就可以了

1. LLM内核。VortexOSAI是围绕LLM构建的未来智能操作系统，因此系统必须有至少一个LLM内核。
    VortexOSAI以Agent为单位对LLM进行配置，未指定LLM模型名的Agent将会默认使用GPT4（GPT4也是目前最聪明的LLM）。你可以修改该配置到llama或其它安装的Local LLM。今天使用Local LLM需要相当强的本地算力的支持，这需要一笔不小的一次性投入。
    但我们相信LLM领域也会遵循摩尔定律，未来的LLM模型会越来越强大，越来越小，越来越便宜。因此我们相信在未来，每个人都会有自己的Local LLM。
2. 你的个人信息，这能让你的私人AI管家Jarvis更好的为你服务。注意这里一定要输入你自己正确的Telegram username ,否则由于权限控制，后续将无法通过Telegram访问VortexOSAI上安装的Agent/Workflow。

好的，简单的了解了上述背景后，请按界面提示完成必要信息的输入。

P.S:
上述配置会保存在`/your/local/myai/etc/system.cfg.toml`中，如果你想要修改配置，可以直接修改这个文件。如果你想要调整配置，可以直接编辑这个文件。


## （实验性）安装本地LLM内核

首次快速体验VortexOSAI,我们强烈的推荐你使用GPT4，虽然它很慢，也很贵，但它也是目前最强大和稳定的LLM内核。VortexOSAI在架构设计上，允许不同的Agent选择不同的LLM内核（系统里至少要有一个可用的LLM内核），如果你因为各种原因无法使用GPT4，可以是用下面方法安装Local LLM让系统能跑起来。VortexOSAI是面向未来设计的系统，我们相信今天GPT4的能力一定会是未来所有LLM的下限。但目前的现实情况，其它的LLM不管是效果还是功能和GPT4都还有比较明显的差距，所以要完整体验VortexOSAI，在一定时间内，我们还是推荐使用GPT4.

目前我们只完成了基于Llama.cpp的Local LLM的适配，为VortexOSAI适配新的LLM内核并不是复杂的工作，有需要的工程师朋友可以自行扩展（记得给我们PR~）。如果你有一定的动手能力，可以用下面的方法安装基于Llama.cpp的Compute Node:

### 安装Llama.cpp ComputeNode

VortexOSAI支持分布式计算资源调度，因此你可以把LLaMa的计算节点安装在和VortexOSAI不同的机器上。根据模型的大小需要相当的算力支持，请根据自己的机器配置量力而行。我们使用llama.cpp构建LLaMa LLM ComputeNode,llama.cpp也是一个正在高速演化的项目，正致力降低LLM的运行需要的设备门槛，提高运行速度。请阅读llamap.cpp的项目了解其支持的各个模型的最低系统要求。


安装LLama.cpp 总共分两步：

Step1: 下载LLama.cpp的模型，有3个选择：7B-Chat,13B-Chat,70B-Chat. 我们的实践经验最少需要13B的才能工作。LLaMa2 目前官方的模型并不支持inner function call,而目前VortexOSAI的很多Agent都高度依赖inner function call.所以我们推荐您下载通过Fine-Tune 的 13B模型：

```
https://huggingface.co/Trelis/Llama-2-13b-chat-hf-function-calling
```

Step2 运行llama-cpp-python镜像

```
docker run --rm -it -p 8000:8000 -v /path/to/models:/models -e MODEL=/models/llama-2-13b-chat.gguf ghcr.io/abetlen/llama-cpp-python:latest
```

完成上述步骤后，如果输出如下，说明LLaMa已经正确加载模型并正常运行了
```
....................................................................................................
llama_new_context_with_model: kv self size  =  640.00 MB
llama_new_context_with_model: compute buffer total size =  305.47 MB
AVX = 1 | AVX2 = 1 | AVX512 = 0 | AVX512_VBMI = 0 | AVX512_VNNI = 0 | FMA = 1 | NEON = 0 | ARM_FMA = 0 | F16C = 1 | FP16_VA = 0 | WASM_SIMD = 0 | BLAS = 0 | SSE3 = 1 | SSSE3 = 1 | VSX = 0 | 
INFO:     Started server process [171]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 将LLama.cpp ComputeNode增加到VortexOSAI中

ComputeNode是VortexOSAI的底层组件，而且可能不会与VortexOSAI运行在同一个机器上。因此从依赖关系的角度，VortexOSAI并没有“主动检测”ComputeNode的能力，需要用户（或系统管理员）在VortexOSAI的命令行中通过下面命令手工添加

```
/node add llama Llama-2-13b-chat http://localhost:8000
```

上面添加的是运行在本地的13b模型，如果你使用的是其它模型，或则跑在了不同的机器上。请修改上述命令中的模型名和端口号。

### 配置Agent使用LLaMa

VortexOSAI的Agent可以选择最适合其职责的LLM-Model，我们内置了一个Agent叫Lachlan的私人西班牙语老师Agent，已经被配置成了使用LLaMa-2-13b-chat模型。你可以通过下面命令与其聊天：

```
/open Lachlan
```


因此添加了一个新的LLM后，需要手工修改Agent的配置，才能让其使用新的LLM。比如我们的私人英文老师Tracy，其配置文件是`/opt/aios/agents/Tracy/Agent.toml`，修改配置如下：
```
llm_model_name="Llama-2-13b-chat"
max_token_size = 4000
```
然后重新启动VortexOSAI,你就可以让Tracy使用LLaMa了(你也可以通过该方法查看其它内置的Agent使用了哪些LLM模型)


## Hello, Jarvis!

配置完成后，你会进入一个AIOS Shell,这和linux bash 和相似，这个界面的含义是：
当前用户 "username" 正在 和 名“为Jarvis的Agent/Workflow” 进行交流，当前话题是default。
和你的私人AI管家Jarvis Say Hello吧！

***如果一切正常，你将会在一小会后得到Jarvis的回复。此时VortexOSAI系统已经正常运行了***

## 给Jarvis注册Telegram账号
你已经完成了VortexOSAI的安装和配置，并已经验证了其可以正常工作。下面让我们尽快回到熟悉的图形界面，回到移动互联网吧！
我们将给Jarvis注册一个Telegram账号，通过Telegram，我们可以使用熟悉的方式和Jarvis进行交流了~
在VortexOSAI的aios_shell输入

```
/connect Jarvis
```

按照提示输入Telegram Bot Token就完成了Jarvis的账号注册. 你可以通过阅读下面文章来了解如何获取Telegram Bot Token
https://core.telegram.org/bots#how-do-i-create-a-bot，

我们还支持给Agent注册email账号，用下面命令行

```
/connect Jarvis email
```

然后根据提示就可以给Jarvis绑定电子邮件账号了。但由于目前系统并未对email内容定制前置过滤，所以可能会带来潜在的大量LLM访问费用，因此Email的支持是实验性的。我们推荐给Agent创建全新的电子邮件账号。

## 以服务方式运行VortexOSAI

上述的运行方式是以交互方式运行VortexOSAI，这种方式适合在开发和调试的时候使用。在实际使用的时候，我们推荐以服务方式运行VortexOSAI，这样可以让VortexOSAI在后台默默的运行，不会影响你的正常使用。
先输入

```
/exit
```

关闭并退出VortexOSAI,随后我们再用服务的方式启动VortexOSAI：

```
docker start aios
```

Jarvis是运行在VortexOSAI上的Agent,当VortexOSAI退出后，其活动也会被终止。因此如果想随时随地通过Telegram和Jarvis交流，请记住保持VortexOSAI的运行（不要关闭你的电脑，并保持其网络连接）。

实际上,VortexOSAI是一个典型的Personal OS，运行在Personal Server之上。关于Personal Servier的详细定义可以参考[CYFS Owner Online Device(OOD) ](https://github.com/buckyos/CYFS)。因此运行在PC或笔记本上并不是一个正式选择，但谁要我们正在Internal Test呢？

我们正在进行的很多研发工作，其中有很大一部分的目标，就是能让你轻松的拥有一个搭载AIOS的Personal Server.相对PC，我们将把这个新设备叫PI(Personal Intelligence)，VortexOSAI是面向PI的首个OS。

## 你的私人管家 Jarvis 前来报道！

现在你已经可以随时随地通过Telegram和Jarvis交流了，但只是把他看成更易于访问的ChatGPT,未免有点小瞧他了。让我们来看一下运行在VortexOSAI里的Jarvis有什么新本事吧！

## 让Jarvis给你安排日程

相信不少朋友有长期使用Outlook等传统Calender软件来管理自己日程的习惯。像我自己通常每周会花至少2个小时来是使用这类软件，当发生一些计划外的情况时，对计划进行手工调整是一个枯燥的工作。作为你的私人管家，Jarvis必须能够帮用自然语言的方式帮你管理日程！
试试和Jarvis说：

```
我周六和Alic上午去爬山，下午去看电影！
```

如果一切正常，你会看到Jarvis的回复，并且已经记住了你的日程安排。

你可以通过自然语言的方式和Jarvis查询
```
我这周末有哪些安排？
```

你会看到Jarvis的回复，其中包含了你的日程安排。
由于Jarvis使用LLM作为思考内核，他能以非常自然的方式和你进行交流，并在合适的时候管理你的日程。比如你可以说

```
我周六有朋友从LA过来，很久没见了，所有周六的约会都移动到周日吧！
```

你会看到Jarvis会自动的帮你吧周六的日程移动到周日。
实际上在整个交流的过程中，你不需要有明确的“使用日程管理语言的意识”，Jarvis作为你的管家，在理解你的个人数据的基础上，会在合适的时机和你进行交流，帮你管理日程。
这是一个非常简单而又常用的例子，通过这个例子，我们可以看到未来人们不再需要学习一些今天非常重要的基础软件了。

欢迎来到新时代！

Agent安排的日程数据都保存在 ~/myai/calender.db 文件中，格式是sqlite DB. 我们后续计划授权让Jarvis可以操作你生产环境中的Calender(比如常用的Google Calender)。但我们还是希望未来，人们可以把重要的个人数据都保存在自己物理上拥有的Personal Server中。

## 介绍Jarvis给你的朋友

把Jarvis的telegram账号分享给你的朋友，可以做一些有趣的事情。比如你的朋友可以在联系不到你的时候，通过Jarvis，你的高级私人助理来处理一些事务性的工作，比如了解你最近的日程安排或计划。
尝试后你会发现，Jarvis并不会按预期工作。是因为站在数据隐私的角度，Jarvis默认只会和“可信的人”进行交流。要实现上面目标，你需要让Jarvis能了解你的人际关系。

### 让Jarvis管理你的联系人

VortexOSAI在 myai/contacts.toml 文件中保存了系统已知的所有人的信息。现在非常简单的分成了两组
1. Family Member,现在该文件里保存里你自己的信息（在系统首次初始化时登陆的）添加
2. Contact，通常是你的好友

任何不存在上述列表中的联系人，都会被系统划分到`Guest`。Jarvis默认不允许和`Guest`进行交流。因此如果你想要让Jarvis和你的朋友进行交流，你需要把他添加到`Contact`中。
你可以手工修改 myai/contacts.toml 文件，也可以通过Jarvis来添加联系人。试试和Jarvis说

```
Jarvis,请添加我的朋友Alic到我的联系人中，他的telegram username是xxxx,email是xxxx
```

Jarvis能够理解你的意图，并完成添加联系人的工作。
添加联系人后，你的朋友就可以和你的私人管家Jarvis进行交流了。

## 更新VortexOSAI的镜像

现在VortexOSAI还处在早期阶段，因此我们会定期发布VortexOSAI的镜像来修正一些BUG。因此你可能需要定期更新你的VortexOSAI镜像。更新VortexOSAI的镜像非常简单，只需要执行下面的命令就可以了
```
docker stop aios
docker rm aios
docker pull paios/aios:latest
docker run -v /your/local/myai/:/root/myai --name aios -it paios/aios:latest 
```


## 让Agent进一步访问你的信息 

你已经知道Jarvis可以帮你管理一些重要的信息。但这些信息都是“新增信息”。在上世纪80年代PC发明以后，我们的一切都在高速的数字化。每个人都已有了海量的数字信息，包括你通过智能手机拍摄的照片，视频，你工作中产生的邮件文档等等。过去我们通过文件系统来管理这些信息，在AI时代，我们将通过Knowledge Base来管理这些信息，保存在Knowledge Base中的信息能更好的被AI访问，让你的Agent更理解你，更好的为你服务。

Knowledge Base是VortexOSAI里非常重要的一个基础概念，也是我们为什么需要Personal AIOS的一个关键原因。Knowledge Base相关的技术目前正在快速发展，因此VortexOSAI的Knowledge Base的实现也在快速的进化。目前我们的实现更多的是让大家能体验Knowledge Base与Agent结合带来的新能力，其效果还远远未达我们的预期。站在系统设计的角度，我们尽快开放这个组件的另一个目的，是希望找到在产品上对用户更友好，更平滑的方法来把已经存在的个人信息导入进Knowledge Base。

Knowledge Base功能已经默认开启了，将自己的数据放入Knowledge Base有两种方法

1. 把要放入KnowledgeBase的数据复制到 `~myai/data`` 文件夹中。
2. 通过输入`/Knowledge add dir` ，系统会要求你输入一个将要导入到Knowledge Base的本地目录。注意VortexOSAI默认运行在容器中，因此$dir是相对于容器的路径，如果你想要加入本地磁盘的数据，需要先把本地数据挂载到容器中。

VortexOSAI会在后台不断分析已加入Knowledge Base文件夹中的文件，分析结果保存在 ~/myai/knowledge 目录中。将该目录删除后，系统会重新分析已加入Knowledge Base的文件。由于目前VortexOSAI的Knowledge Base还处在早期阶段，因此目前只支持分析识别文本文件，图片，短视频等。未来VortexOSAI将会支持所有的主流文件格式，尽可能把所有的已有信息都能导入到Knowledge。可以aios_shel中通过下面命令来查询Knowledge Base 分析任务的运行状态。

```
/Knowledge journal
```

### Mia：个人信息助手

然后我们可以通过 Agent "Mia"来访问Knwolege Base,

```
/open Mia
```

试着与Mia交流一下吧！我想这会带来完全不同的体验！
Mia找到的信息会用下面方式展示：

```
{"id": "7otCtsrzbAH3Nq8KQGtWivMXV5p54qrv15xFZPtXWmxh", "type": "image"}
```

可以用`/knowledge query 7otCtsrzbAH3Nq8KQGtWivMXV5p54qrv15xFZPtXWmxh` 命令来调用本地的文件查看器来查看结果。

我们更推荐把Mia接入到Telegram中,这样Mia会把查询结果直接用图片的方式展现，用起来更加方便~

### Embeding Pipeline

Knowledge Base读取并分析文件，产生Agent可以访问的信息的过程被称作Embeding.这个过程需要一定的计算资源。经过我们的测试，目前VortexOSAI基于“Sentence Transformers”构建的Embeding Pipeline是可以在绝大多数类型的机器上运行起来的。不同能力的机器的区别主要在于Embeding的速度和质量。了解VortexOSAI进度的朋友可能知道，我们在实现的过程中也曾支持过云端Embeding,用来彻底的减少VortexOSAI的最小系统性能要求。不过考虑到Embeding过程中涉及到的大量的个人隐私数据，我们还是决定关闭云端Embeding这个特性。有需要的同学可以通过修改源代码来打开云端Embeding,让VortexOSAI可以在非常低性能的设备上工作起来。

遗憾的是，现在并没有统一的Embeding标准，因此不同的Embeding Pipeline产生的结果不能互相兼容。这意味着一旦切换了Embeding Pipline,知识库的所有信息都要重新扫描。

## bash@aios

如果你有一定的工程背景，通过让Agent 执行bash命令，也可以非常简单快速的让VortexOSAI具有你的私有数据的访问能力。
使用命令

```
/open ai_bash
```

打开ai_bash,然后你就可以在aios_shell的命令行中执行传统的bash命令了。同时你还拥有了智能命令的能力，比如查找文件，你可以用

```
帮我查找 ~/Documents 目录下所有包含VortexOSAI的文件
```

来代替输入find命令~ 非常酷吧！

VortexOSAI目前默认运行在容器中，因此ai_bash也只能访问docker容器中的文件。这相对安全，但我们还是提醒你不要轻易的把ai_bash这个agent暴露出去，可能会带来潜在的安全风险。

## 我们为什么需要Personal AIOS?

很多人会第一个想到隐私，这是一个重要的原因，但我们不认为这是人们真正离开ChatGPT,选择Personal AIOS的真正原因。毕竟今天很多人并不对隐私敏感。而且今天的平台厂商一般都是默默的使用你的隐私赚钱，而很少会真正泄露你的隐私。

我们认为Personal AIOS的真正价值在于：

1. 成本是一个重要的决定因素。LLM是非常强大的，边界非常清楚的核心组件,是新时代的CPU。从产品和商业的角度，ChatGPT类产品只允许用有限的方法来使用它。让我想起了小型机刚刚出现时大家分时使用系统的时代：有用，但有限。要真正发挥LLM的价值，我们需要让每个人都能拥有自己的LLM，并能自由的使用LLM作为任何应用的底层组件，这就必须要有一个新的，以LLM为核心构建的操作系统来重新抽象应用（Agent/Workflow）和应用所使用的资源（算力，数据，环境）

2. 当拥有LLM后，当能把LLM放到每一个计算前面时，你会看到真正的宝藏！现在的ChatGPT通过Plugin对LLM能力的扩展，其能力和边界都是非常有限的，这里既有商业成本的原因，也有传统云服务的法律边界问题：平台要承担的责任太多了。而通过在Personal AIOS中使用LLM，你可以自由的把自然语言，LLM，已有服务，私人数据，智能设备连接在一起，并不用担心隐私泄露和责任问题（你自己承担了授权给LLM后产生后果的责任）！

VortexOSAI is an open-source project, let's define the future of Humans and AI together!