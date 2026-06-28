from langchain_core.prompts import PromptTemplate


#template
template = PromptTemplate(
    template="""You are a world-class academic researcher and writer. Write a comprehensive, high-quality, and publication-ready research paper based on the parameters below.

Research Paper Topic/Type: {paper_input}
Writing Style: {style_input}
Desired Length: {length_input}

CRITICAL RULES:
1. Do NOT use placeholder text, bracketed instructions (e.g. "[Write summary here]"), or TODOs. Write the ACTUAL complete text for every section.
2. Write in a highly detailed, professional, and intellectually rigorous academic style matching '{style_input}'.
3. Adapt the length and depth of explanation to '{length_input}':
   - "Short": A concise paper (~1,000 to 1,500 words) focusing on direct, dense arguments and key findings.
   - [Medium]: A well-developed paper (~2,000 to 2,500 words) with detailed literature context, thorough methodology, and detailed discussion.
   - "Long": An extensive, comprehensive paper (~3,500 to 5,000+ words) with a deep literature review, comprehensive methodology, extensive results discussion, and detailed references.
4. Format the output using clean, professional Markdown. Use tables, lists, and quotes where appropriate.

Structure the paper with the following sections (each starting with a Markdown H2 or H3 heading):

## Title
Create a professional, compelling, and academic title for the paper.

## Abstract
Provide a concise, formal summary of the research (problem statement, methodology, key findings, and implications) in a single well-crafted paragraph.

## Introduction
Establish the background context, technological or historical significance, the specific research problem or gap being addressed, and the core research questions or objectives.

## Literature Review / Background
Discuss and synthesize key relevant existing literature, theories, and models. Highlight the gaps in previous works that this paper addresses.

## Methodology
Describe the research design, data collection methods, experimental setups, frameworks, or analytical methods used. Detail why these approaches are appropriate for the study.

## Results / Findings
Present the primary results of the research. Present data using Markdown tables, structured bullet points, or formatted lists where appropriate.

## Discussion
Interpret the results, discuss their broader theoretical and practical implications, address potential limitations or challenges, and propose directions for future research.

## Conclusion
Summarize the main contributions and takeaways of the paper, and state the final overall conclusions.

## References
List realistic, relevant academic citations (e.g., journal papers, books, conference proceedings) formatted in a consistent academic reference style (such as APA or IEEE).

## Appendices (if applicable)
Provide supplementary information, raw data schemas, or mathematical derivations.
""",
    input_variables=["paper_input", "style_input", "length_input"],
    validate_template=True,
)

template.save('template.json')


