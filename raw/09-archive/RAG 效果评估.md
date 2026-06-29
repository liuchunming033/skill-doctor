在 RAG 系统的开发、优化与应用过程中，RAG 效果评估是其中不可或缺的一环。通过建立统一的评估标准，能够公平、客观地比较不同 RAG 系统及其优化方法，从而识别出最佳实践。这套评估体系不仅帮助开发者发现系统的优劣，亦为后续的改进提供了有力的参考依据。

下面我介绍一种在真实应用场景中采用的 RAG 效果评估标准与方法。

1. ### 评估方式
    

- 人工打分：由人类评审员对 RAG 的输出进行逐一打分。人工评估方式可以提供更为精确、细致的反馈，特别是在检测生成答案中的细微错误和幻觉时，但其耗时较长，成本较高。
    
- 大模型打分：通过使用大语言模型对 RAG 的输出进行自动评分。这类评估方式效率高，能够快速处理大规模的评估任务，但在准确性上可能受到模型本身偏差的影响。
    
- 综合方式：结合人工打分和大模型打分，充分利用他们各自的优点。最终给出RAG效果的结论。通常将所有评测样本进行大模型打分，然后再对其中部分评测样本进行人工打分。
    

2. ### 评估流程
    

具体到评测阶段，评测流程包括：评测需求分析、评测数据集构建、执行评测、分析评测数据、出具评测报告几个阶段。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=N2U0MGFkNzY5ZTIyOGEyZDljYWE3OTcwMTY1MjVjY2JfVUIwaFRiSVdmWlBmV2trTmlSOU1xclg4cGZpSDNydXpfVG9rZW46WXM1dGI3U0hwb0VvSlN4WmxZWmNOTWNpbkY5XzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

3. ### 评估指标
    

按照RAG的阶段划分，RAG的评估指标可以分为与检索器相关的指标和与生成器相关的指标。

以Ragas框架为例，说明一下RAG的主要评估指标。Ragas是一个评估检索增强生成（RAG）系统的性能的框架。它提供了一组评估指标（metrics），用于衡量RAG应用的性能。

- Context Precision 上下文精度
    
- Context Recall 上下文召回率
    
- Context Entities Recall 上下文实体召回率
    
- Noise Sensitivity 噪声敏感
    
- Response Relevancy 响应的相关性
    
- Faithfulness 忠实度
    
- Factual Correctness 事实正确性
    
- Answer Semantic Similarity 答案的语义相似度
    

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=MzZkY2NmYzE4ZjE2OWZkNDVkNWI5MjZlODUzNjBhMjJfT3RxM0w0b2h0R3JqZXFGaHIyS2tOZzdwNFdjN3dBREFfVG9rZW46R2lxSmJSTGM4b0JHYXh4bWZ1dWNYVjEzbnhiXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

检索器相关指标用于衡量检索系统性能，包括：

- Context Precision 上下文精度，衡量检索到的上下文（context）与用户问题（query）的相关程度，理想情况下相关度高的排在前面。
    
- Context Recall 上下文召回率，衡量检索器检索所有必要信息（context）以回答用户问题（query）的能力。
    
- Context Entities Recall 上下文实体召回率，衡量检索到的上下文中实体的召回率。
    

生成器相关指标用于衡量生成器的性能，包括:

- Faithfulness 忠实度，衡量答案answer与基于问题相关上下文（context）的事实一致性。
    
- Noise Sensitivity 噪声敏感度，衡量系统在利用相关或不相关的检索文档时提供错误响应的频率。
    
- Response Relevancy 响应的相关性，衡量答案与问题之间的相关程度。
    
- Factual Correctness 事实正确性，用于比较和评估生成的回应与参考信息的事实准确性，有F1（F1分数），精确度（precision）或召回率（recall）三种评估指标。
    
- Answer Semantic Similarity 答案的语义相似度，这是一种评估生成答案与真实答案（ground truth）之间语义相似度。
    

Ragas评测示例：

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=OGRlOTU4ZTRiNTMwYzJhNjg1ZWZmMzFhNTZiMGFmZTdfa2VJV2M5YUNsZ2JXejJmQzZGWkpQQllDbU9wUHd6RU5fVG9rZW46WEd6bmJGdGNYb2J5dFR4SjFHWmNKY25abktiXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

1. **Faithfulness 忠实度**
    

忠实度faithfulness指标用于评估生成答案的准确性，即检查答案中所述内容是否由提供的上下文所支持。通过分析生成答案中每个陈述的有效性（相对于上下文）来计算该指标。“忠实度”值在0到1的范围内，值越大表示“忠实度”越好。

如果生成的答案中所有陈述都可以从给定的上下文中推断出来，生成的答案被认为是准确的。要确定这一点，首先将生成的答案拆解成一组陈述语句。然后，将这些陈述语句与给定的上下文一一核对，以查看它们是否可以从上下文中推断出来。

忠实度faithfulness得分计算方式为：

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=MmVmOTEyMzRjNmRkZjc2MjE5NzY2MTYyYzJkYTU5ZDFfZE9RSkdNd2RnSkVXQ1ZNc2pZMFB6anFpNnMxRlg5V0ZfVG9rZW46T0Z0MWJsNHo3b2pjbmh4NnB5b2M0Vm1GblJoXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

举个例子说明忠实度faithfulness的计算方法：

> Question：爱因斯坦出生在哪里，何时？
> 
> Context: 阿尔伯特·爱因斯坦（生于1879年3月14日）是一位德国出生的理论物理学家，被普遍认为是有史以来最伟大、最有影响力的科学家之一。
> 
> 高 faithfulness 答案: 爱因斯坦于1879年3月14日出生在德国。
> 
> 低 faithfulness 答案: 爱因斯坦于1879年3月20日出生在德国。
> 
> 让我们来看看如何对于“低忠诚度”答案，他的忠诚度怎么计算：
> 
> 第1步：将生成的答案分解为独立的陈述语句：
> 
> 陈述语句1：“爱因斯坦出生在德国。”
> 
> 陈述语句2：“爱因斯坦于1879年3月20日出生。”
> 
> 第2步：对于生成的每个陈述语句，检查它是否能从给定的上下文中推断得出。显然，
> 
> 陈述语句1：能
> 
> 陈述语句2：不能
> 
> 第3步：使用上图所示的公式计算忠诚度。例如计算低faithfulness的答案的忠实度为：faithfulness=1/2=0.5

使用Ragas计算faithfulness：

