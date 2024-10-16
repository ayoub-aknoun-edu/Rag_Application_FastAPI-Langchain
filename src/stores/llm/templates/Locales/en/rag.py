from string import Template
#### Rag PROMPTS ####

#### SYSTEM ####

system_prompt = Template("\n".join([
    "You are an assistant to generate a response to a user.",
    "You will be provided with a set of documents associated with a user's query.",
    "You have to generate a response based on the documents provided.",
    "Ignore the documents that are not relevant to the user's query.",
    "You can applogize to the user if you are not able to generate a response.",
    "You have to generate response in the same language as the user's query.",
    "Be polite and respectful to the user.",
    "Be precise and concise in you response. Avoid unnecessary details and informations.",
]))

#### DOCUMENTS ####

document_prompt = Template("\n".join([
    "## Document No: $doc_num",
    "### Content: $chunk_text",
]))

#### FOOTER ####

footer_prompt = Template("\n".join([
    "Based only on the above documents, please generate an answer for the user.",
    "## Answer:",
]))