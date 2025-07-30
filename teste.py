from markdown_it import MarkdownIt
import json

md_text = """```json
{
  "specialty": "Neurologia",
  "urgency": "Média",
  "explanation": "A dor de cabeça é um sintoma comum com diversas causas, desde tensão muscular até condições mais graves como hemorragia subaracnóide ou aneurisma.  A avaliação por um neurologista é necessária para determinar a causa e o tratamento adequado. A urgência é média pois, embora a maioria das dores de cabeça não sejam graves, algumas exigem intervenção imediata. ",
  "immediate_care": "Se a dor de cabeça for intensa, súbita, acompanhada de febre alta, rigidez na nuca, visão turva, fraqueza em um lado do corpo, dificuldade para falar ou alterações na consciência, procure atendimento médico imediatamente.  Para dores de cabeça menos intensas, agende uma consulta com um médico o mais breve possível."
}
```
"""

print(md_text.endswith("\n```\n"))

if md_text.startswith("```json\n"):
    result_text = md_text.replace("```json\n", "", 1) # Remove apenas a primeira ocorrência
if md_text.endswith("\n```"):
    result_text = result_text.rsplit("\n```", 1)[0] # Remove apenas a última ocorrência
#result_text = result_text.strip() # Remove quaisquer espaços em branco ou novas linhas extras

json_output = json.loads(result_text)

print(json_output)