```Python
from ragas.database_schema import SingleTurnSample 
from ragas.metrics import Faithfulness
sample = SingleTurnSample(
        user_input="When was the first super bowl?",
        response="The first superbowl was held on Jan 15, 1967",
        retrieved_contexts=[
"The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."
        ]
    )
scorer = Faithfulness()
await scorer.single_turn_ascore(sample)
```

2. **Response Relevancy 响应的相关性**
    

答案相关性response_relevancy用于评估生成的响应与对应问题的相关程度。包含不完整信息或冗余信息的答案得分较低，而得分越高表示相关性越好。

答案相关性是指原始问题与基于答案生成（反向工程）的一系列人工问题之间的平均余弦相似度。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=YTk3ZjI5YjA2ZTVlZjBlMzY4ZDVjNWM0OWI4Y2NlMzhfcjdROUxpTjlzZkE1cW9tUEJEVnRSRDhUbFBwZldSbUpfVG9rZW46T1k2Z2JjRnpEb2JWY2N4MXBEd2NxdTgwbm1kXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

其中，_E(gi)_表示第 i个生成问题的嵌入向量，而 _E(o)_ 表示实际问题的嵌入向量。 cos⁡(_E(gi) , E(o)_)用于衡量两个向量之间的余弦相似度。

举个例子说明响应相关性response_relevancy的计算方法：

> 问题：法国在哪里？它的首都是哪里？
> 
> response_relevancy较低的答案：法国位于西欧。
> 
> response_relevancy较高的回答：法国位于西欧，巴黎是其首都。
> 
> 为了计算答案与给定问题的相关性，我们遵循以下两个步骤：
> 
> 第一步：利用大型语言模型（LLM）从生成的响应中逆向推导出“n”种问题变体。例如，对于第一个答案，LLM可能会生成以下可能的问题：
> 
> 问题1：“法国位于欧洲的哪个部分？”
> 
> 问题2：“法国在欧洲的地理位置在哪里？”
> 
> 问题3：“你能指出法国位于欧洲的哪个地区吗？”
> 
> 第二步：计算生成的问题与实际问题的平均余弦相似度。

使用Ragas计算response_relevancy：

```Python
from ragas import SingleTurnSample 
from ragas.metrics import ResponseRelevancy
sample = SingleTurnSample(
        user_input="When was the first super bowl?",
        response="The first superbowl was held on Jan 15, 1967",
        retrieved_contexts=[
"The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."
        ]
    )
scorer = ResponseRelevancy()
await scorer.single_turn_ascore(sample)
```

3. **Noise Sensitivity 噪声敏感度**
    

NoiseSensitivity衡量RAG系统在使用相关或不相关的检索文档（retrieved_contexts）时得出不正确响应（response）的频率。该分数的范围为0到1，分数越低表示性能越好。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=OTIwYzAyMTlmZDVkNjAyMDQ4YWQ5YmJhOTE0MzllMDdfVklrc1hyb3hZMTFFWGM1anA3aGN5Nm1LTTVQRDhrZHRfVG9rZW46TVI4bmJYMVVkb2JNdjR4U0dIZWN2cVVwbjlnXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

为了估算噪声敏感度，需要对生成的响应（response）中的每个陈述（claim）进行检查，以确定其是否基于事实（Ground truth），以及它是否与检索到的上下文（retrieved_contexts）相关。理想情况下，响应中的所有断言（claim）都应由相关的检索到的上下文（retrieved_contexts）支持。

举个例子，说明噪声敏感度NoiseSensitivity是如何计算的：

> 问题user_input：印度人寿保险公司（LIC）以什么著称？
> 
> 事实reference：印度人寿保险公司(LIC)是印度最大的保险公司，成立于1956年，当时政府将保险业国有化。该公司以管理庞大的投资组合而闻名。
> 
> 响应response：印度人寿保险公司（LIC）是印度最大的保险公司，以其庞大的投资组合而闻名。LIC为国家的金融稳定做出了贡献。
> 
> 找回的上下文retrieved_contexts，其中：
> 
> - 相关检索：
>     
> 
> context 1. 印度人寿保险有限公司（LIC）成立于1956年，当时印度的保险业实现了国有化。
> 
> context 2. LIC是印度最大的保险公司，拥有庞大的保单持有人网络，在金融领域发挥着重要作用。
> 
> context 3. 作为印度最大的机构投资者，LIC管理着一笔庞大的寿险基金，为国家的金融稳定做出了贡献。
> 
> - 不相关的检索：
>     
> 
> context4：印度经济是全球增长最快的主要经济体之一，得益于金融、技术、制造业等行业。
> 
> 计算步骤：
> 
> 第1步：从事实（reference）中，识别出相关的上下文：context 1、context 2和context 3
> 
> 第2步：确认生成响应（response）中提出的主张是否能从上面的上下文中推断得出：context 1（能）、context 2（能）和context 3（能）。
> 
> 第3步：识别答案（response）中的任何错误陈述（即没有得到事实（reference）支持的陈述）：事实真相中并未提及LIC对国家金融稳定作出贡献。因此，答案中的这个陈述是不正确的。
> 
> 因此，错误陈述1：全部陈述：3。根据公式计算答案NoiseSensitivity=1/3=0.3333

使用Ragas计算NoiseSensitivity：

```Python
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import NoiseSensitivity
sample = SingleTurnSample(
    user_input="What is the Life Insurance Corporation of India (LIC) known for?",
    response="The Life Insurance Corporation of India (LIC) is the largest insurance company in India, known for its vast portfolio of investments. LIC contributes to the financial stability of the country.",
    reference="The Life Insurance Corporation of India (LIC) is the largest insurance company in India, established in 1956 through the nationalization of the insurance industry. It is known for managing a large portfolio of investments.",
    retrieved_contexts=[
        "The Life Insurance Corporation of India (LIC) was established in 1956 following the nationalization of the insurance industry in India.",
        "LIC is the largest insurance company in India, with a vast network of policyholders and huge investments.",
        "As the largest institutional investor in India, LIC manages substantial funds, contributing to the financial stability of the country.",
        "The Indian economy is one of the fastest-growing major economies in the world, thanks to sectors like finance, technology, manufacturing etc."
    ]
)
scorer = NoiseSensitivity()
await scorer.single_turn_ascore(sample)
```

4. **Factual Correctness 事实正确性**
    

这个指标用来确定生成的响应（Response）和参考信息（reference）的一致程度。事实正确性得分的范围是0到1，值越高表示性能越好。

具体计算过程：

1. 使用大型语言模型（LLM）将响应（Response）和参考信息（reference）分解成单独的陈述或“主张”（claims）。
    
2. 然后使用自然语言推理（natural language inference）来确定响应（Response）和参考信息（reference）之间的事实重叠部分。
    
3. 使用精确度（precision）、召回率（recall）和F1分数（F1 score）来量化这种事实重叠。
    

精确度、召回率和F1分数的计算公式如下：

- 真正例（True Positive, TP）：响应（Response）中存在且参考中也有的主张数量。
    
- 假正例（False Positive, FP）：响应（Response）中存在但参考中没有的主张数量。
    
- 假负例（False Negative, FN）：参考中存在但响应（Response）中没有的主张数量。
    
- 精确度（Precision）= TP / (TP + FP)
    
- 召回率（Recall）= TP / (TP + FN)
    
- F1分数（F1 Score）= 2 × 精确度 × 召回率 / (精确度 + 召回率)
    

示例代码：

```Python
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics._factual_correctness import FactualCorrectness
sample = SingleTurnSample(
    response="The Eiffel Tower is located in Paris.",
    reference="The Eiffel Tower is located in Paris. I has a height of 1000ft."
)
scorer = FactualCorrectness(mode="F1", atomicity="low", coverage="low")
scorer.llm = openai_model
await scorer.single_turn_ascore(sample)
```

（LLM）将响应（Response）和参考信息（reference）分解成单独的陈述或“主张”（claims）的数量可以通过“原子性（Atomicity）”和“覆盖度（Coverage）”两个参数来控制。

1. **原子性Atomicity**指的是句子被分解成最小、有意义的组成部分的程度。
    
    1. 高原子性：句子被分解成基本的、不可分割的断言，结果是多个较小的“主张”（claims），每个代表一个独特的信息片段。
        
    2. 低原子性：句子保持更完整，结果产生较少的“主张”（claims），可能包含多个信息片段。
        
2. **覆盖度**Coverage指的是“主张”（claims）在多大程度上全面代表了原始句子中的信息。
    
    1. 高覆盖度：分解的“主张”（claims）捕捉了原始句子中的所有信息，保留每个细节。
        
    2. 低覆盖度：分解的“主张”（claims）只覆盖主要点，省略了一些细节，以提供更一般化的观点。
        

通过调整原子性和覆盖度，可以定制细节和完整性的水平，以满足特定用例的需求。

- 高原子性 & 高覆盖度：产生高度详细和全面的“主张”（claims），涵盖原始句子的所有方面。
    
- 低原子性 & 低覆盖度：产生较少的“主张”（claims），细节较少，总结主要观点而不涉及具体细节。
    

当你需要详细和全面的分解以进行深入分析或信息提取时，使用高原子性和高覆盖度。当只需要关键信息时，例如在总结时，使用低原子性和低覆盖度。

5. **Answer Semantic Similarity 答案的语义相似度**
    

Answer Semantic Similarity是一种评估生成答案与真实答案之间语义相似度的方法。该评估基于真实答案和生成答案，使用交叉编码模型计算语义相似度得分，得分范围为0到1，分数越高表示生成答案与真实答案的对齐度越好。

计算过程是，先将真实答案和生成响应向量化，然后计算两个向量之间的余弦相似度来得出答案相似度。

示例代码：

```Python
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import SemanticSimilarity
sample = SingleTurnSample(
    response="The Eiffel Tower is located in Paris.",
    reference="The Eiffel Tower is located in Paris. I has a height of 1000ft."
)
scorer = SemanticSimilarity()
scorer.embeddings = embedding_model
await scorer.single_turn_ascore(sample)
```

embedding_model是一个Embedding模型实例。默认是用的open-ai-embeddings模型，也可以从[https://huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard)榜单上找一个合适的模型。

6. **Context Recall 上下文召回率**
    

召回率context_recall衡量的是成功检索到的与答案相关的文档数量。context_recall值介于 0 和 1 之间，值越大表示性能越好。

计算公式：

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=NjQxN2ZiNmJkNjk1ZDUxZjZmNTk5ZmViZDI5ZGFhMmNfOVhFd2VOSnhvMDlrazBGQmZyaGhMWUJyZmY2czBIWE5fVG9rZW46Sk5ENGJCZ2E2b3FaUVN4VXphdmN2cnR4bnNjXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

其中，

- `Number of claims in GT that can be attributed to context`表示能够追溯到检索到的上下文（retrieved_contexts）的主张数量
    
- Number of claims in GT表示参考答案中的主张（claims）数据量。
    

评估过程中，参考答案（ground_truth_answer）被分解成一系列的主张（claims），然后对参考答案（ground_truth_answer）中的每个主张进行分析，以确定它是否可以归因于检索到的上下文（retrieved_contexts）。换句话说，就是检查参考答案中的每个信息点是否都能在检索到的上下文（retrieved_contexts）中找到依据。

在理想的情况下，参考答案（ground_truth_answer）中的所有主张都应该能够追溯到检索到的上下文（retrieved_contexts）中，这样的结果表明检索系统能够准确地找到与用户查询相关的信息。

使用Ragas计算context_recall：

```Python

from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import LLMContextRecall
sample = SingleTurnSample(
    user_input="Where is the Eiffel Tower located?",
    response="The Eiffel Tower is located in Paris.",
    reference="The Eiffel Tower is located in Paris.", # ground truth answer
    retrieved_contexts=["Paris is the capital of France."], 
)
context_recall = LLMContextRecall()
await context_recall.single_turn_ascore(sample)
```

上面计算上下文召回（Context Recall）的计算方法是基于大型语言模型（LLM）的，另外一种计算方法是非基于LLM的上下文召回（NonLLMContextRecall）。

NonLLMContextRecall 使用检索到的上下文（retrieved_contexts）和参考上下文（reference_contexts）来计算上下文召回率。这个指标的值范围在0到1之间，值越高表示性能越好。这个方法使用非LLM的字符串比较指标来确定检索到的上下文是否相关。你可以使用任何非LLM的指标作为距离度量来识别检索到的上下文是否相关。

计算上下文召回的公式如下：

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=MjRkY2Q5NmVhNWY3ZDg0Y2VjYTUwNDRjODE4OWY3OTRfaE5BOHVaTmFiWDVwMTYwZDVHVWh6S3FZc1lJU3JocWlfVG9rZW46WEhmUmJOVkdqb2tPRHh4VzhpRmM1YUQwbmdlXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

其中，

- `Number of relevant contexts retrieved`指的是检索到的相关上下文的数量，
    
- `Total number of reference contexts`指的是参考上下文的总数。
    

下面是一个例子：

```Python
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import NonLLMContextRecall
sample = SingleTurnSample(
    retrieved_contexts=["Paris is the capital of France."],
    reference_contexts=["Paris is the capital of France.", "The Eiffel Tower is one of the most famous landmarks in Paris."]
)
context_recall = NonLLMContextRecall()
await context_recall.single_turn_ascore(sample)
```

在这个例子中，`retrieved_contexts` 包含了一个检索到的上下文，即“Paris is the capital of France.”，而 `reference_contexts` 包含了两个参考上下文。如果检索到的上下文与参考上下文之一相匹配，那么上下文召回率就是1（因为检索到的相关上下文数量是1，而参考上下文的总数也是1）。如果检索到的上下文与任何参考上下文都不匹配，那么上下文召回率就是0。

7. **Context Entities Recall 上下文实体召回率**
    

ContextEntityRecall这个度量指标指的是retrieved_contexts中存在的实体数量与reference中存在的实体数量之间的相对比例。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=NTI0ZGZjOGM3ZjBlNTMxYTE4YmYwYmZjOWY1ZTVhYzBfZk9xbzdTU1JBTE1Fd01DNklSOUVLZzBLNGFBUGtSUFlfVG9rZW46TVFsNmJCbm55b2lad2J4MzQzUmNtUzZRbmNoXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

其中，GE表示Ground Entity，即参考文本中的实体集合，CE表示Context Entity，即检索到的上下文中的实体集合。

该公式表示，先计算这两个集合的交集，即同时出现在GE和CE中的实体。再统计出交集中的元素数量。最后将交集中的元素数量除以GE集合中的元素数量。

举一个例子说明ContextEntityRecall的计算逻辑：

> 参考（reference）：泰姬陵是一座位于印度阿格拉市亚穆纳河右岸的象牙白色大理石陵墓。它是莫卧儿皇帝沙贾汗于1631年下令建造的，用来安葬他最喜爱的妻子穆塔兹·马哈尔。
> 
> 高实体召回上下文（High entity recall context）：泰姬陵是位于印度阿格拉的一座爱情和建筑奇迹的象征。它是莫卧儿皇帝沙贾汗为了纪念他心爱的妻子穆塔兹·马哈尔而建造的。这座建筑以其精致的大理石雕刻和环绕周围的美丽的花园而闻名。
> 
> 低实体召回上下文（Low entity recall context）：泰姬陵是印度的一个标志性建筑。它是联合国教科文组织世界遗产地，每年吸引数百万游客。其精致的雕刻和惊人的建筑使其成为必游之地。
> 
> 第一步，找出ground truths即reference中存在的实体集合 - ['泰姬陵'， '亚穆纳河'， '阿格拉'， '1631'， '沙贾汗'， '穆塔兹·马哈尔']
> 
> 第二步：找出上下文中存在的实体。高实体召回上下文中实体集合是： ['泰姬陵'， '阿格拉'， '沙贾汗'， '穆塔兹·马哈尔'， '印度']，低实体召回上下文中实体集合是： ['泰姬陵'， '联合国教科文组织'， '印度']
> 
> 第三步：使用上述公式计算实体召回率。
> 
> 我们可以看到，第一个上下文的实体召回率很高，因为它在真实情况下具有更好的实体覆盖率。如果这两个上下文是由同一组文档的两个检索机制提取的，那么可以说，在实体很重要的情况下，第一个机制比另一个更好。

使用Ragas计算ContextEntityRecall：

```Python
from ragas import SingleTurnSample
from ragas.metrics import ContextEntityRecall
sample = SingleTurnSample(
    reference="The Eiffel Tower is located in Paris.",
    retrieved_contexts=["The Eiffel Tower is located in Paris."], 
)
scorer = ContextEntityRecall()
await scorer.single_turn_ascore(sample)
```

8. **Context Precision 上下文精度**
    

上下文精度（Context Precision）用来衡量检索到的上下文中与问题相关的片段的比例。为了估计检索到的上下文是否与用户输入相关，计算context precision时使用大型语言模型（LLM）来判断检索上下文（retrieved_contexts）中的每一个上下文与用户输入（user_input）是否有关。

上下文精度（Context Precision）的计算方法是对上下文中每个片段的`precision@k`取平均值。`precision@k`是指在排名k中相关片段的数量与排名k中所有片段总数之比。

计算公式：

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=NjNiYThmYjQ0MGY5NmM0OGZkYzk4OTAzMDgwMzQ4ZDNfcjhNR0FyY0VCVUtwMnpJZ3pnOTVYZjRmWm42Sktnb0dfVG9rZW46TENycWJqT3dsbzdaRkV4QzBtUWN0YnpIbmtjXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

这里的K代表检索到的上下文（retrieved_contexts）中的总片段数，而V(k)是一个二元变量，表示在排名k位置上的片段的相关性指示器，其值可以是0或1。如果一个片段在排名k时被认为是相关的，则V(k)为1；如果无关，则V(k)为0。

`precision@k`的定义为：

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=OWRhNzM5NDE0MmEyYTE0YjhlYTQ4N2I3MDc2NGNhN2Ffbm1MamR2a1Rvak9jN1puUzczZjFwMXhlT2ZlQmI2eVVfVG9rZW46VjQ4YmJYWDhhb0t6MDJ4WmhRaGNXOXlTbjVlXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

`Precision@k`的计算公式，即在前k个结果中真正例（true positives）的数量与真正例和假正例（false positives）之和的比例。这个比例可以用来衡量在给定的k个结果中，真正例的比例。

举个例子说明precision@k的计算过程：

> 假设你正在使用一个搜索引擎来搜索“最好的智能手机”，搜索引擎返回了以下结果列表：
> 
> 1. 智能手机评测文章
>     
> 2. 智能手机销售网站
>     
> 3. 智能手机用户论坛
>     
> 4. 智能手机游戏应用
>     
> 5. 智能手机比较工具
>     
> 
> 假设你只关注前3个结果（即k=3），并且你已经确定：
> 
> - 结果1（智能手机评测文章）是相关的。
>     
> - 结果2（智能手机销售网站）是相关的。
>     
> - 结果3（智能手机用户论坛）是不相关的。
>     
> 
> 那么，`precision@3` 的计算如下：
> 
> - 相关项的数量 = 2（结果1和结果2）
>     
> - 排名位置3的总项数 = 3（结果1、结果2和结果3）
>     
> 
> 即precision@3=2/3

有两种办法计算上下文精度（Context Precision），一种是基于大模型`LLM Based Context Precision`，另外一种不基于大模型`Non LLM Based Context Precision`。

`LLM Based Context Precision`是使用大型语言模型（如GPT等）来评估检索到的上下文（retrieved contexts）是否与用户输入（user_input）相关。基于LLM的上下文精确度评估方法有两种：

1. **无参考上下文的上下文精确度（Context Precision without reference）：**
    

这种方法使用`LLMContextPrecisionWithoutReference`指标，适用于没有与用户输入相关联的参考答案（reference）情况。

这种方法使用大型语言模型（LLM）将检索到的每个上下文（retrieved_contexts）或检索上下文中的每个片段（chunk）与用户输入的响应（response）进行比较。

示例代码：

```Python

from ragas import SingleTurnSample
from ragas.metrics import LLMContextPrecisionWithoutReference
context_precision = LLMContextPrecisionWithoutReference()
sample = SingleTurnSample(
    user_input="Where is the Eiffel Tower located?",
    response="The Eiffel Tower is located in Paris.",
    retrieved_contexts=["The Eiffel Tower is located in Paris."], 
)
await context_precision.single_turn_ascore(sample)
```

2. **有参考上下文的上下文精度（Context Precision with reference）**
    

这种方法适用于当你既有检索到的上下文（retrieved_contexts），也有与用户输入相关联的参考回答（reference）时。通过比较检索到的每个上下文或块与参考回答来估计检索到的上下文是否相关。如果检索到的上下文与参考回答相匹配或相关，那么这个检索到的上下文就被认为是相关的。

示例代码：

```Python
from ragas import SingleTurnSample
from ragas.metrics import LLMContextPrecisionWithReference
# 创建一个度量指标实例
context_precision = LLMContextPrecisionWithReference()
# 创建一个样本，包含用户输入、参考回答和检索到的上下文
sample = SingleTurnSample(
    user_input="Where is the Eiffel Tower located?",
    reference="The Eiffel Tower is located in Paris.",
    retrieved_contexts=["The Eiffel Tower is located in Paris."], 
)
# 计算并等待返回单轮对话的分数
await context_precision.single_turn_ascore(sample)
```

`Non LLM Based Context Precision`是指不依赖于大型语言模型来确定检索到的上下文是否与用户响应或者参考上下文相关的方法。相反，它使用传统的度量方法来评估检索到的上下文的相关性。

具体来说，当既有检索到的上下文（retrieved contexts）也有与用户输入（user_input）相关的参考上下文（reference contexts）时，可以使用`NonLLMContextPrecisionWithReference`这个指标。这个方法通过比较检索到的上下文中的每个部分（或称为chunk）与参考上下文中的每个部分来估计检索到的上下文是否相关。

示例代码：

```Python
from ragas import SingleTurnSample
from ragas.metrics import NonLLMContextPrecisionWithReference
context_precision = NonLLMContextPrecisionWithReference()
sample = SingleTurnSample(
    retrieved_contexts=["The Eiffel Tower is located in Paris."],
    reference_contexts=["Paris is the capital of France.", "The Eiffel Tower is one of the most famous landmarks in Paris."]
)
await context_precision.single_turn_ascore(sample)
```

4. ### 生成RAG评测集
    

评测集是用于评估模型性能的数据集，它不参与模型的训练过程，而是用于在模型训练完成后测试其准确性和泛化能力。

第一种方法是从 Hugging Face Datasets 库中加载数据集，并将其转换为 Ragas 库可以处理的格式。需要提前[安装datasets](https://huggingface.co/docs/datasets/installation)`pip install datasets`。

```Python
from datasets import load_dataset
dataset = load_dataset("explodinggradients/amnesty_qa","english_v3")

from ragas import EvaluationDataset

eval_dataset = EvaluationDataset.from_hf_dataset(dataset["eval"])
```

另外一种方法是使用多个单个对话样本（SingleTurnSample实例）来创建一个评估数据集，如果是手工制作评测集，可以采用这个方法。

```Python
# Sample 1
sample1 = SingleTurnSample(
    user_input="What is the capital of Germany?",
    retrieved_contexts=["Berlin is the capital and largest city of Germany."],
    response="The capital of Germany is Berlin.",
    reference="Berlin",
)

# Sample 2
sample2 = SingleTurnSample(
    user_input="Who wrote 'Pride and Prejudice'?",
    retrieved_contexts=["'Pride and Prejudice' is a novel by Jane Austen."],
    response="'Pride and Prejudice' was written by Jane Austen.",
    reference="Jane Austen",
)

# Sample 3
sample3 = SingleTurnSample(
    user_input="What's the chemical formula for water?",
    retrieved_contexts=["Water has the chemical formula H2O."],
    response="The chemical formula for water is H2O.",
    reference="H2O",
)

dataset = EvaluationDataset(samples=[sample1, sample2, sample3])
```

实践中，更多的是通过使用自己的文档生成测试集，可以确保测试集与RAG具体应用场景紧密相关，从而更准确地评估RAG系统的效果。Ragas提供了从加载文档、选择语言模型（LLM）、生成测试集到导出结果的全链路支持。

1. **安装依赖包**
    

文章首先指导用户如何安装必要的包，并提供了一个快速示例，展示如何为RAG流水线生成测试集。

```Shell
pip install langchain-openai
pip install ragas
```

2. **加载样本文档**
    

通过git克隆样本文档，并使用DirectoryLoader加载文档，用户可以替换为自己的文档。

```Shell
git clone https://huggingface.co/datasets/explodinggradients/Sample_Docs_Markdown
```

使用`langchain_community`的`DirectoryLoader`加载器从样本数据集中加载文档。

```Python
from langchain_community.document_loaders import DirectoryLoader
path = "Sample_Docs_Markdown/"
loader = DirectoryLoader(path, glob="**/*.md")
docs = loader.load()
```

你也可以使用`llama_index`中的任何加载器加载文档，例如使用`SimpleDirectoryReader：`

```Python
from llama_index.core import SimpleDirectoryReader
path = "Sample_Docs_Markdown/"
docs = SimpleDirectoryReader(path).load_data()
```

3. **选择用于合成数据的LLM**
    

Ragas需要利用大型语言模型（LLM）和嵌入模型来合成测试数据。可以选择OpenAI、Amazon Bedrock、Azure OpenAI等LLM供应商提供的模型。Ragas集成了Langchain和Llamaindex框架。可以通过他们更好的和模型交互。

如果使用OpenAI的模型，并且使用Langchain框架进行调用，则需要安装langchain-openai包，这是一个通过Langchain框架与OpenAI模型进行交互的包。

```Python
pip install langchain-openai
```

接着，配置OpenAI密钥。

```Python
import os
os.environ["OPENAI_API_KEY"] = "your-openai-key"
```

将大型语言模型（LLMs）封装在LangchainLLMWrapper这个包装器中，以便它们可以与ragas集成。

```Python
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
```

如果使用其他模型供应商的模型，将`ChatOpenAI(model="gpt-4o")`换成你的模型实例即可。例如使用通义千问大模型：

```Shell
import os
os.environ["DASHSCOPE_API_KEY"] = "sk-28c6d2761a864dafadabe0ffc8dc6465"
from langchain_community.llms import Tongyi
llm = Tongyi(
    model="qwen-max",
    # top_p="...",
    # api_key="...",
    # other params...
)
generator_llm = LangchainLLMWrapper(llm)
```

这里需要安装`pip install dashscope`。

如果你使用LlamaIndex框架而不是Langchain与大模型交互，将LangchainLLMWrapper替换成`LlamaIndexLLMWrapper` 即可。

4. 生成测试集
    

使用加载的文档和设置好的LLM运生成测试数据集。注意，TestsetGenerator的构造参数，官方文档写错了。应该没有`embedding_model`参数。`generate_with_langchain_docs`函数中要指定`transforms_embedding_model`参数。

```Python
from ragas.testset import TestsetGenerator
generator = TestsetGenerator(llm=generator_llm)
dataset = generator.generate_with_langchain_docs(docs, transforms_embedding_model=generator_embeddings, testset_size=10)
```

testset_size指定生成的测试集的大小为10。

如果你前面使用的是llama_index的工具来加载文档，那么你应该使用`generate_with_llama_index_docs`这个方法来代替`generate_with_langchain_docs`。

```Python
dataset = generator.generate_with_llama_index_docs(docs, testset_size=10)
```

5. 导出测试集
    

生成的测试集可以导出并进行检查。

```Shell
dataset.to_pandas()
df.to_json('./testsets.json')
df.head()
```

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=N2MzMTZlYzdiZGE1NDI1ZTU3MjExNmJmMmRmZjUyYTBfUTNOQllYYTg4NjFzSGVFSndBdm5EdjRBSlhmQVhwb0xfVG9rZW46TWtMV2JObnZRb0VEWHN4R0FwWmNYYW1XbkRoXzE3ODIyNjM3MDQ6MTc4MjI2NzMwNF9WNA&add_watermark=true&scene_type=CCM)

在生成测试集的过程中，Ragas有两个主要的操作：

1. **知识图谱创建（KnowledgeGraph Creation）**：使用你提供的文档创建一个知识图谱，并使用各种转换（Transformations）来丰富知识图谱，添加额外的信息，这些信息将用于生成测试集。
    
2. **测试集生成（Testset Generation）**：使用知识图谱生成一组场景（scenarios），这些场景将被用来生成测试集。
    

下面详细介绍一下这两个过程的实现。

首先，知识图谱创建。

通过提供文档创建知识图谱，并使用Transformations丰富知识图谱。

```Python
from ragas.testset.graph import KnowledgeGraph
kg = KnowledgeGraph()
```

初始时，这个知识图谱没有任何节点（nodes）和关系（relationships）。

1. **添加文档到知识图谱**：
    

遍历之前加载的文档（`docs`），为每个文档创建一个`Node`实例，并将其添加到知识图谱的节点列表中。

```Python
from ragas.testset.graph import Node, NodeType
for doc in docs:
    kg.nodes.append(
        Node(
            type=NodeType.DOCUMENT,
            properties={"page_content": doc.page_content, "document_metadata": doc.metadata}
        )
    )
```

每个节点都被标记为`NodeType.DOCUMENT`类型，并包含两个属性：`page_content`（文档的内容）和`document_metadata`（文档的元数据）。在添加文档后，知识图谱的状态更新为包含多个节点（nodes）和0个关系（relationships），因为目前只是简单地将文档作为节点添加到图中，还没有定义任何节点之间的关系。

2. **使用变换丰富知识图谱**
    

通过变换（Transformations）丰富知识图谱（KnowledgeGraph）的信息。

```Python
from ragas.testset.transforms import default_transforms, apply_transforms
define your LLM and Embedding Model
here we are using the same LLM and Embedding Model that we used to generate the testset
transformer_llm = generator_llm
embedding_model = generator_embeddings
trans = default_transforms(llm=transformer_llm, embedding_model=embedding_model)
apply_transforms(kg, trans)
```

通过调用`default_transforms`函数并传入LLM和嵌入模型，创建了一个变换集合`trans`。然后，使用`apply_transforms`函数将这些变换应用到知识图谱`kg`上。

3. **保存和加载知识图谱**
    

知识图谱丰富完成后，将知识图谱保存为JSON文件。

```Python
kg.save("knowledge_graph.json")
```

使用`kg.save("knowledge_graph.json")`将知识图谱保存为JSON文件。

随后，可以使用`KnowledgeGraph.load("knowledge_graph.json")`来加载这个保存的知识图谱。

```Python
loaded_kg = KnowledgeGraph.load("knowledge_graph.json")
loaded_kg
```

查看加载之后知识图谱的状态，会包含多个节点和多个关系。这表明知识图谱已经被成功地丰富了。

接着，使用知识图谱生成测试集。

1. **创建TestsetGenerator实例**：
    

加载之前生成的知识图谱`loaded_kg`和`generator_llm`（之前设置的LLM）来创建一个`TestsetGenerator`实例。这个实例将用于生成测试集。

```Python
from ragas.testset import TestsetGenerator
generator = TestsetGenerator(llm=generator_llm, knowledge_graph=loaded_kg)
```

2. **定义查询分布**：
    

查询分布（query distribution）是指在生成测试集时，不同类型的查询按照一定的概率分布被选取的模式。在机器学习和自然语言处理中，特别是在构建测试集时，查询分布可以确保测试集的多样性和代表性，从而更好地评估模型的性能。

```Python
from ragas.testset.synthesizers import default_query_distribution
query_distribution = default_query_distribution(generator_llm)
```

Ragas默认使用`default_query_distribution`生成查询分布。它包括三种类型的查询合成器，每种都有不同的权重：

- `SingleHopSpecificQuerySynthesizer`：单跳具体查询合成器，权重为0.5。
    
- `MultiHopAbstractQuerySynthesizer`：多跳抽象查询合成器，权重为0.25。
    
- `MultiHopSpecificQuerySynthesizer`：多跳具体查询合成器，权重为0.25。
    

权重表示在生成数据集时，它们被选中的概率。这些查询合成器负责生成不同类型的查询，而它们的概率则决定了在生成测试集时，每种类型的查询被生成的频率。这样做的目的是为了模拟真实世界中查询的多样性，以及确保测试集能够覆盖不同的查询类型。

通过这种方式，`query_distribution`定义了一个生成测试集时的查询生成策略，确保了测试集中包含了不同类型和难度的查询，从而可以更全面地评估模型的性能。

3. **生成测试集**：
    

使用`TestsetGenerator`实例的`generate`方法来生成测试集。

```Python
testset = generator.generate(testset_size=10, query_distribution=query_distribution)
testset.to_pandas()
```

这将生成一个包含10个测试案例的测试集，并且将测试集转换为Pandas DataFrame，以便进行进一步的检查和分析。我们可以对上述过程进行个性化定制，以满足我们对测试集生成的需求。

5. ### 执行评估
    

准备好了评测集，接下来就是执行评测了。主要涉及以下步骤：加载数据集、选择评估指标、选择评估语言模型（LLM），并运行评估，最终导出和分析结果。

下面是一个标准流程：

1. **加载评测集**
    

这里使用的是Hugging Face托管的“amnesty_qa”数据集，这是一个基于Amnesty International（国际特赦组织，简称AI）的报告创建的问答数据集。数据集包含问题、正确答案和上下文信息，支持英语、马拉雅拉姆语和印地语，但仅提供评估数据集。

```Python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from datasets import load_dataset

dataset = load_dataset(
    "explodinggradients/amnesty_qa",
    "english_v3",
    trust_remote_code=True
)

from ragas import EvaluationDataset

eval_dataset = EvaluationDataset.from_hf_dataset(dataset["eval"])
```

评测集的样例eval_dataset[0]：

```JSON
SingleTurnSample(user_input="What are the global implications of the USA Supreme Court ruling on abortion?", retrieved_contexts=["- In 2022, the USA Supreme Court handed down a decision ruling that overturned 50 years of jurisprudence recognizing a constitutional right to abortion.\n- This decision has had a massive impact: one in three women and girls of reproductive age now live in states where abortion access is either totally or near-totally inaccessible.\n- The states with the most restrictive abortion laws have the weakest maternal health support, higher maternal death rates, and higher child poverty rates.\n- The USA Supreme Court ruling has also had impacts beyond national borders due to the geopolitical and cultural influence wielded by the USA globally and the aid it funds.\n- SRR organizations and activists across the world have expressed fear about the ruling laying the groundwork for anti-abortion legislative and policy attacks in other countries.\n- Advocates have also observed the ruling's impact on progressive law reform and the stalling of the adoption and enforcement of abortion guidelines in certain African countries.\n- The ruling has created a chilling effect in international policy spaces, emboldening anti-abortion state and non-state actors to undermine human rights protections.", "The USA Supreme Court ruling on abortion has sparked intense debates and discussions not only within the country but also around the world. Many countries look to the United States as a leader in legal and social issues, so the decision could potentially influence the policies and attitudes towards abortion in other nations.", "The ruling may also impact international organizations and non-governmental groups that work on reproductive rights and women's health issues. Depending on the outcome, there could be shifts in funding, advocacy efforts, and collaborations with American counterparts, leading to ripple effects in the global fight for reproductive justice."], reference_contexts=None, response="The global implications of the USA Supreme Court ruling on abortion can be significant, as it sets a precedent for other countries and influences the global discourse on reproductive rights. Here are some potential implications:\n\n1. Influence on other countries: The Supreme Court's ruling can serve as a reference point for other countries grappling with their own abortion laws. It can provide legal arguments and reasoning that advocates for reproductive rights can use to challenge restrictive abortion laws in their respective jurisdictions.\n\n2. Strengthening of global reproductive rights movements: A favorable ruling by the Supreme Court can energize and empower reproductive rights movements worldwide. It can serve as a rallying point for activists and organizations advocating for women's rights, leading to increased mobilization and advocacy efforts globally.\n\n3. Counteracting anti-abortion movements: Conversely, a ruling that restricts abortion rights can embolden anti-abortion movements globally. It can provide legitimacy to their arguments and encourage similar restrictive measures in other countries, potentially leading to a rollback of existing reproductive rights.\n\n4. Impact on international aid and policies: The Supreme Court's ruling can influence international aid and policies related to reproductive health. It can shape the priorities and funding decisions of donor countries and organizations, potentially leading to increased support for reproductive rights initiatives or conversely, restrictions on funding for abortion-related services.\n\n5. Shaping international human rights standards: The ruling can contribute to the development of international human rights standards regarding reproductive rights. It can influence the interpretation and application of existing human rights treaties and conventions, potentially strengthening the recognition of reproductive rights as fundamental human rights globally.\n\n6. Global health implications: The Supreme Court's ruling can have implications for global health outcomes, particularly in countries with restrictive abortion laws. It can impact the availability and accessibility of safe and legal abortion services, potentially leading to an increase in unsafe abortions and related health complications.\n\nIt is important to note that the specific implications will depend on the nature of the Supreme Court ruling and the subsequent actions taken by governments, activists, and organizations both within and outside the United States.", multi_responses=None, reference="The global implications of the USA Supreme Court ruling on abortion are significant. The ruling has led to limited or no access to abortion for one in three women and girls of reproductive age in states where abortion access is restricted. These states also have weaker maternal health support, higher maternal death rates, and higher child poverty rates. Additionally, the ruling has had an impact beyond national borders due to the USA's geopolitical and cultural influence globally. Organizations and activists worldwide are concerned that the ruling may inspire anti-abortion legislative and policy attacks in other countries. The ruling has also hindered progressive law reform and the implementation of abortion guidelines in certain African countries. Furthermore, the ruling has created a chilling effect in international policy spaces, empowering anti-abortion actors to undermine human rights protections.", rubric=None)
```

2. **设置评测指标**
    

```JSON
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas import evaluate
```

3. **选择评估器模型**
    

上面选择的评估指标都是基于大型语言模型（LLM）的指标，我们需要确定用于评估的大型语言模型（LLM）。以使用QWen大模型为例，这里使用LangChain调用QWen。

```Python
import os
os.environ["OPENAI_API_KEY"] = "获取APIKEY"  # 必须要有，NIOGPT平台的serivceid
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI  # NIOGPT平台的语言模型兼容OpenAI协议，所以用ChatOpenAI
from niogpt import NIOGPTEmbeddings  # NIOGPT平台的Embedding模型封装类

llm = ChatOpenAI(
    openai_api_key="e25752e645834d2fb8d7f6fd2ccc86c1",
    base_url="https://chatnio.nioint.com/v1"
)
# print(llm.invoke("你是谁"))

embeddings = NIOGPTEmbeddings(
    api_key="3e12397789bc4e2fb0481e74498c292e",
    model="bce",
    deployment="bce",
    user="yinliang.he",
    base_url="https://chatnio-test.nioint.com/v1/",
    default_headers={"Content-Type": "application/json", "X-WHITELIST-TOKEN": "61783ff4eaacb5afcb7786e180c51cf6"},
)
# print(embeddings.embed_documents(["你好"]))

# 使用NIOGPT平台的qwen-14b作为评估器模型
evaluator_llm = LangchainLLMWrapper(llm)

# 使用NIOGPT平台的嵌入模型作为嵌入评估器
evaluator_embeddings = LangchainEmbeddingsWrapper(embeddings)
```

注：需要安装`pip install langchain-openai`。

NIOGPTEmbeddings是对NIOGPT平台的embedding模型封装（参考langchain_community/embeddings/zhipuai.py改造的）：

```Python
import os
from typing import Any, Dict, List, Optional, Union, Mapping

from langchain_core.embeddings import Embeddings
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator


class NIOGPTEmbeddings(BaseModel, Embeddings):
    """ZhipuAI embedding model integration.

    Setup:

        To use, you should have the ``zhipuai`` python package installed, and the
        environment variable ``ZHIPU_API_KEY`` set with your API KEY.

        More instructions about ZhipuAi Embeddings, you can get it
        from  https://open.bigmodel.cn/dev/api#vector

        .. code-block:: bash

            pip install -U zhipuai
            export ZHIPU_API_KEY="your-api-key"

    Key init args — completion params:
        model: Optional[str]
            Name of ZhipuAI model to use.
        api_key: str
            Automatically inferred from env var `ZHIPU_API_KEY` if not provided.

    See full list of supported init args and their descriptions in the params section.

    Instantiate:

        .. code-block:: python

            from langchain_community.embeddings import ZhipuAIEmbeddings

            embed = ZhipuAIEmbeddings(
                model="embedding-2",
                # api_key="...",
            )

    Embed single text:
        .. code-block:: python

            input_text = "The meaning of life is 42"
            embed.embed_query(input_text)

        .. code-block:: python

            [-0.003832892, 0.049372625, -0.035413884, -0.019301128, 0.0068899863, 0.01248398, -0.022153955, 0.006623926, 0.00778216, 0.009558191, ...]


    Embed multiple text:
        .. code-block:: python

            input_texts = ["This is a test query1.", "This is a test query2."]
            embed.embed_documents(input_texts)

        .. code-block:: python

            [
                [0.0083934665, 0.037985895, -0.06684559, -0.039616987, 0.015481004, -0.023952313, ...],
                [-0.02713102, -0.005470169, 0.032321047, 0.042484466, 0.023290444, 0.02170547, ...]
            ]
    """  # noqa: E501

    client: Any = Field(default=None, exclude=True)  #: :meta private:
    model: str = Field(default="embedding-2")
    """Model name"""
    api_key: str
    """Automatically inferred from env var `ZHIPU_API_KEY` if not provided."""
    dimensions: Optional[int] = None
    """The number of dimensions the resulting output embeddings should have.

    Only supported in `embedding-3` and later models.
    """
    user: str
    base_url: Optional[str] = Field(default=None, alias="base_url")
    default_headers: Union[Mapping[str, str], None] = None

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that auth token exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "OPENAI_API_KEY")
        values["base_url"] = values["base_url"] or os.getenv(
            "OPENAI_API_BASE"
        )

        try:
            from openai import OpenAI

            values["client"] = OpenAI(api_key=values["api_key"], base_url=values["base_url"],
                                      default_headers=values["default_headers"])
        except ImportError:
            raise ImportError(
                "Could not import zhipuai python package."
                "Please install it with `pip install zhipuai`."
            )
        return values

    def embed_query(self, text: str) -> List[float]:
        """
        Embeds a text using the AutoVOT algorithm.

        Args:
            text: A text to embed.

        Returns:
            Input document's embedded list.
        """
        resp = self.embed_documents([text])
        return resp[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of text documents using the AutoVOT algorithm.

        Args:
            texts: A list of text documents to embed.

        Returns:
            A list of embeddings for each document in the input list.
            Each embedding is represented as a list of float values.
        """
        if self.dimensions is not None:
            resp = self.client.embeddings.create(
                model=self.model,
                input=texts,
                dimensions=self.dimensions,
            )
        else:
            resp = self.client.embeddings.create(model=self.model, input=texts, user=self.user)
        embeddings = [r.embedding for r in resp.data]
        return embeddings
```

4. **执行评估**
    

```JSON
metrics = [
    AnswerRelevancy(embeddings=evaluator_embeddings, llm=evaluator_llm),
    # ResponseRelevancy(embeddings=evaluator_embeddings),     # 响应相关性(question-answer)
    ContextPrecision(llm=evaluator_llm),                    # 上下文精确度(question-query)
    Faithfulness(llm=evaluator_llm),                        # 忠实度(context-answer)
    NoiseSensitivity(llm=evaluator_llm),                    # 噪声敏感度(context-answer)
    SemanticSimilarity(embeddings=evaluator_embeddings),    # 答案的语义相似度(answer-ground_truth)
    FactualCorrectness(llm=evaluator_llm),                  # 事实正确性(answer-ground_truth)
    LLMContextRecall(llm=evaluator_llm),                    # 上下文召回率(context-ground_truth)
    ContextEntityRecall(llm=evaluator_llm),                 # 上下文实体召回率(context-ground_truth)
]
results = evaluate(dataset=eval_dataset, metrics=metrics)
```

`results`内容：

```Python
{'context_recall': 0.9158, 'factual_correctness': 0.7572, 'faithfulness': 0.7220, 'semantic_similarity': 0.8509}
```

5. **导出评估结果**
    

```JSON
df = results.to_pandas()
df.to_json('./output.json')
```

暂时无法在飞书文档外展示此内容

```Python
>>> df.head()
                                          user_input                                 retrieved_contexts                                           response  ... factual_correctness  faithfulness  semantic_similarity
0  What are the global implications of the USA Su...  [- In 2022, the USA Supreme Court handed down ...  The global implications of the USA Supreme Cou...  ...                 NaN      0.640000             0.903598
1  Which companies are the main contributors to G...  [In recent years, there has been increasing pr...  According to the Carbon Majors database, the m...  ...                0.30      0.200000             0.875961
2  Which private companies in the Americas are th...  [The issue of greenhouse gas emissions has bec...  According to the Carbon Majors database, the l...  ...                0.15      0.000000             0.929812
3  What action did Amnesty International urge its...  [In the case of the Ogoni 9, Amnesty Internati...  Amnesty International urged its supporters to ...  ...                0.25      0.400000             0.763458
4  What are the recommendations made by Amnesty I...  [In recent years, Amnesty International has fo...  Amnesty International made several recommendat...  ...                0.08      0.142857             0.736439

[5 rows x 8 columns]
```